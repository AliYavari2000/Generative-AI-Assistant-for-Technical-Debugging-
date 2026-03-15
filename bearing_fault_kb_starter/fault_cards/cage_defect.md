---
id: BRG-004
fault_name: Cage defect
aliases:
- FTF fault
- train defect
- separator defect
category: localized_bearing_defect
bearing_components:
- cage
observability_from_vibration: medium
confidence: medium
tags:
- cage
- ftf_fault
- localized_bearing_defect
- medium
- train_defect
references:
- title: NI Calculate Characteristic Frequencies and Orders
  source: NI
  url: https://www.ni.com/docs/en-US/bundle/labview-sound-and-vibration-toolkit/page/calculating-characteristic-frequencies-and-or.html
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
---

## Symptoms
- Low-frequency modulation and instability
- Impulsive or rattling behavior
- Envelope activity near FTF and combinations with other defect frequencies

## Likely causes
- Poor lubrication
- Skidding or instability under light load
- Advanced bearing damage affecting cage motion
- Debris or installation damage

## Expected vibration signatures
- FTF-related peaks, often weaker than race defects
- Modulation sidebands around higher-frequency bearing components
- May co-occur with BSF/BPFO/BPFI activity in advanced damage

## Confirm tests
- Calculate FTF and inspect envelope/order spectrum
- Look for modulation rather than only strong direct peaks
- Check lubrication state and loading regime
- Inspect for advanced bearing damage if multiple defect families coexist

## Fixes
- Replace the bearing
- Correct lubrication and operating load
- Investigate upstream causes of skidding or severe damage

## Notes
Cage faults are important but usually harder than race faults for a vibration-only system.
