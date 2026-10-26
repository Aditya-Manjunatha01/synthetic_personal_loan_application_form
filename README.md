# Personal Loan Application Form: synthetic template

Renders a typed, filled personal loan application form (4-page A4 PDF) from a JSON data dictionary.
Bank name/tagline are placeholders ("bank logo" / "bank tagline") set in `form_meta`; all static text is bank-neutral.

## Layout
- `schema.py`        blank dictionary with every key (`blank()`)
- `form_text.py`     all static printed text (declarations, terms, FATCA text, charges)
- `render_form.py`   reportlab renderer: `python3 render_form.py in.json out.pdf`
- `persona_01.py`    Rohan Suresh Iyer: NEW to bank (customer ID / account no empty, "Saving Account = N"), salaried, India-only tax resident (FATCA table empty)
- `persona_02.py`    Ananya Venkat Shetty: EXISTING customer (customer ID + account no filled), self-employed consultant, tax resident in India and UK (FATCA table filled), co-applicant, "NA" convention in sourcing fields
- `build_samples.py` merges each persona onto `blank()`, writes JSON + PDF
- `samples/`         applicant_01.json, applicant_02.json, blank_schema.json
- `output/`          application_01.pdf, application_02.pdf, blank_template.pdf
- `fonts/`           script font used for signature placeholders

## Usage
    pip install reportlab
    python3 build_samples.py                                   # rebuild everything
    python3 render_form.py samples/applicant_02.json out.pdf   # render one JSON

## Conventions
- Tick boxes: boolean per option (true = filled black box, false = empty box)
- Text: uppercase typed; dates ISO `YYYY-MM-DD` (rendered DDMMYYYY); amounts integers; phone/PIN/account numbers digit strings
- Blocks: `form_meta`, `applicant` (customer answers), `bank_use` (official-use fields)
- To add a persona: create `persona_03.py` with a `PERSONA_03` dict and register it in `build_samples.py`
