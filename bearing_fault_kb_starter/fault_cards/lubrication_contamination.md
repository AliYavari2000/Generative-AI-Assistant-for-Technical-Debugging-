---
id: BRG-008
fault_name: Contaminated lubrication / debris ingress
aliases:
- dirty grease
- dirty oil
- particle contamination
category: root_cause
bearing_components:
- all
observability_from_vibration: medium
confidence: high
tags:
- all
- dirty_grease
- dirty_oil
- medium
- root_cause
references:
- title: NSK Bearing Maintenance Guide
  source: NSK
  url: https://www.nsk.com/content/dam/nsk/am/en_us/documents/bearings-americas/Bearing-Maintenance-Guide.pdf
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
- title: SKF Bearing Damage and Failure Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/093168a92d25cc46/pdf_preview_medium/093168a92d25cc46_pdf_preview_medium.pdf
---

## Symptoms
- Broadband roughness and high-frequency noise
- Premature impulsive activity and wear
- Damage can evolve into pitting, indentation, or spalling

## Likely causes
- Poor seals
- Dirty relubrication practice
- Moisture or debris entering the bearing
- Particles trapped between rolling element and raceway

## Expected vibration signatures
- Elevated broadband HF energy
- Possible impulsive events but often less clean than a single seeded defect
- Progressive growth of defect-family lines as damage localizes

## Confirm tests
- Inspect seals and contamination source
- Sample lubricant for particles or moisture
- Check if vibration growth correlates with recent maintenance or environmental exposure

## Fixes
- Improve sealing and cleanliness
- Filter or replace lubricant
- Replace the bearing if raceway damage has formed

## Notes
A critical real-world card because many benchmark datasets overrepresent clean seeded defects and underrepresent contamination-driven failures.
