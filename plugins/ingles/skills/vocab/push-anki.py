#!/usr/bin/env python3
"""
Empurra o registro de vocabulario do plugin `ingles` (<pasta>/ingles-vocabulario.csv) pro Anki,
via AnkiConnect.

Idempotente: cada linha do CSV tem uma tag de identidade `uid::voc-NNNN` (gravada no proprio CSV
se faltar). O push compara por essa tag, entao rodar duas vezes nao cria duplicata, e corrigir uma
linha do CSV atualiza o card correspondente em vez de criar outro.

Uso (a skill /ingles:vocab passa o caminho do script e do CSV):
    python push-anki.py --csv <pasta>/ingles-vocabulario.csv --dry-run
    python push-anki.py --csv <pasta>/ingles-vocabulario.csv
    python push-anki.py --csv <pasta>/ingles-vocabulario.csv --deck "Ingles"

Pre-requisitos: Anki aberto, add-on AnkiConnect (codigo 2055492159) instalado.
O tipo de nota e detectado sozinho ("Basic" no Anki em ingles, "Basico" em portugues);
use --model se o seu tiver outro nome.
"""

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ANKI_URL = "http://127.0.0.1:8765"
DEFAULT_DECK = "English"
PREFIX = "voc"
MODEL_CANDIDATES = ("Basic", "Básico", "Básica", "Basique", "Básico (e cartão invertido)")

UID_RE = re.compile(r"^uid::([a-z]+)-(\d+)$")


def anki(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params})
    req = urllib.request.Request(
        ANKI_URL, payload.encode("utf-8"), {"Content-Type": "application/json"}
    )
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.URLError as exc:
        raise SystemExit(
            f"Nao consegui falar com o Anki em {ANKI_URL} ({exc}).\n"
            "O Anki precisa estar ABERTO e com o add-on AnkiConnect instalado.\n"
            "Sem AnkiConnect: no Anki, File > Import e escolha o ingles-vocabulario.csv."
        )
    if resp.get("error"):
        raise RuntimeError(f"AnkiConnect recusou '{action}': {resp['error']}")
    return resp["result"]


def pick_model(wanted):
    """Devolve (modelo, campo_frente, campo_verso)."""
    names = anki("modelNames")
    if wanted:
        if wanted not in names:
            raise SystemExit(f"Tipo de nota '{wanted}' nao existe. Disponiveis: {', '.join(names)}")
        model = wanted
    else:
        model = next((m for m in MODEL_CANDIDATES if m in names), None)
        if model is None:
            raise SystemExit(
                "Nao achei o tipo de nota basico. Rode com --model <nome>. "
                f"Disponiveis: {', '.join(names)}"
            )
    fields = anki("modelFieldNames", modelName=model)
    if len(fields) < 2:
        raise SystemExit(f"O tipo de nota '{model}' tem menos de 2 campos.")
    return model, fields[0], fields[1]


def read_csv(path):
    """Devolve (linhas_de_cabecalho, linhas_de_dados). Cabecalho = linhas com '#'."""
    header, rows = [], []
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if not row:
                continue
            if row[0].startswith("#"):
                header.append(",".join(row))
            else:
                if len(row) != 3:
                    raise SystemExit(
                        f"{path.name}: linha com {len(row)} colunas (esperado 3). "
                        "Aspas mal escapadas? Corrija antes de empurrar.\n"
                        f"  {row[0][:80]}"
                    )
                rows.append(row)
    return header, rows


