# FIREFALL data

The same dataset that is embedded in `index.html`, exported by `python tools/validate.py --export`.

| File | Contents |
| --- | --- |
| `psi_data.json` | Everything the dashboard uses: `provenance`, `config` (scoring weights and targets; team judgments, not PSI data), `investigations` (25 records with DOIs), `tests` (2,009 table rows: 1,879 individual tests, 112 test-day summaries, 8 condition-matrix rows, 8 data-index rows and 2 session rows; see `row_type`) and `reference_scores` |
| `tests.csv` | Every table row as a flat table (2,009 rows plus a header): test ID, PSI investigation, row type, fuel phase, outcome, source line, flags, then each field's raw text and its low/high numeric values |

## Provenance

- **Source:** NASA Physical Science Informatics (psi.nasa.gov). Each investigation is cited by its DOI in `../docs/data-sources.md`.
- **Coverage:** 24 Combustion Science investigations plus one context entry (PSI-179, ASE, cabin aerosols for smoke detection). Test rows come from the 20 investigations that publish experimental tables (22 tables); PSI-60, PSI-62, PSI-115 and PSI-117 are analysis and modeling studies with no experimental table. Images, video and raw sensor files are not parsed.
- **Traceability:** every test row keeps the PSI file (`src`) and line (`ln`) it came from. Values that could not be read reliably are flagged and left empty; the only two recovered values (ACME BRE "3400%" and "2100%", read as 34 % and 21 %) are marked approximate.
- **Oxygen:** `o2_frac` is always the ambient atmosphere. In ACME inverse flames (PSI-10, PSI-159; 274 rows) the burner-stream oxidizer is stored as `o2_burner_frac`.
- **Units:** oxygen and other gas fractions as mole fractions (0–1); pressure in kPa; lengths in mm or cm and times in s, as named in each field.

## AI acknowledgment

In this project, Claude (Anthropic), an AI model, assisted with separating burner-stream oxygen, recovering two values, writing the validator and exports, and checking the data. All values come from NASA's files, none was invented, and `tools/validate.py` re-checks this dataset.
