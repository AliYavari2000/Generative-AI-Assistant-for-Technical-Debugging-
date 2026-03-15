---
id: BRG-005
fault_name: Subsurface fatigue / spalling progression
aliases:
- fatigue spalling
- flaking
- rolling contact fatigue
category: damage_mechanism
bearing_components:
- inner_race
- outer_race
- rolling_elements
observability_from_vibration: medium_high
confidence: high
tags:
- damage_mechanism
- fatigue_spalling
- flaking
- inner_race
- medium_high
- outer_race
- rolling_elements
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
- title: SKF Bearing Damage and Failure Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/093168a92d25cc46/pdf_preview_medium/093168a92d25cc46_pdf_preview_medium.pdf
- &id001
  title: NASA PCoE Bearings / IMS Bearing Data Set
  source: NASA / University of Cincinnati IMS
  url: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/
- *id001
---

## Symptoms
- Gradually increasing noise and vibration
- Early high-frequency impulsive activity followed by stronger broadband vibration
- Later-stage spectrum may show a broad hump near characteristic bearing bands

## Likely causes
- Age-related rolling contact fatigue
- Higher loading than anticipated
- Incorrect fits or installation
- Ineffective or contaminated lubrication

## Expected vibration signatures
- Early stage: local-defect signatures in envelope spectrum
- Late stage: stronger velocity and acceleration response, sometimes broad humps
- Progression is gradual rather than abrupt

## Confirm tests
- Trend envelope indicators over time
- Review residual-life trend and maintenance history
- Check calculated defect frequencies plus overall vibration growth
- Confirm with inspection if practical

## Fixes
- Plan replacement before catastrophic failure
- Address the underlying load, lubrication, and fit issues
- Set alarm logic on trend rate, not just absolute level

## Notes
This card helps bridge early defect detection and maintenance planning.
