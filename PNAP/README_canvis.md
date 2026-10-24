# PNAP – Programa Anual 2026: registre de canvis

Document de control de les modificacions fetes a l'Excel `Programa_actuacions_PNAP2026_vd.xlsx` (pestanya PROGRAMA ANUAL) i de la conversió a `PNAP_PA2026.json` per al Motor de Contractació. Data: 24/10/2026.

Fitxers resultants:
- `PNAP_Programa_actuacions_2026_v2.xlsx` — Excel corregit (només canvia la pestanya PROGRAMA ANUAL; la resta, incloses les llistes desplegables, queda intacta).
- `PNAP_PA2026.json` — 342 actuacions, `codiPla` = `PNAP-PA2026`, parc `PNAP`, any 2026.

## 1. Canvis a l'Excel (i, per tant, també al JSON)

| # | Canvi | Cel·les afectades |
|---|---|---|
| 1 | Prefix del codi unificat a `26_` (abans 296 codis començaven per `25_`). | Columna A, 296 files |
| 2 | Objectiu `0.2.2.2` → `02.2.2`. | E29 (`26_NA_26`) |
| 3 | Objectiu `6.1.1` → `06.1.1`. | E101 (`26_CO_05`) |
| 4 | Separador dels objectius relacionats unificat a «, » (abans `;` o `,` sense espai). | E6, E39, E206, E207 |
| 5 | Eix de `26_US_68` canviat de «4. Desenvolupament local» a «5. Ús públic i social». | F241 |

Total: 303 cel·les modificades. Els codis RAE, els imports i la resta de dades no s'han tocat a l'Excel.

## 2. Transformacions només al JSON

- **Imports buits → `0`** (170 actuacions; en total 171 amb import 0 comptant la que ja era 0). Suma total d'imports: 2.158.785,25 €.
- **Imports amb fórmula → valor calculat**, amb la fórmula original a `observacions`:

  | Codi | Fórmula original | Import al JSON |
  |---|---|---|
  | 26_NA_04 | `=724445.66*0.05` | 36.222,28 |
  | 26_NA_06 | `=724445.66*0.05` | 36.222,28 |
  | 26_CU_03 | `=724445.66*0.025` | 18.111,14 |
  | 26_CU_05 | `=724445.66*0.01` | 7.244,46 |
  | 26_US_04 | `=7000/4` | 1.750,00 |

- **Eix «1.Natura» → «1. Natura»** (grafia única).
- **Actuació recurrent**: «Si»/«No» → `true`/`false`.
- **Camps buits** → `null` (`codiRAE`, `objectiusOperatiusRelacionats`, `partidaRAE`, `observacions`, `grauCompliment`). 27 actuacions no tenen grau de compliment.
- **Neteja de text**: espais i salts de línia sobrants eliminats (actuació, observacions, tipus MAP).
- **Camps nous respecte a la majoria de plans**: `tipusActuacio_MAP` i `observacions` (com a PNINA i RMM).
- La columna «Contracte menor a càrrec del RAE» de l'Excel és, en realitat, el tipus de despesa; al JSON és `tipusActuacio_despesa`.

## 3. Pendent de revisió (copiat tal com és a l'Excel)

- **Codis RAE** (decisió: es mantenen):
  - El codi RAE `68` està repetit a `26_NA_14` i `26_DE_40`.
  - `26_CU_34` té el codi RAE `"104.2"` en format text.
  - `26_NA_46` té codi RAE 62 però el tipus de despesa és «Altres».
- **Imports a 0 d'actuacions que podrien tenir import**: `26_CU_29` (contracte menor a càrrec del RAE) i una actuació de PEA Infraestructures.
- Partida RAE de format diferent: `227.014 Serveis de formació` (la resta segueix «227.0014 - …»).
- La pestanya Instruccions conserva l'exemple de codi `25_NA_PNAE_01` i parla de l'any 2025; no s'ha modificat.

## 4. Canvi al Motor

A `Motor_integrat_v038.html`, dins `programaAnualUrls`, s'ha afegit l'entrada:
`'PNAP-PA2026': '…/PNAP_PA2026.json'`.