def stamp_uids(path, header, rows):
    """Garante uid::voc-NNNN em toda linha. Reescreve o CSV se faltar algum."""
    used = set()
    for _, _, tags in rows:
        for tag in tags.split():
            m = UID_RE.match(tag)
            if m and m.group(1) == PREFIX:
                used.add(int(m.group(2)))

    nxt = max(used) + 1 if used else 1
    changed = False
    for i, (front, back, tags) in enumerate(rows):
        if any(UID_RE.match(t) for t in tags.split()):
            continue
        rows[i] = [front, back, f"uid::{PREFIX}-{nxt:04d} {tags}".strip()]
        nxt += 1
        changed = True

    if changed:
        with path.open("w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(header) + "\n")
            csv.writer(fh, lineterminator="\n").writerows(rows)
    return changed


def uid_of(tags):
    for tag in tags.split():
        if UID_RE.match(tag):
            return tag
    return None


def push(path, deck, model, f_front, f_back, dry_run):
    header, rows = read_csv(path)
    if stamp_uids(path, header, rows):
        print(f"  {path.name}: uids gravados no CSV")

    if not dry_run:
        anki("createDeck", deck=deck)

    created = updated = unchanged = 0
    for front, back, tags in rows:
        uid = uid_of(tags)
        tag_list = tags.split()
        found = anki("findNotes", query=f'"tag:{uid}"')

        if len(found) > 1:
            print(f"  ! {uid}: {len(found)} notas com essa tag no Anki, pulando")
            continue

        if not found:
            created += 1
            print(f"  + {uid}  {front[:58]}")
            if not dry_run:
                anki(
                    "addNote",
                    note={
                        "deckName": deck,
                        "modelName": model,
                        "fields": {f_front: front, f_back: back},
                        "tags": tag_list,
                        "options": {"allowDuplicate": False},
                    },
                )
            continue

        note_id = found[0]
        info = anki("notesInfo", notes=[note_id])[0]
        same_fields = (
            info["fields"][f_front]["value"] == front
            and info["fields"][f_back]["value"] == back
        )
        same_tags = sorted(info["tags"]) == sorted(tag_list)
        if same_fields and same_tags:
            unchanged += 1
            continue

        # "~" = o card no Anki difere do CSV. Se o aluno editou no app, o push sobrescreve:
        # olhar o dry-run antes.
        updated += 1
        print(f"  ~ {uid}  {front[:58]}")
        if not dry_run:
            if not same_fields:
                anki(
                    "updateNoteFields",
                    note={"id": note_id, "fields": {f_front: front, f_back: back}},
                )
            if not same_tags:
                anki("removeTags", notes=[note_id], tags=" ".join(info["tags"]))
                anki("addTags", notes=[note_id], tags=" ".join(tag_list))

    return created, updated, unchanged


def main():
    # terminal do Windows usa cp1252 e quebra no print de acento ou IPA
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Empurra o ingles-vocabulario.csv pro Anki.")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que faria, sem tocar no Anki")
    ap.add_argument("--no-sync", action="store_true", help="nao sincronizar com o AnkiWeb")
    ap.add_argument("--csv", type=Path, required=True, help="caminho do ingles-vocabulario.csv")
    ap.add_argument("--deck", default=DEFAULT_DECK, help=f"deck no Anki (padrao: {DEFAULT_DECK})")
    ap.add_argument("--model", help="tipo de nota (padrao: detecta Basic/Basico)")
    args = ap.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"{args.csv} nao existe.")

    anki("version")  # falha cedo e com mensagem legivel se o Anki estiver fechado
    model, f_front, f_back = pick_model(args.model)

    print(f"{args.csv.name} -> {args.deck} ({model})")
    created, updated, unchanged = push(args.csv, args.deck, model, f_front, f_back, args.dry_run)
    print(
        f"\n{created} criados, {updated} atualizados, {unchanged} sem mudanca"
        + (" (dry-run, nada foi escrito no Anki)" if args.dry_run else "")
    )

    if not args.dry_run and not args.no_sync and (created or updated):
        print("sincronizando com o AnkiWeb...")
        try:
            anki("sync")
            print("sync ok")
        except RuntimeError as exc:
            # FULL_SYNC: o Anki exige escolher entre subir a colecao local ou baixar a do
            # AnkiWeb, e um dos lados perde dados. Decisao do usuario, nunca automatica.
            print(f"\ncards gravados, mas o sync nao passou sozinho:\n  {exc}")
            print("Aperte Sincronizar dentro do Anki. Os cards ja estao salvos localmente.")


if __name__ == "__main__":
    sys.exit(main())
