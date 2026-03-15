# Unbalance-induced bearing loading

| Field | Value |
|-------|-------|
| **ID** | BRG-017 |
| **Category** | adjacent_machine_fault |
| **Observability from Vibration** | high |
| **Diagnostic Confidence** | high |
| **Affected Components** | system_level |
| **Aliases** | rotor unbalance affecting bearing | 1x unbalance |

## Symptoms
- Dominant 1× RPM vibration in radial direction
- Vibration amplitude proportional to speed squared
- Steady phase angle at 1× RPM

## Likely Causes
- Mass loss from erosion, fouling, or component detachment
- Rotor bow from thermal gradient
- Assembly error leaving residual unbalance

## Vibration / Diagnostic Signatures
- Single dominant peak at 1× RPM in radial spectrum
- Stable 1× phase angle corresponding to heavy spot location

## Confirmatory Tests
- 1× amplitude and phase tracking during run-up and coast-down (Bode plot)
- Trial-weight balancing response verification
- Rotor inspection for mass loss or buildup

## Recommended Fixes
- Perform in-situ single-plane or two-plane balancing
- Correct rotor bow via controlled thermal cycle or straightening
- Address root cause of mass change (erosion protection, cleaning schedule)

## References
1. ISO 1940-1 "Balance quality requirements of rigid rotors"

---
**Tags:** `1x_unbalance`, `adjacent_machine_fault`, `high`, `rotor_unbalance_affecting_bearing`, `system_level`
