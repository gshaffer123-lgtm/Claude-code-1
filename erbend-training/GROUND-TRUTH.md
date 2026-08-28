# ERBend Trainer — Ground Truth Spec

This is the single source of truth for the adjustment/taper/misalignment model in the
ERBend training app (currently deployed at erbend-training.pages.dev). Every display —
gauge strip, diagram label, step header, misal readout — must derive from ONE
computation that follows the rules below. No display may implement its own sign or
frame math.

Status legend: ✅ confirmed by Genaro (operator, owns the machine) · ❓ open question

---

## 1. The trusted component: the gauge strip

✅ The gauge strip widget is CORRECT as built, including how it handles flips and
rotation orientation. It is the reference implementation for frame mapping.

Anatomy (as rendered):

```
[ R +2T ]  | 0        F        0 |  [ L 0 ]  [pin icon]
  (blue)   | +2T      B        0 |   (red)
```

- **R button (blue, left side of strip)** = machine RIGHT = X1. Shows the signed
  taper currently spent on that machine side, in thicknesses (T).
- **L button (red, right side of strip)** = machine LEFT = X2. Same, other side.
- **F row (top, gray)** = Front; **B row (bottom, brown)** = Back. Corner numbers
  show how the taper is distributed front/back.
- The strip already accounts for part flips: after a flip, an entry addressed to a
  machine side lands on the correct PART side. This mapping is trusted and locked.

RULE: all other UI derives from this widget's internal state. If any other label
disagrees with the gauge strip, the other label is wrong by definition.

## 2. Frames: machine side vs part side

- Machine RIGHT (X1) and machine LEFT (X2) are FIXED references tied to the
  machine/tooling. They never move.
- The part's own left/right SWAP relative to the machine every time the part is
  flipped. Rotations similarly re-map which part edge faces which machine side.
- Operator taper entries are addressed in the MACHINE frame ("R -1" = machine right,
  regardless of part orientation). The app maps them into the part frame using the
  same transform the gauge strip uses — never a second, separately-written one.

## 3. Taper entry (step dialog)

Dialog contract (as shipped, kept):
- Value is in THICKNESSES (T), signed: **+ grows / − tucks in**. Halves allowed
  (0.5, −1.5, …).
- Optional side prefix: `R 4` = machine right (X1); `L 4` = machine left (X2);
  no letter = leave side alone; empty = back to automatic (T and side).

## 4. Misalignment vs X correction — TWO numbers, not one

✅ Current UI shows a single fused "Misal.X −0.017″" line. This is wrong: you cannot
adjust misal without adjusting X, but they are different quantities and must be
shown separately:

- **Misal** — the MEASURED error: where the gauged edge (e.g. "step 1's folded
  edge") actually sits vs where it should sit. Read-only. Derived from the current
  taper state via the gauge-strip transform.
- **X correction** — the INPUT: the compensation dialed into the axis to cancel the
  misal. Editable (or auto-proposed). Also expressed/tracked through the same
  transform, so the app can state exactly which side and sign the adjustment must
  go to.

RULE: lock the X-correction math to the gauge strip's frame mapping. Given a
measured misal, the app computes: which machine side (X1/X2), which sign, and how
many inches/T — and that proposal must round-trip: applying the proposed correction
must drive the displayed Misal to 0.

## 5. The diagram label bug (why the numbers "made no sense")

Observed on step 5 of program "2-12 8IN HIGH EAVE" (baseline: step-4 gauge R +3T):

| Operator entered | Gauge strip showed        | Diagram label showed |
|------------------|---------------------------|----------------------|
| `R -1`           | L +1T (mirrored, negated) | −1T                  |
| `L 2`            | R −2T (mirrored, negated) | +5T (= 3 + 2)        |
| `L -2`           | R +2T (mirrored, negated) | +1T (= 3 − 2)        |

Two different formulas are live: the gauge strip renders **−(entry) on the mirrored
side**, while the diagram label renders **baseline + entry, un-negated**. They can
never agree except by accident.

RESOLUTION: ✅ the gauge strip is the correct one. The diagram label (and the note
text under it) must be re-derived from gauge-strip state, not recomputed.

❓ OPEN: on the real machine, when the gauge shows e.g. R −2T after an `L 2` entry,
what should the diagram's big callout read — the resulting total taper on that end
of the part, or the delta just applied? (Pick one, label it, derive it.)

## 6. Step display

❓ OPEN: step 5 shows `A 5.5″ 80°` plus taper/misal, but no explicit X adjustment
field, while step 4 shows `H 6.85″`. Decide per step type which of these are shown:
target dimension, measured misal, X correction, taper — all as separate labeled
values.

## 7. Implementation requirements (when source is in this repo)

1. One pure function computes the full adjustment state:
   `computeAdjustment(programStep, entryHistory) -> { gauge: {R, L, F, B}, partFrame: {...}, misal, xCorrection, diagramCallout }`
2. Every UI element renders from that function's output. Grep-level acceptance
   check: no `+`/`-` sign logic or L/R mirroring exists anywhere in render code.
3. Unit tests pin the table in §5 (corrected expectations) plus flip/rotation
   round-trips: apply proposed X correction → misal must read 0.
4. Source of the deployed app must live in this repo (branch → Cloudflare Pages),
   so every change is versioned and this spec travels with the code.

---

## To do before implementation

- [ ] Get the app source into this repo (push from the original session, or save
      the deployed page's JS and drop it into chat).
- [ ] Genaro answers the two ❓ items above.
- [ ] Confirm baseline sign: screenshots show step-4 gauge as **R +3T**; Genaro
      described the part as "started with −3". Reconcile which is right before
      pinning tests.
