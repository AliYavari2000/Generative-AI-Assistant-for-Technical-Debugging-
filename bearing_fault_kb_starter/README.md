# Bearing Fault Knowledge Base Starter Kit

This starter kit is designed for a **vibration-first debugging assistant** focused on **rolling bearings / ball bearings**.

## What is inside

- `fault_cards/`: 20 starter fault cards in Markdown with YAML front matter
- `scripts/parse_fault_cards.py`: parser that extracts fields and writes JSON / JSONL / CSV metadata
- `exports/`: empty folder for parser outputs

## Design principle

A good bearing-debugging assistant should not collapse everything into a single label like “bearing fault”.

It should separate:

1. **Observable defect pattern**  
   Example: outer race defect, inner race defect, rolling element defect

2. **Likely root cause**  
   Example: lubrication starvation, contamination, misalignment, preload, loose fit, electrical erosion

3. **Recommended confirmation action**  
   Example: compute BPFO/BPFI/BSF/FTF, run envelope analysis, inspect lubricant, check alignment, verify fit/preload

This matters because real industrial failures are often **caused by something upstream**.  
A vibration model may detect a localized defect, while the *maintenance action* depends on the root cause.

## Suggested first taxonomy

### A. Directly observable from vibration
- Outer race defect
- Inner race defect
- Rolling element defect
- Cage defect
- Subsurface fatigue / spalling progression
- Surface distress

### B. Root causes that often appear indirectly in vibration
- Lubrication starvation
- Lubrication contamination
- Pitting
- Fretting
- False brinelling
- Creep / loose fit
- Electrical erosion / fluting
- Overheating / seizure
- Excessive preload
- Corrosion / moisture damage
- Improper installation / handling

### C. Important confounders / adjacent machine faults
- Misalignment-induced bearing loading
- Unbalance-induced bearing loading
- Mechanical looseness near bearing

## Recommended fields per card

Each card contains:
- `fault_name`
- `aliases`
- `category`
- `bearing_components`
- `observability_from_vibration`
- `confidence`
- `references`

and body sections:
- Symptoms
- Likely causes
- Expected vibration signatures
- Confirm tests
- Fixes
- Notes

## How to use this KB in a debugging assistant

### Retrieval
Use the fault cards as retrieval documents:
- retrieve top-k cards using symptom text, spectrum notes, and machine context
- return both **fault hypothesis** and **why it matches**

### Ranking
Rank cards using:
- overlap with spectral clues
- overlap with operating context
- observability weight
- recent maintenance history
- known bearing geometry if BPFO/BPFI/BSF/FTF can be calculated

### Important metadata to add later
To strengthen the KB, extend cards with:
- machine type
- shaft speed range
- load regime
- sensor position
- domain applicability
- seeded fault support
- field evidence support
- vibration-only observability score
- whether envelope analysis is required
- whether teardown/inspection is usually needed

## Recommended next expansion

Grow from 20 cards to 30–40 by splitting:
- lubrication starvation into grease vs oil-film starvation
- contamination into particle vs moisture contamination
- misalignment into angular vs parallel
- looseness into mounting looseness vs seat looseness
- electrical erosion into VFD shaft-current vs grounding-related cases
- outer-race defects by load-zone location where relevant

## Suggested data sources for model evaluation

- **CWRU Bearing Data Center** for seeded outer race / inner race / ball defects and normal baselines
- **NASA IMS bearing dataset** for degradation progression
- **NASA FEMTO bearing dataset** for accelerated life / prognostics style evaluation

## Caveat

Benchmark datasets are useful, but they do **not** fully represent real plant failures.
Use the KB to encode field reasoning that datasets usually miss:
- contamination
- poor lubrication practice
- fit problems
- transport damage
- electrical erosion
- maintenance-history clues

## Example parser usage

```bash
python scripts/parse_fault_cards.py --input_dir fault_cards --out_dir exports
```

This produces:
- `exports/fault_cards.json`
- `exports/fault_cards.jsonl`
- `exports/fault_cards_index.csv`
