---
id: BRG-013
fault_name: Electrical erosion / fluting
aliases:
- electrical discharge damage
- fluting
- current through bearing
category: root_cause
bearing_components:
- raceways
- rolling_elements
observability_from_vibration: medium
confidence: high
tags:
- electrical_discharge_damage
- fluting
- medium
- raceways
- rolling_elements
- root_cause
references:
- title: NSK Bearing Maintenance Guide
  source: NSK
  url: https://www.nsk.com/content/dam/nsk/am/en_us/documents/bearings-americas/Bearing-Maintenance-Guide.pdf
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
---

## Symptoms
- Distinct tonal noise or roughness after damage develops
- Premature vibration increase even when lubrication appears normal

## Likely causes
- Electric current passing through the bearing
- Poor grounding or inverter-related shaft currents

## Expected vibration signatures
- Can produce characteristic roughness and broadband activity; advanced fluting may create tonal components
- Vibration-only pattern is less canonical than BPFO/BPFI and usually benefits from electrical context

## Confirm tests
- Check for shaft voltage/current and grounding issues
- Inspect raceways for fluting or washboard-like corrugation
- Correlate with inverter drive operation

## Fixes
- Mitigate shaft currents with grounding or insulated bearings where appropriate
- Replace damaged bearing
- Check drive and grounding architecture

## Notes
Include this card because it is common in modern variable-speed-drive systems but often missed by purely mechanical taxonomies.
