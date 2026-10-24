#!/usr/bin/env python3
"""Genera els models Programa d'actuacions 2027. Ús: python3 scripts/generar_model_2027.py PNAP"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pa2027_lib as L
BASE = 'PLANS_2027/_origen/Model_Programa_actuacions_2027_base.xlsx'
PARCS = {
 'PNAP': dict(codi='PNAP', nom="Parc Natural de l'Alt Pirineu", pla='PLANS_ESTRATEGICS/Alt Pirineu_Pla Estrategic_final.xlsx',
              pla_nom='Alt Pirineu_Pla Estrategic_final.xlsx', pa2026='PLANS_2026/PNAP_Programa_actuacions_2026_v2.xlsx', gestors_fragment="l'alt pirineu"),
}
if __name__ == '__main__':
    for c in sys.argv[1:]:
        print(c, L.construeix_model(PARCS[c], f'PLANS_2027/{c}_Programa_actuacions_2027.xlsx', BASE))
