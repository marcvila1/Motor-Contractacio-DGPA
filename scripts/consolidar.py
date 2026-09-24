#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consolida tots els fitxers de contractes/*.json en un unic contractes.json
a l'arrel del repositori, que es el que llegeix el Motor de Contractacio.

Cada fitxer individual ha de contenir UN contracte, amb la mateixa estructura
que els elements de l'array "contractes" del fitxer consolidat.

Si algun fitxer es invalid, l'script avorta amb codi 1 i NO reescriu
contractes.json, per no deixar el Motor sense dades.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ARREL = Path(__file__).resolve().parent.parent
CARPETA = ARREL / "contractes"
SORTIDA = ARREL / "contractes.json"

MOTOR_VERSION = "v064"
VERSIO_FORMAT = "2.0"


def clau(contracte):
    """Numero de contracte, que identifica univocament el registre."""
    meta = contracte.get("metadata_contracte") or {}
    num = meta.get("numerocontracte") or contracte.get("numeroContracte")
    return str(num).strip() if num else None


def data_ordre(contracte):
    """Data de creacio, per ordenar. Els que no en tenen van al final."""
    meta = contracte.get("metadata_contracte") or {}
    return meta.get("data_creacio") or contracte.get("data") or "9999"


def main():
    errors = []
    contractes = []
    vistos = {}

    if not CARPETA.is_dir():
        print(f"ERROR: no existeix la carpeta {CARPETA.relative_to(ARREL)}/")
        return 1

    fitxers = sorted(CARPETA.glob("*.json"))
    if not fitxers:
        print(f"AVIS: {CARPETA.relative_to(ARREL)}/ es buida. Es genera un contractes.json sense contractes.")

    for fitxer in fitxers:
        nom = fitxer.name

        try:
            dades = json.loads(fitxer.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{nom}: JSON mal format (linia {e.lineno}, col {e.colno}) - {e.msg}")
            continue
        except Exception as e:
            errors.append(f"{nom}: no s'ha pogut llegir - {e}")
            continue

        if not isinstance(dades, dict):
            errors.append(f"{nom}: l'arrel ha de ser un objecte JSON, no {type(dades).__name__}")
            continue

        # Tolerancia: si algu puja un fitxer amb l'embolcall sencer,
        # n'extraiem els contractes igualment.
        if "contractes" in dades and isinstance(dades["contractes"], list):
            candidats = dades["contractes"]
        else:
            candidats = [dades]

        for candidat in candidats:
            num = clau(candidat)
            if not num:
                errors.append(f"{nom}: falta metadata_contracte.numerocontracte")
                continue

            if num in vistos:
                errors.append(f"{nom}: numero '{num}' duplicat (ja definit a {vistos[num]})")
                continue

            vistos[num] = nom
            contractes.append(candidat)

    if errors:
        print("CONSOLIDACIO AVORTADA. S'han trobat errors:\n")
        for e in errors:
            print(f"  - {e}")
        print(f"\ncontractes.json NO s'ha modificat.")
        return 1

    contractes.sort(key=data_ordre)

    resultat = {
        "metadata": {
            "versio": VERSIO_FORMAT,
            "data_ultim_update": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_contractes": len(contractes),
            "motor_version": MOTOR_VERSION,
            "descripció": "Base de dades de contractes DGPA - generat automaticament des de contractes/",
        },
        "contractes": contractes,
    }

    SORTIDA.write_text(
        json.dumps(resultat, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"OK: {len(contractes)} contractes consolidats des de {len(fitxers)} fitxers.")
    for c in contractes:
        meta = c.get("metadata_contracte") or {}
        estat = c.get("estat_contr", "?")
        print(f"  - {meta.get('numerocontracte')}  [{estat}]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
