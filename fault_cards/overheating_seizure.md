---
id: BRG-014
fault_name: Overheating / seizure
aliases:
- bearing seizure
- thermal damage
- melting damage
category: damage_mechanism
bearing_components:
- all
observability_from_vibration: medium
confidence: high
tags:
- all
- bearing_seizure
- damage_mechanism
- medium
- thermal_damage
references:
- title: NSK Bearing Maintenance Guide
  source: NSK
  url: https://www.nsk.com/content/dam/nsk/am/en_us/documents/bearings-americas/Bearing-Maintenance-Guide.pdf
---

## Symptoms
- Rapid increase in noise, heat, and vibration
- Possible smearing, discoloration, or melting after teardown
- Can escalate abruptly

## Likely causes
- Poor lubrication
- Excessive load or excessive preload
- Excessive speed
- Too little internal clearance
- Water or debris ingress
- Poor shaft/housing precision or shaft bending

## Expected vibration signatures
- Rapid broadband vibration increase
- May be preceded by lubrication or preload-related roughness
- Late-stage behavior can be chaotic rather than a clean defect family

## Confirm tests
- Review temperature trend and lubrication history
- Check preload, clearance, speed, and alignment
- Inspect for discoloration, smearing, melting, or seized elements

## Fixes
- Correct lubrication method and load/speed/preload/clearance issues
- Replace the bearing and inspect surrounding components

## Notes
Useful as an alarm-level card for severe conditions where the assistant should prioritize shutdown guidance.
