"""Builds the sample dictionaries (one JSON per persona), the blank schema, and renders every PDF.

    python3 build_samples.py

Outputs
    samples/applicant_01.json   samples/applicant_02.json   samples/blank_schema.json
    output/application_01.pdf   output/application_02.pdf   output/blank_template.pdf
"""
import json
import os

from persona_01 import PERSONA_01
from persona_02 import PERSONA_02
from render_form import Form
from schema import blank

HERE = os.path.dirname(os.path.abspath(__file__))
PERSONAS = {"01": PERSONA_01, "02": PERSONA_02}


def merge(base, over):
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            merge(base[k], v)
        else:
            base[k] = v
    return base


def build(persona):
    full = merge(blank(), persona)
    b = blank()["applicant"]["financial"]
    fin = full["applicant"]["financial"]
    for key in ("bank_accounts", "existing_loans"):
        while len(fin[key]) < len(b[key]):
            fin[key].append(dict(b[key][0]))
    return full


def render(data, path):
    form = Form(data, path)
    form.render()
    for w in form.warnings:
        print("  WARN:", path, w)
    return form


def main():
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    blank_data = blank()
    with open(os.path.join(HERE, "samples", "blank_schema.json"), "w") as f:
        json.dump(blank_data, f, indent=2)
    render(blank_data, os.path.join(HERE, "output", "blank_template.pdf"))
    for pid, persona in PERSONAS.items():
        data = build(persona)
        with open(os.path.join(HERE, "samples", f"applicant_{pid}.json"), "w") as f:
            json.dump(data, f, indent=2)
        render(data, os.path.join(HERE, "output", f"application_{pid}.pdf"))
        print("built persona", pid)


if __name__ == "__main__":
    main()
