# Sources and verification

Every outside source used in the dashboard, deck and submission text, what it supports, and how it was checked. Last full check: 15 Nov 2026.

## The challenge itself

| Source | Checked how | Result |
| --- | --- | --- |
| [Official challenge page](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/), Details tab | Opened in a browser and compared with the text the team uploaded | Identical, word for word |
| Same page, Resources tab | Opened in a browser | 10 resources; same links as the uploaded text, plus a one-line description of each (copied in `official-challenge-text.txt`) |

## NASA data

| Source | Checked how | Result |
| --- | --- | --- |
| [NASA PSI repository](https://psi.nasa.gov/physci/repo/search?q=combustion) | Queried PSI's public API | 133 investigations in total; 24 in Combustion Science, all in the dashboard; ASE (PSI-179) added as context |
| DOIs of all 25 investigations | Compared each DOI in `data/psi_data.json` with PSI's live record | 25 of 25 match |
| Saffire-II table (PSI-99) | Downloaded NASA's original CSV | Every value in the 0 g vs 1 g panel matches; 21.5–22.1 % O₂, 20 cm/s |
| Solid-material tables (BASS, BASS-II, Saffire-I/II/III) | Downloaded NASA's original CSVs, read headers | None has a pressure column; highest O₂ in BASS-II is 22.2 % |
| SoFIE, FLARE, FM2, LUCI | Searched PSI | None has data in PSI yet |

## The brief's resources (all 10 opened)

| Resource | What we use from it |
| --- | --- |
| [PSI repository](https://psi.nasa.gov/physci/repo/search?q=combustion) | All data |
| [NASA Glenn: Combustion Science](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/) | Links to FM2, SoFIE, FLARE; CIR and MDCA hardware descriptions |
| [A Researcher's Guide to: Combustion Science (2015)](https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/) | Exact quotes: "NASA-STD-6001 Test 1 is not conservative" (p. 31); flammability minimum "on the order of 10 cm/s," typical of spacecraft ventilation (p. 31); FLEX LOI "significantly lower than in normal gravity" (p. 36); three misconceptions (p. 35); SoFIE 10–40 % O₂ at 0.2–1.5 atm (p. 19) |
| [Apollo 1 (NASA OSMA)](https://sma.nasa.gov/sma-disciplines/accllp/apollo-1) | 100 % oxygen cabin; crew died of carbon monoxide and toxic gases, burns likely survivable; NASA then restricted combustible materials |
| [Apollo 13 (NASA OSMA)](https://sma.nasa.gov/sma-disciplines/accllp/apollo-13) | Oxygen tank explosion; crew moved to the lunar module |
| [Fire aboard Mir (NASA History)](https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/) | 24 Feb 1997; solid-fuel oxygen generator; six crew; blocked path to one Soyuz; smoke for hours |
| [Fireman's Air Tanks (Spinoff)](https://spinoff.nasa.gov/node/9582) | Earth applications |
| [Fire Detector (Spinoff)](https://spinoff.nasa.gov/node/9407) | Shuttle detector that tells smoke from dust; supports the ASE context entry |
| [New Technology for the Fire Attire (Spinoff)](https://spinoff.nasa.gov/node/9918) | Earth applications |
| [NASA ScienceCasts video](https://www.youtube.com/watch?v=W1oXykoz9zg) | Not watched (video); not cited |

## Other NASA sources

| Source | Checked how | Used for |
| --- | --- | --- |
| [NASA Glenn: FM2](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/flammability-of-materials-on-the-moon-fm2/) | Opened | First combustion experiment on another planetary body; materials may burn at lower O₂ in lunar gravity; tests in planned habitat atmospheres |
| [NASA Glenn: SoFIE](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/solid-fuel-ignition-and-extinction-sofie/) | Opened | Narrow Channel Apparatus: PMMA up to 85 % O₂ near normoxic |
| [NASA Glenn: FLARE](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/flammability-limits-at-reduced-g-experiment-flare/) | Linked from the Glenn page | International correlation of 1 g and microgravity flammability limits |
| [Ferkul, Kralik & Liao, LPSC 2026 (NTRS 20260000646)](https://ntrs.nasa.gov/citations/20260000646) | NTRS record checked | Flame spread peaks and the oxygen limit is lowest near lunar gravity |
| [Ferkul, Liao et al., Fire on the Moon (NTRS 20210020516)](https://ntrs.nasa.gov/citations/20210020516) | NTRS record checked | Partial-gravity flammability background |
| [Spacecraft Fire Safety Demonstration (Saffire) fact sheet](https://www.nasa.gov/wp-content/uploads/2025/07/spacecraft-fire-safety-demonstration-saffire.pdf) | Opened | Saffire-IV burned Saffire-II's materials at different pressures and oxygen; Saffire-V covered the pressures and oxygen expected in exploration spacecraft. Neither is in PSI |
| [Ferkul et al., LUCI results (NTRS 20250010653)](https://ntrs.nasa.gov/citations/20250010653) | NTRS record read | LUCI flew on a spinning New Shepard rocket: first extended-duration (over 25 s) combustion tests in simulated lunar gravity; not in PSI |
| [Ferkul et al., LPSC 2026 presentation (NTRS 20260001966)](https://ntrs.nasa.gov/citations/20260001966) | Slides read | Lunar gravity "nearly the most flammable condition"; oxygen limit minimum near lunar g |
| [Orndoff & Marmolejo, Soft goods in 34 % O₂ 8.2 psia atmosphere (NTRS 20200002311)](https://ntrs.nasa.gov/api/citations/20200002311/downloads/20200002311.pdf) | Opened | NASA ground tests of crew textiles in the exploration atmosphere; one reason the "never tested" wording was wrong |
| [NASA Science: SoFIE](https://science.nasa.gov/biological-physical/investigations/sofie) | Opened 15 Nov 2026 | Delivered to the ISS via Cygnus NG-17; listed as operating through February 2025. Not in PSI |
| [JAXA: FLARE](https://humans-in-space.jaxa.jp/en/biz-lab/experiment/theme/detail/000807.html) | Opened 15 Nov 2026 | JAXA investigation of material flammability in microgravity, listed as in progress. Not in PSI |
| [Ferkul et al., LPSC 2026 slides (PDF)](https://ntrs.nasa.gov/api/citations/20260001966/downloads/Ferkul-Lunar%20and%20Planetary%20Science%20Conf%202026%20v2.pdf) | Read 15 Nov 2026 | "Numerical and experimental evidence suggests that Lunar gravity is nearly the most flammable condition." |
| [NASA PSI on the Registry of Open Data](https://registry.opendata.aws/nasa-psi) | Opened | License: no restrictions on use (the dashboard previously said CC0; corrected) |

## Corrections made during verification

- **FM2 link was wrong.** The dashboard linked a guessed address; replaced with NASA Glenn's actual FM2 page.
- **"Same samples" was imprecise.** Saffire-II reports a microgravity and a 1 g result for the same materials, not the same physical samples; wording fixed in the dashboard and docs.
- **Moon-base atmosphere.** The brief says "30 % or greater" oxygen at "10.2 psi or less." The dashboard's 30–34 % and 8.2–10.2 psi target band is our assumption for scoring; findings, deck and submission text now quote the brief's own figures.

- **"NASA has never tested a cabin material in a Moon-base atmosphere" was wrong.** Saffire-IV and V (and ground tests at 34 % O₂, 8.2 psia) did. The finding is now scoped to PSI everywhere: no solid-material test *in PSI* records pressure, and the highest oxygen recorded is 22.2 %.
- **"Flagged values are never corrected" was wrong.** Two ACME BRE formatting slips ("3400%", "2100%") are recovered as 34 % and 21 % and marked approximate; the dashboard now says so.
- **Footer said NASA PSI data is CC0.** PSI's listing says only that there are no restrictions on use; wording corrected.
- **References to files not in the repo** (`data/raw`, `data/processed/INGESTION_REPORT.md`, `ingest/ranking_config.json`) removed from dashboard text.
- **LUCI** was described only as "future data"; it has flown (sounding rocket, simulated lunar g). Card updated with the NTRS record.

- **SoFIE was described as "planned" and grouped with "upcoming" experiments.** NASA lists it as delivered to the ISS and operating through February 2025; wording corrected to say its results are not in PSI yet.

## Space Apps rules

| Source | Note |
| --- | --- |
| [Participant FAQ](https://www.spaceappschallenge.org/resources/participant-faqs/) | 2026 dates: 14–15 November |
| [Project Submission Guide](https://www.spaceappschallenge.org/resources/project-submission-guide/) | Demo limits (7 slides or 30 s), required fields, use-of-AI disclosure |
| [Judging and Awards Guide](https://www.spaceappschallenge.org/resources/judging-awards-guide/) | Five criteria: Influence, Creativity, Validity, Relevance, Presentation |
