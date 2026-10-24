#!/usr/bin/env python3
"""Converteix un model PA 2027 omplert a JSON del Motor. Ús: python3 scripts/xlsx_a_json_2027.py fitxer.xlsx [sortida.json]
Les fórmules s'han de tenir calculades (obrir i desar amb Excel abans d'enviar)."""
import sys, json, openpyxl
def norm(v): return '' if v is None else str(v).strip()
def converteix(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['PROGRAMA ANUAL 2027']; codi = norm(ws['B2'].value)
    acts = []
    for r in range(6, ws.max_row + 1):
        v = [ws.cell(r, c).value for c in range(1, 23)]
        if not norm(v[2]) and not norm(v[3]): continue
        rel = ', '.join(norm(x) for x in v[5:8] if norm(x))
        imp = v[12] if isinstance(v[12], (int, float)) else 0
        grau = v[16] if isinstance(v[16], (int, float)) else 0
        acts.append({'codi': norm(v[0]), 'codiRAE': norm(v[1]), 'actuacio': norm(v[2]), 'objectiuOperatiuPrincipal': norm(v[3]),
            'objectiusOperatiusRelacionats': rel, 'eixPlaEstrategic': norm(v[8]), 'tipusActuacio_despesa': norm(v[9]), 'partidaRAE': norm(v[10]),
            'tipusActuacio_MAP': norm(v[11]), 'import': imp, 'accioPla_indicador': norm(v[13]), 'fitaMinima': v[14], 'fitaMaxima': v[15],
            'grauCompliment': grau, 'observacions': norm(v[20]), 'gestorResponsable': norm(v[17]), 'actuacioRecurrent': norm(v[18]),
            'naturalesa': norm(v[19]), 'revisio': norm(v[21])})
    return {'codiPla': f'{codi}-PA2027', 'parc': codi, 'any': 2027, 'actuacions': acts}
if __name__ == '__main__':
    d = converteix(sys.argv[1]); out = sys.argv[2] if len(sys.argv) > 2 else f"{d['parc']}_PA2027.json"
    json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(out, len(d['actuacions']), 'actuacions')
