---
id: BRG-007
fault_name: Lubrication starvation / ineffective lubrication
aliases:
- poor lubrication
- lubrication failure
- insufficient film
category: root_cause
bearing_components:
- all
observability_from_vibration: medium
confidence: medium_high
tags:
- all
- lubrication_failure
- medium
- poor_lubrication
- root_cause
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
- title: NSK Bearing Maintenance Guide
  source: NSK
  url: https://www.nsk.com/content/dam/nsk/am/en_us/documents/bearings-americas/Bearing-Maintenance-Guide.pdf
- title: SKF Bearing Damage and Failure Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/093168a92d25cc46/pdf_preview_medium/093168a92d25cc46_pdf_preview_medium.pdf
---

## Symptoms
- Rising high-frequency vibration and temperature
- Increased noise and roughness
- Premature growth of localized defect features

## Likely causes
- Wrong lubricant type or amount
- Relubrication interval too long
- Blocked grease path or poor oil supply
- Excess heat degrading lubricant

## Expected vibration signatures
- Broadband HF acceleration growth
- Envelope activity may rise before clear BPFO/BPFI labels
- May evolve into surface distress, spalling, seizure, or fretting-related damage

## Confirm tests
- Check lubricant condition, quantity, and delivery path
- Correlate with temperature and maintenance records
- Inspect whether demodulated spectrum is showing early local defects

## Fixes
- Restore correct lubricant type, quantity, and interval
- Fix delivery path and seals
- Replace damaged bearing if secondary damage is present

## Notes
Vibration alone often indicates the effect of poor lubrication before it cleanly identifies the cause.
