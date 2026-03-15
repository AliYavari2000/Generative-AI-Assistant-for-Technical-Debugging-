---
id: BRG-018
fault_name: Mechanical looseness near bearing
aliases:
- bearing-seat looseness
- mounting looseness
- clearance-driven looseness
category: adjacent_machine_fault
bearing_components:
- system_level
- bearing_seat
observability_from_vibration: high
confidence: high
tags:
- adjacent_machine_fault
- bearing-seat_looseness
- bearing_seat
- high
- mounting_looseness
- system_level
references:
- title: SKF Spectrum Analysis
  source: SKF
  url: https://cdn.skfmediahub.skf.com/api/public/0901d1968024acef/pdf_preview_medium/0901d1968024acef_pdf_preview_medium.pdf
---

## Symptoms
- Series of harmonics or half-harmonics of running speed
- Rattling/impacting behavior
- Vibration may be direction-dependent

## Likely causes
- Machine loose on mounting
- Cracked or broken mounting
- Loose component
- Worn bearing elements or excessive clearance at bearing seat

## Expected vibration signatures
- Three or more harmonics or half-harmonics from roughly 2× to 10× running speed
- 1× often high, with decaying harmonic family

## Confirm tests
- Inspect mountings and bearing seats
- Use FFT plus phase to distinguish from misalignment and rub
- Check for excessive clearance or wear

## Fixes
- Tighten or repair mounting/components
- Restore correct fits/clearances
- Replace bearing if wear created the looseness

## Notes
A must-have negative-control card to prevent overcalling every impulsive spectrum as a bearing race defect.
