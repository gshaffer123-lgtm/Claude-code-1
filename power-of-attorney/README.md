# Washington Durable Power of Attorney for Health Care

Generates a print-ready **Durable Power of Attorney for Health Care (DPOA-HC)** for
Washington State, drafted to track chapter 11.125 RCW (Uniform Power of Attorney Act).

`WA-DPOA-HealthCare.pdf` is the generated output: a 6-page legal instrument plus a
1-page instruction sheet that is clearly labelled as not part of the document.

## Usage

```bash
pip install reportlab
python3 make_dpoa.py WA-DPOA-HealthCare.pdf              # blank, fill in by hand
python3 make_dpoa.py filled.pdf values.json              # names typed onto the lines
```

Copy `values.example.json` to `values.json` to pre-fill names. Any key omitted or left
empty stays a blank ruled line. **Do not commit a filled-in `values.json` or a filled
PDF** — they contain personal health information.

## What the document contains

| Page | Contents |
| --- | --- |
| 1 | Principal, agent, alternate agent, durability clause |
| 2 | Effective date, scope of the agent's authority (Art. 6) |
| 3 | Life-sustaining treatment (optional), limitations, prior documents, reliance, guardian nomination |
| 4 | Principal's signature (Art. 12), execution block — notary certificate (Art. 13, Option A) |
| 5 | Two-witness attestation (Option B), agent's acceptance (Art. 14) |
| 6 | Stand-alone HIPAA authorization |
| 7 | Instruction sheet (not part of the legal document) |

## Statutory points the draft turns on

- **RCW 11.125.040 — durability is not the default.** Authority terminates on the
  principal's incapacity *unless* the document says otherwise, so Article 4 carries the
  express words "This power of attorney shall not be affected by my disability or
  incapacity."
- **RCW 11.125.050 — execution.** Signed and dated by the principal, and the signature
  either acknowledged before a notary **or** attested by two competent witnesses. The two
  routes are alternatives; Article 13 presents them as Option A and Option B with an
  instruction to complete only one.
- **Witness disqualification (same section).** A witness may not be related to the
  principal *or to the agent* by blood, marriage, or state registered domestic
  partnership, and may not be the principal's home care provider or a care provider at an
  adult family home or long-term care facility where the principal resides. Because the
  agent is typically a family member, this usually rules out the whole family — the form
  warns about it in the execution block and again on the instruction sheet.
- **RCW 11.125.400 — health care authority.** A general grant of health care authority
  lets the agent give informed consent and act as the principal's HIPAA personal
  representative. Article 6 grants it generally and then enumerates specifics.
- **RCW 7.70.065 — surrogate consent.** Sets the priority order of people who may consent
  for a patient who cannot, with an agent under a durable power of attorney ranking just
  below a court-appointed guardian. Covered on the instruction sheet as the fallback if
  the document is not signed in time.

Not legal advice; no attorney-client relationship. For anything beyond a near-term
procedure, have a Washington attorney review it.

## Implementation notes

The build runs twice. The first pass is a throwaway render into a `BytesIO` that records
the total page count and, via a zero-size `Marker` flowable, the page where the
instruction sheet starts. The second pass uses those numbers so the legal instrument and
the instruction sheet each carry their own page numbering, and the "Principal's initials"
footer appears only on pages of the legal instrument.
