---
id: BRG-017
fault_name: Unbalance-induced bearing loading
aliases:
- rotor unbalance affecting bearing
- 1x unbalance
category: adjacent_machine_fault
bearing_components:
- system_level
observability_from_vibration: high
confidence: high
tags:
- 1x_unbalance
- adjacent_machine_fault
- high
- rotor_unbalance_affecting_bearing
- system_level
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
---

## Symptoms
- Strong 1× running-speed vibration
- Increased radial load on bearing
- May accelerate fatigue and looseness

## Likely causes
- Mass eccentricity on rotor, fan, pulley, or coupling
- Build-up of product or debris
- Manufacturing or repair imbalance

## Expected vibration signatures
- Dominant 1× running-speed component
- Phase stable with speed if unbalance is primary

## Confirm tests
- Confirm dominant synchronous 1× peak
- Check phase consistency and speed relation
- Inspect rotor/fan/pulley for build-up or mass imbalance

## Fixes
- Balance the rotor
- Clean or repair rotating components
- Inspect bearing for secondary damage if vibration was prolonged

## Notes
Not a bearing defect by itself, but critical in a debugging assistant because it is a common confounder.
