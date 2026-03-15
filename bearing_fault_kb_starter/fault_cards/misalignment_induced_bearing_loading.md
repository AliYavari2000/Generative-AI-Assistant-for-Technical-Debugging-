---
id: BRG-016
fault_name: Misalignment-induced bearing loading
aliases:
- shaft misalignment
- coupling misalignment affecting bearing
category: adjacent_machine_fault
bearing_components:
- system_level
observability_from_vibration: high
confidence: high
tags:
- adjacent_machine_fault
- coupling_misalignment_affecting_bearing
- high
- shaft_misalignment
- system_level
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
---

## Symptoms
- Elevated 2× running-speed component
- High axial vibration
- Bearing temperature and fatigue risk increase over time

## Likely causes
- Angular or parallel shaft misalignment
- Thermal growth
- Poor cold alignment during installation
- Piping strain or foundation movement

## Expected vibration signatures
- 2× running speed often elevated; severe cases may show multiple harmonics
- Phase across the coupling helps distinguish angular vs parallel misalignment
- May coexist with bearing-defect frequencies because misalignment drives early fatigue

## Confirm tests
- Check 1× vs 2× relationship and axial vibration
- Use phase measurements across coupling ends
- Perform alignment verification

## Fixes
- Realign shafts/couplings
- Compensate for thermal growth and piping strain
- Replace damaged bearing if secondary fatigue is confirmed

## Notes
This is essential because many 'bearing faults' are actually bearing symptoms caused by another machine problem.
