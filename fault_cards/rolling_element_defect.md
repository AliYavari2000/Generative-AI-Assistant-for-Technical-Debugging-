---
id: BRG-003
fault_name: Rolling element defect
aliases:
- ball defect
- BSF fault
- rolling element spall
category: localized_bearing_defect
bearing_components:
- rolling_elements
observability_from_vibration: high
confidence: medium_high
tags:
- ball_defect
- bsf_fault
- high
- localized_bearing_defect
- rolling_elements
references:
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
- Impulsive vibration with more variable repetition than pure outer-race defects
- Envelope spectrum peaks near BSF or 2×BSF depending on convention
- Broadband high-frequency energy growth

## Likely causes
- Surface fatigue or spall on a ball
- Poor lubrication and sliding damage
- Contamination or debris indentation

## Expected vibration signatures
- BSF-related peaks with harmonics and possible sidebands
- Amplitude can vary as the damaged rolling element contacts both races
- Time waveform often less regular than a fixed outer-race defect

## Confirm tests
- Calculate BSF from geometry and shaft speed
- Inspect envelope spectrum for BSF-related families
- Check if diagnostic software uses BSF or ball-defect frequency = 2×BSF
- Confirm with teardown or borescope if available

## Fixes
- Replace the bearing
- Improve lubrication and cleanliness
- Check load, fit, and installation practice

## Notes
Use this card carefully because naming conventions differ: some tools label ball-defect frequency as 2×BSF.
