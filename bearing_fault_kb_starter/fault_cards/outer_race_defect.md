---
id: BRG-001
fault_name: Outer race defect
aliases:
- BPFO fault
- outer race spall
- outer ring defect
category: localized_bearing_defect
bearing_components:
- outer_race
observability_from_vibration: high
confidence: high
tags:
- bpfo_fault
- high
- localized_bearing_defect
- outer_race
- outer_race_spall
references:
- title: 'NI Bearings: Envelope Detection and Characteristic Frequencies'
  source: NI
  url: https://www.ni.com/docs/en-US/bundle/labview-sound-and-vibration-toolkit/page/bearings.html
- title: NI Calculate Characteristic Frequencies and Orders
  source: NI
  url: https://www.ni.com/docs/en-US/bundle/labview-sound-and-vibration-toolkit/page/calculating-characteristic-frequencies-and-or.html
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
- title: CWRU Bearing Data Center
  source: Case Western Reserve University
  url: https://engineering.case.edu/bearingdatacenter
---

## Symptoms
- Periodic impulsive vibration
- Envelope spectrum peaks near BPFO and harmonics
- High-frequency acceleration or envelope energy growth
- Noise and vibration increase as damage progresses

## Likely causes
- Surface fatigue and spalling
- Contaminated or ineffective lubrication
- Improper installation or handling
- Excess load or poor fits

## Expected vibration signatures
- BPFO and harmonics in envelope spectrum
- Stable repetition because outer race load zone is often fixed
- May later appear as broad hump in higher-frequency spectrum

## Confirm tests
- Compute BPFO from bearing geometry and shaft speed
- Compare calculated BPFO to envelope-spectrum peaks
- Review time waveform for repetitive impacts
- Inspect lubrication quality and loading/alignment conditions

## Fixes
- Replace the bearing if defect is confirmed
- Correct the root cause: lubrication, contamination, fit, or loading
- Improve sealing and relubrication practice

## Notes
Good first card for a vibration assistant because observability is strong and it maps well to seeded-fault benchmarks such as CWRU.
