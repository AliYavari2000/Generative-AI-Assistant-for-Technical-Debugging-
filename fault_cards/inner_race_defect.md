---
id: BRG-002
fault_name: Inner race defect
aliases:
- BPFI fault
- inner race spall
- inner ring defect
category: localized_bearing_defect
bearing_components:
- inner_race
observability_from_vibration: high
confidence: high
tags:
- bpfi_fault
- high
- inner_race
- inner_race_spall
- localized_bearing_defect
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
- Periodic impacts with stronger amplitude modulation than outer-race faults
- Envelope spectrum peaks near BPFI and harmonics
- Noise and vibration increase with progression

## Likely causes
- Surface fatigue and spalling
- Poor lubrication or contaminated lubricant
- Improper mounting or overload

## Expected vibration signatures
- BPFI and harmonics in envelope spectrum
- Sidebands around BPFI harmonics may appear because the defect rotates through the load zone
- High-frequency acceleration is usually more informative than overall velocity early on

## Confirm tests
- Compute BPFI from geometry and shaft speed
- Overlay BPFI orders on the envelope spectrum
- Check time waveform for repeated impulsive events with modulation
- Inspect for misalignment or preload issues that may have accelerated damage

## Fixes
- Replace the bearing if confirmed
- Correct lubrication, preload, misalignment, or overload
- Review mounting method and fit tolerance

## Notes
Inner-race faults are commonly detectable but may require better demodulation than coarse overall metrics.
