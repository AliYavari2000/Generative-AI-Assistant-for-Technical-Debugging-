---
id: BRG-006
fault_name: Surface distress
aliases:
- surface-initiated damage
- surface cracking from distress
category: damage_mechanism
bearing_components:
- raceways
- rolling_elements
observability_from_vibration: medium_high
confidence: high
tags:
- damage_mechanism
- medium_high
- raceways
- rolling_elements
- surface-initiated_damage
- surface_cracking_from_distress
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
- title: 'NI Bearings: Envelope Detection and Characteristic Frequencies'
  source: NI
  url: https://www.ni.com/docs/en-US/bundle/labview-sound-and-vibration-toolkit/page/bearings.html
---

## Symptoms
- Early high-frequency noise and impulsive activity
- Envelope indicators rise before large overall-velocity changes
- Progressive roughness and noise

## Likely causes
- Excessive load
- Improper lubrication

## Expected vibration signatures
- Envelope analysis is often more sensitive than standard velocity measures
- High-frequency resonance-excited impacts can precede gross failure

## Confirm tests
- Run demodulation/envelope analysis
- Compare high-frequency channels against baseline
- Check lubrication condition and applied load

## Fixes
- Correct load and lubrication conditions
- Inspect for early cracking and replace the bearing if damage is confirmed

## Notes
Useful as a root-cause-oriented card when the assistant sees early HF growth but cannot yet localize to one component.
