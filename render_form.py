#!/usr/bin/env python3
"""Renders the 4-page personal loan application form from a JSON dictionary.

Usage: python3 render_form.py sample_applicant.json out.pdf

Conventions (see the field-map doc):
  * text -> typed into per-character boxes where the form shows boxes
  * boolean tick keys -> box filled solid black when true, empty white box when false
  * dates are ISO strings, drawn as DDMMYYYY in boxes
  * signatures are typed placeholders drawn in a script font
  * static clauses live in form_text.py; {bank_name}/{bank_website} come from form_meta
"""
import json
import os
import sys

from reportlab.graphics.barcode import code128
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import form_text as FT

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 595.28, 841.89
LM, RM = 34.0, 561.0
MAROON = Color(0.58, 0.10, 0.26)
INK = Color(0.06, 0.10, 0.42)          # typed values
GREY = Color(0.86, 0.86, 0.86)
MIDGREY = Color(0.62, 0.62, 0.62)
LGREY = Color(0.93, 0.93, 0.93)

LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Body", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", LIB + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("BodyI", LIB + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sign", os.path.join(HERE, "fonts", "MrsSaintDelafield-Regular.ttf")))


DJV = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("RupeeR", DJV + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("RupeeB", DJV + "DejaVuSans-Bold.ttf"))
RUPEE = "₹"


def _segments(s, font):
    """Split on the rupee sign, which Liberation Sans lacks; draw it from DejaVu."""
    if RUPEE not in s:
        return [(s, font)]
    out = []
    for part in s.split(RUPEE):
        out.append((part, font))
        out.append((RUPEE, "RupeeB" if font == "BodyB" else "RupeeR"))
    return [(p, f) for p, f in out[:-1] if p]


def sw(s, font, size):
    return sum(pdfmetrics.stringWidth(p, f, size) for p, f in _segments(s, font))


class Form:
    def __init__(self, data, path):
        self.d = data
        self.a = data["applicant"]
        self.b = data["bank_use"]
        self.meta = data["form_meta"]
        self.c = canvas.Canvas(path, pagesize=(W, H))
        self.c.setTitle(self.meta.get("form_title", "Application"))
        self.warnings = []
        self.page_no = 1

    # ------------------------------------------------------------------ basics
    def T(self, s):
        return (s.replace("{bank_name}", self.meta["bank_name"])
                 .replace("{bank_website}", self.meta["bank_website"]))

    def warn(self, msg):
        self.warnings.append(msg)

    def txt(self, x, y, s, size=6.3, font="Body", color=black, anchor="l"):
        c = self.c
        c.setFillColor(color)
        w = sw(s, font, size)
        if anchor == "c":
            x -= w / 2
        elif anchor == "r":
            x -= w
        for part, f in _segments(s, font):
            c.setFont(f, size)
            c.drawString(x, H - y, part)
            x += pdfmetrics.stringWidth(part, f, size)

    def rect(self, x, y, w, h, fill=None, stroke=True, lw=0.45, color=black):
        c = self.c
        c.setLineWidth(lw)
        c.setStrokeColor(color)
        if fill is not None:
            c.setFillColor(fill)
        c.rect(x, H - y - h, w, h, stroke=1 if stroke else 0, fill=1 if fill is not None else 0)

    def line(self, x1, y1, x2, y2, lw=0.45, color=black, dash=None):
        c = self.c
        c.setLineWidth(lw)
        c.setStrokeColor(color)
        if dash:
            c.setDash(*dash)
        c.line(x1, H - y1, x2, H - y2)
        if dash:
            c.setDash()

    def label(self, x, y, s, size=6.3, bold=False, color=black):
        """y is the TOP of a 10.5pt field row; text is baseline-aligned inside it."""
        self.txt(x, y + 7.6, s, size, "BodyB" if bold else "Body", color)
        return x + sw(s, "BodyB" if bold else "Body", size)

    # ------------------------------------------------------------- field widgets
    def comb(self, x, y, n, text, cw=8.5, ch=10.5, size=7.2, align="l", name=""):
        text = str(text if text is not None else "").upper()
        if len(text) > n:
            self.warn(f"overflow in {name or 'comb'}: '{text}' > {n} boxes")
            text = text[:n]
        for i in range(n):
            self.rect(x + i * cw, y, cw, ch, lw=0.4)
        start = 0 if align == "l" else n - len(text)
        for i, chh in enumerate(text):
            self.txt(x + (start + i) * cw + cw / 2, y + ch - 2.7, chh, size, "BodyB", INK, "c")
        return x + n * cw

    def box(self, x, y, w, text, h=10.5, size=7.2, name=""):
        self.rect(x, y, w, h, lw=0.4)
        self.fit_text(x + 2.5, y + h - 2.7, w - 5, str(text or "").upper(), size, name)
        return x + w

    def uline(self, x, y, w, text, size=7.0, h=10.5, name="", upper=True):
        self.line(x, y + h, x + w, y + h, lw=0.4)
        s = str(text if text is not None else "")
        s = s.upper() if upper else s
        self.fit_text(x + 1.5, y + h - 2.2, w - 3, s, size, name)
        return x + w

    def fit_text(self, x, base, w, s, size, name=""):
        if not s:
            return
        sz = size
        while sw(s, "BodyB", sz) > w and sz > 4.4:
            sz -= 0.2
        if sw(s, "BodyB", sz) > w:
            self.warn(f"text too wide in {name or 'field'}: '{s}'")
        self.txt(x, base, s, sz, "BodyB", INK)

    def tick(self, x, y, on, s=6.6):
        self.rect(x, y, s, s, fill=black if on else white, lw=0.5)
        return x + s

    def tick_label(self, x, y, on, label, size=6.1, s=6.6):
        self.tick(x, y + 1.0, on, s)
        self.txt(x + s + 2.2, y + 7.2, label, size)
        return x + s + 2.2 + sw(label, "Body", size)

    def ticks_row(self, x, y, items, size=6.1, gap=7.5):
        for on, lab in items:
            x = self.tick_label(x, y, on, lab, size) + gap
        return x

    def date_boxes(self, x, y, iso, cw=8.5, ch=10.5, name="date"):
        digits = ""
        if iso:
            yy, mm, dd = iso.split("-")
            digits = dd + mm + yy
        return self.comb(x, y, 8, digits, cw, ch, name=name)

    @staticmethod
    def num(v, zero=False):
        if v in (None, ""):
            return ""
        if isinstance(v, float):
            return ("%g" % v)
        if v == 0 and not zero:
            return ""
        return str(v)

    def sign_text(self, x, y, w, h, s, size=None):
        if not s:
            return
        sz = size or min(18, h * 0.62)
        while sw(s, "Sign", sz) > w - 6 and sz > 8:
            sz -= 0.5
        self.txt(x + 4, y + h * 0.62, s, sz, "Sign", INK)

    def banner(self, y, text, h=11.0):
        self.rect(LM, y, RM - LM, h, fill=MAROON, stroke=False)
        self.txt((LM + RM) / 2, y + h - 3.1, text, 7.2, "BodyB", white, "c")
        return y + h

    def flow(self, x, y, w, tokens, size=5.6, lead=None, font="Body", fields=None):
        """Greedy word-wrap. tokens: str or ('f', key_or_text, width). Returns y after the block."""
        lead = lead or size * 1.24
        items = []
        for t in tokens:
            if isinstance(t, str):
                for wd in self.T(t).split(" "):
                    if wd:
                        items.append(("w", wd, sw(wd, font, size)))
            else:
                items.append(("f", t[1], t[2]))
        space = sw(" ", font, size)
        lines = [[]]
        cur = 0.0
        for it in items:
            add = it[2] + (space if lines[-1] else 0)
            if cur + add > w and lines[-1]:
                lines.append([])
                cur = 0.0
                add = it[2]
            lines[-1].append(it)
            cur += add
        yy = y
        for ln in lines:
            xx = x
            for it in ln:
                if it[0] == "w":
                    self.txt(xx, yy + size, it[1], size, font)
                else:
                    self.line(xx, yy + size + 0.6, xx + it[2], yy + size + 0.6, lw=0.4)
                    if it[1]:
                        self.txt(xx + 1.5, yy + size - 0.4, str(it[1]), size + 0.8, "BodyB", INK)
                xx += it[2] + space
            yy += lead
        return yy

    def para(self, x, y, w, text, size=5.6, lead=None, font="Body"):
        return self.flow(x, y, w, [text], size, lead, font)

    def numbered(self, x, y, w, items, size=5.5, indent=9.0, gap=0.6):
        for i, t in enumerate(items, 1):
            self.txt(x, y + size, f"{i}.", size)
            y = self.flow(x + indent, y, w - indent, [t], size) + gap
        return y

    def photo_box(self, x, y, w, h, placeholder):
        self.rect(x, y, w, h, lw=0.5, color=MIDGREY)
        if placeholder:
            self.rect(x + 14, y + 14, w - 28, h - 34, fill=LGREY, stroke=False)
            self.txt(x + w / 2, y + h / 2 + 2, placeholder, 8, "BodyB", MIDGREY, "c")
        self.txt(x + w / 2, y + 8, "Applicant", 6.5, "BodyB", MIDGREY, "c")
        self.txt(x + w / 2, y + h - 12, "Please sign across the", 5.2, "Body", MIDGREY, "c")
        self.txt(x + w / 2, y + h - 6, "photograph / Passport Size Photograph", 5.2, "Body", MIDGREY, "c")

    def sig_box(self, x, y, w, h, text, caption="Signature"):
        self.rect(x, y, w, h, lw=0.5, color=MIDGREY)
        self.sign_text(x, y, w, h, text)
        self.txt(x + w - 3, y + h - 2.5, caption, 5.2, "Body", MIDGREY, "r")

    def footer(self):
        self.txt(W / 2, H - 16, str(self.page_no), 6.5, "Body", black, "c")

    def next_page(self):
        self.footer()
        self.c.showPage()
        self.page_no += 1

    # ------------------------------------------------------------ address blocks
    def addr_lines(self, y, title, a, sub=None, rows3=True):
        self.label(LM, y, title, 6.3, True)
        if sub:
            self.txt(LM, y + 15.5, sub, 4.8, "Body", MIDGREY)
        x0 = 134
        self.comb(x0, y, 50, a["line_1"], name=f"{title} line1")
        y += 13
        self.comb(x0, y, 50, a["line_2"], name=f"{title} line2")
        y += 13
        self.comb(x0, y, 20, a["line_3"], name=f"{title} line3")
        self.label(308, y, "Landmark")
        self.comb(346, y, 12, a["landmark"], name=f"{title} landmark")
        self.label(451, y, "*City")
        self.comb(476, y, 10, a["city"], name=f"{title} city")
        return y + 13

    def addr_loc(self, y, a, pin_label="*Pin Code"):
        self.label(LM, y, "State")
        self.comb(134, y, 14, a["state"], name="state")
        self.label(262, y, "*Country")
        self.comb(292, y, 14, a["country"], name="country")
        self.label(418, y, pin_label)
        self.comb(452, y, 6, a["pincode"], name="pincode")
        return y + 13

    def addr_phone(self, y, a, mailing_key="is_mailing_address"):
        self.label(LM, y, "*Mobile Number")
        self.comb(134, y, 10, a["mobile_number"], name="mobile")
        self.label(228, y, "*Phone Number")
        self.comb(276, y, 11, a["phone_number"], name="phone")
        self.label(386, y, "*Mailing Address")
        self.tick(452, y + 1.5, a[mailing_key])
        return y + 13

    # ===================================================================== PAGE 1
    def page1(self):
        a, b, m = self.a, self.b, self.meta
        # header band with logo + tagline placeholders
        self.rect(0, 22, 178, 54, fill=MAROON, stroke=False)
        self.txt(30, 50, m["bank_name"], 17, "BodyB", white)
        self.txt(30, 63, m["bank_tagline"], 6.8, "Body", white)
        parts = m["form_title"].split(" ", 2)
        self.txt(196, 42, " ".join(parts[:2]), 15.5, "BodyB", MAROON)
        self.txt(196, 59, parts[2] if len(parts) > 2 else "", 15.5, "BodyB", MAROON)
        bc = code128.Code128(m["form_code"], barHeight=11, barWidth=0.62, quiet=False)
        bc.drawOn(self.c, 196, H - 75)
        self.txt(196 + bc.width + 4, 74.5, m["form_code"], 5.5, "Body", MIDGREY)
        # serial box
        self.rect(405, 22, 156, 48, lw=0.7, color=MAROON)
        self.txt(411, 33, "Serial No.", 8.5, "Body", MIDGREY)
        self.txt(483, 60, b["serial_no"], 11, "BodyB", INK, "c")
        self.txt(RM, 79, "*Mandatory Field", 5.3, "BodyB", black, "r")

        y = 86
        ec = a["existing_customer"]
        self.label(LM, y, "If existing " + m["bank_name"] + " Customer, Please Provide")
        self.label(196, y, "*Customer ID")
        self.comb(240, y, 12, ec["customer_id"], name="customer id")
        self.label(458, y, "Date")
        self.date_boxes(RM - 68, y, a["application_date"], name="application date")
        # note: date box starts after label; label sits left of boxes
        y += 14
        self.label(LM, y, "Saving Account")
        self.tick_label(90, y, ec["savings_account_yes"], "Y")
        self.tick_label(112, y, ec["savings_account_no"], "N")
        self.label(196, y, "*Account no.")
        self.comb(240, y, 16, ec["account_no"], name="account no")
        y += 14
        lt = a["loan_type"]
        self.label(LM, y, "Loan Type", 6.3, True)
        self.tick_label(90, y, lt["pre_approved"], "Pre Approved")
        self.tick_label(200, y, lt["topup_with_closure"], "Topup (With closure of existing loan)")
        self.tick_label(372, y, lt["parallel"], "Parallel (In addition to existing loan)")
        y += 13
        self.tick_label(90, y, lt["premium_scheme"], "Premium Scheme")
        xx = self.label(200, y, "External BT Topup / Ext BT Loan A/c no:")
        self.box(xx + 4, y, RM - xx - 4, lt["external_bt_loan_account_no"], name="ext bt")
        y += 14
        self.txt(LM, y + 5, "PLEASE FILL THIS FORM IN BLOCK CAPITAL LETTERS ONLY", 5.4, "BodyB")
        y = self.banner(y + 8, "Personal Details")

        # ---- names
        pd = a["personal_details"]
        y += 3
        x_pre, x_fn, x_mn, x_ln = 134, 160, 283, 372
        for xx, cap in ((x_pre, "Prefix"), (x_fn, "First Name"), (x_mn, "Middle Name"), (x_ln, "Last Name")):
            self.txt(xx, y + 4, cap, 4.8, "Body", MIDGREY)
        y += 5
        for lab, sub, key in (("*Name", "(Same As ID proof)", "name_as_per_id"),
                              ("*Name", "(as per PAN card)", "name_as_per_pan"),
                              ("*Maiden Name", "(if any)", "maiden_name"),
                              ("Father's Name", "", "father_name"),
                              ("*Mother's Maiden Name", "", "mother_maiden_name")):
            nm = pd[key]
            self.label(LM, y, lab)
            if sub:
                self.txt(LM + sw(lab, "Body", 6.3) + 3, y + 7.4, sub, 4.6, "Body", MIDGREY)
            self.comb(x_pre, y, 1, "", cw=22)
            self.txt(x_pre + 11, y + 7.8, nm["prefix"].upper(), 6.6, "BodyB", INK, "c")
            self.comb(x_fn, y, 14, nm["first_name"], name=key + " first")
            self.comb(x_mn, y, 10, nm["middle_name"], name=key + " middle")
            self.comb(x_ln, y, 14, nm["last_name"], name=key + " last")
            y += 13
        y += 1
        # ---- present address
        pa = a["present_address"]
        y = self.addr_lines(y, "*Residence Address", pa, "(Present Address)")
        y = self.addr_loc(y, pa)
        y = self.addr_phone(y, pa)
        self.label(LM, y, "*E-mail ID")
        self.box(134, y, 256, pd["email"], name="email")
        self.label(398, y, "*Email statement")
        self.tick(466, y + 1.5, pd["email_statement"])
        y += 13
        self.label(LM, y, "*No. of Years In the current residence")
        self.comb(158, y, 2, self.num(pa["years_at_residence"], True), align="r", name="yrs res")
        self.label(177, y, "Years")
        self.comb(196, y, 2, self.num(pa["months_at_residence"], True), align="r", name="mths res")
        self.label(215, y, "Months")
        self.label(262, y, "*No. of Years in the city")
        self.comb(340, y, 2, self.num(pa["years_in_city"], True), align="r", name="yrs city")
        self.label(359, y, "Years")
        self.comb(378, y, 2, self.num(pa["months_in_city"], True), align="r", name="mths city")
        self.label(397, y, "Months")
        y += 13
        o = pa["ownership"]
        self.label(LM, y, "*Residence Ownership")
        self.ticks_row(112, y, [(o["self_owned"], "Self Owned"), (o["parental"], "Parental"),
                                (o["owned_mortgaged"], "Owned-Mortgaged"), (o["company_provided"], "Co. Provided"),
                                (o["paying_guest"], "Paying Guest"), (o["rental"], "Rental"),
                                (o["relative"], "Relative")])
        y += 13
        cs = pd["constitution"]
        self.label(LM, y, "*Constitution")
        self.ticks_row(112, y, [(cs["resident_indian"], "Resident Indian"),
                                (cs["non_resident_indian"], "Non-Resident Indian"),
                                (cs["foreign_national"], "Foreign Nationals"),
                                (cs["overseas_citizen_of_india"], "Overseas Citizen of India"),
                                (cs["person_of_indian_origin"], "Person of Indian Origin")])
        y += 13
        nat = pd["nationality"]
        self.label(LM, y, "*Nationality")
        self.tick_label(112, y, nat["indian"], "Indian")
        self.tick_label(158, y, nat["other_selected"], "Other")
        self.uline(188, y, 70, nat["other_text"], name="nationality other")
        self.txt(262, y + 7.4, "(Kindly mention nationality, if apart from Indian)", 4.8, "Body", MIDGREY)
        self.label(430, y, "*PEP")
        self.tick_label(448, y, pd["pep_yes"], "YES")
        self.tick_label(480, y, pd["pep_no"], "NO")
        y += 16

        # ---- permanent address
        pm = a["permanent_address"]
        y = self.addr_lines(y, "*Resident Address", pm, "(Permanent Address)")
        y = self.addr_loc(y, pm, "*Pincode")
        y = self.addr_phone(y, pm)
        o = pm["ownership"]
        self.label(LM, y, "*Residence Ownership")
        self.ticks_row(112, y, [(o["self_owned"], "Self Owned"), (o["parental"], "Parental"),
                                (o["owned_mortgaged"], "Owned-Mortgaged"), (o["rental"], "Rental"),
                                (o["relative"], "Relative")])
        y += 14

        # ---- community, category, ...
        cm = pd["community"]
        self.label(LM, y, "*Community")
        xx = self.ticks_row(112, y, [(cm["hindu"], "Hindu"), (cm["muslim"], "Muslim"), (cm["buddhist"], "Buddhist"),
                                     (cm["christian"], "Christians"), (cm["sikh"], "Sikh"),
                                     (cm["zoroastrian"], "Zoroastrian"), (cm["jain"], "Jain"),
                                     (cm["parsi"], "Parsi"), (cm["others"], "Others")], gap=5.5)
        self.box(xx, y, RM - xx, cm["others_specify"], name="community specify")
        if not cm["others_specify"]:
            self.txt(xx + 3, y + 7.4, "Specify", 5, "Body", MIDGREY)
        y += 13
        ct = pd["category"]
        self.label(LM, y, "Category")
        xx = self.ticks_row(112, y, [(ct["general"], "General"), (ct["obc"], "Other Backward Castes (OBC)"),
                                     (ct["scheduled_caste"], "Schedule Castes"),
                                     (ct["scheduled_tribe"], "Schedule Tribes"), (ct["others"], "Others")], gap=6)
        self.box(xx, y, RM - xx, ct["others_specify"], name="category specify")
        if not ct["others_specify"]:
            self.txt(xx + 3, y + 7.4, "Specify", 5, "Body", MIDGREY)
        y += 13
        g, st = pd["gender"], pd["status"]
        self.label(LM, y, "*Gender", 6.3, True)
        self.ticks_row(112, y, [(g["male"], "Male"), (g["female"], "Female"), (g["third_gender"], "Third Gender")])
        self.label(262, y, "*Status", 6.3, True)
        self.ticks_row(294, y, [(st["resident"], "Res"), (st["nri"], "NRI"), (st["pio"], "PIO"), (st["oci"], "OCI"),
                                (st["foreign_national"], "Foreign National")])
        y += 13
        self.label(LM, y, "*Date of Birth")
        self.date_boxes(112, y, pd["dob_as_per_id"], name="dob id")
        self.txt(182, y + 7.4, "(Same As ID proof)", 4.8, "Body", MIDGREY)
        self.date_boxes(262, y, pd["dob_as_per_pan"], name="dob pan")
        self.txt(332, y + 7.4, "(as per PAN card)", 4.8, "Body", MIDGREY)
        y += 13
        ms = pd["marital_status"]
        self.label(LM, y, "*Marital Status")
        self.ticks_row(112, y, [(ms["married"], "Married"), (ms["single"], "Single"), (ms["others"], "Others")])
        self.label(262, y, "*No. of Dependents")
        self.comb(330, y, 2, self.num(pd["dependents"], True), align="r", name="dependents")
        self.label(358, y, "*Person with Disability")
        self.tick_label(432, y, pd["disability_yes"], "Y")
        self.tick_label(452, y, pd["disability_no"], "N")
        y += 13
        ed = pd["education"]
        self.label(LM, y, "*Education")
        self.ticks_row(112, y, [(ed["matriculate"], "Matriculate"), (ed["undergraduate"], "Undergraduate"),
                                (ed["graduate"], "Graduate"), (ed["postgraduate"], "Postgraduate"),
                                (ed["professional"], "Professional"), (ed["others"], "Others")])
        y += 13
        em = a["employment"]
        self.label(LM, y, "*Occupation")
        self.ticks_row(112, y, [(em["occupation"]["salaried"], "Salaried"),
                                (em["occupation"]["consultant"], "Consultant")])
        self.label(204, y, "Designation")
        self.comb(244, y, 15, em["designation"], name="designation")
        self.label(376, y, "Department")
        self.comb(418, y, 10, em["department"], name="department")
        y += 13
        ot = em["organisation_type"]
        self.label(LM, y, "If Salaried,")
        self.ticks_row(112, y, [(ot["pvt_ltd"], "Pvt Ltd"), (ot["public_ltd"], "Public Ltd"),
                                (ot["proprietorship"], "Proprietorship"), (ot["partnership_firm"], "Partnership firm"),
                                (ot["public_sector"], "Public Sector"), (ot["government"], "Government"),
                                (ot["mnc"], "MNC")])
        y += 13
        self.tick_label(112, y, ot["trust_association_society_club"], "Trust/Association/Society/Club")
        self.label(262, y, "*Nature of Employment")
        self.uline(336, y, 225, em["nature_of_employment"], name="nature of employment")
        self.txt(RM, y + 17.5, "(As per the type of organization selected above, mention the details of profession "
                               "example: Director/Banker/Agent)", 4.4, "Body", MIDGREY, "r")
        y += 24

        # ---- CKYC grid
        y = self.ckyc_grid(y)
        # ---- police / company / promo
        pdf = a["police_defense"]
        y += 4
        xx = self.label(LM, y, "For Police Defense Employees", 6.0, True) + 5
        for lab, key, w in (("Belt No.", "belt_no", 56), ("PIS no. / Employee no.", "pis_or_employee_no", 70),
                            ("Rank", "rank", 52), ("Regiment/Unit Details", "regiment_unit_details", 70)):
            xx = self.label(xx, y, lab, 6.0) + 2
            xx = self.uline(xx, y, w, pdf[key], size=6.4, name=key) + 6
        y += 13
        self.label(LM, y, "Company Code")
        self.comb(94, y, 8, b_get(self.b, "company_code"), name="company code")
        self.label(172, y, "Name of Employer:")
        self.uline(236, y, RM - 236, em["employer_name"], name="employer name")
        y += 13
        pr = self.b["promo"]
        self.label(LM, y, "Promo Code:")
        self.uline(76, y, 120, pr["code"], name="promo code")
        self.ticks_row(210, y, [(pr["seven_year_tenure"], "1) 7-year tenure"), (pr["regional_police"], "2) Regional Police"),
                                (pr["police"], "3) Police"), (pr["premium_scheme"], "4) Premium Scheme"),
                                (pr["credit_card_balance_transfer"], "5) Credit Card Balance Transfer")], gap=5)
        y += 13
        if y > H - 24:
            self.warn(f"page 1 content runs to y={y:.0f}")
        self.next_page()

    def ckyc_grid(self, y):
        ck = self.a["ckyc"]
        x_lab, x1, x2, x3, x4 = LM, 232.0, 284.0, 336.0, 388.0
        rh = 12.0
        # title row
        self.rect(LM, y, RM - LM, 11.5, fill=LGREY, lw=0.5)
        self.txt((LM + RM) / 2, y + 8.3, "*CKYC Details (Please mention Yes/No, whichever is applicable)", 6.8,
                 "BodyB", black, "c")
        y += 11.5
        # header row
        heads = [(x_lab, x1, "Document"), (x1, x2, "Proof of Identity"), (x2, x3, "Present Address"),
                 (x3, x4, "Permanent Address"), (x4, RM, "Document Number (if any)")]
        for xa, xb, t in heads:
            self.rect(xa, y, xb - xa, 11.5, fill=LGREY, lw=0.45)
            self.txt((xa + xb) / 2, y + 8, t, 5.0 if len(t) > 14 and xb - xa < 60 else 5.6, "BodyB", black, "c")
        y += 11.5

        def yn_cell(xa, xb, cell):
            self.rect(xa, y, xb - xa, rh, lw=0.45, fill=None if cell is not None else Color(0.72, 0.72, 0.72))
            if cell is None:
                return
            mid = xa + 6
            self.tick_label(mid, y + 2.2, cell["yes"], "Y", 5.8, 6.0)
            self.tick_label(mid + 22, y + 2.2, cell["no"], "N", 5.8, 6.0)

        rows = [
            ("aadhaar", "Aadhaar", ("poi", "pa", "perm"), "aadhaar"),
            ("voter_id", "Voter ID", ("poi", "pa", "perm"), "plain"),
            ("pan", "*PAN", ("poi",), "plain"),
            ("passport", "Passport", ("poi", "pa", "perm"), "dates"),
            ("driving_license", "Driving License", ("poi", "pa", "perm"), "dates"),
            ("utility_bill", "Utility Bill (E Bill, Telephone / postpaid bill, Gas bill & Water Bill)", ("pa",), "plain"),
            ("npr_letter", "Letter Issued by National Population Register", ("perm",), "plain"),
            ("pension_order", "Pension/Family payment orders", ("pa",), "plain"),
            ("narega", "NAREGA", ("pa", "perm"), "plain"),
            ("internal_banking", "Internal banking (existing customer)", ("pa", "perm"), "none"),
            ("ckyc_identifier", "CKYC Identifier", ("perm",), "plain"),
        ]
        colkey = {"poi": "proof_of_identity", "pa": "present_address", "perm": "permanent_address"}
        for key, lab, cols, kind in rows:
            rec = ck[key]
            self.rect(x_lab, y, x1 - x_lab, rh, lw=0.45)
            size = 5.8 if len(lab) < 40 else 4.7
            self.txt(x_lab + 3, y + 8.4, lab, size)
            if kind == "dates":
                lw_ = sw(lab, "Body", size)
                dx = x_lab + 3 + lw_ + 5
                self.txt(dx, y + 8.2, "Issue:", 4.6, "Body", MIDGREY)
                self.comb_mini(dx + 14, y + 2.0, rec["date_of_issue"])
                dx2 = dx + 14 + 8 * 5.4 + 5
                self.txt(dx2, y + 8.2, "Expiry:", 4.6, "Body", MIDGREY)
                self.comb_mini(dx2 + 16, y + 2.0, rec["date_of_expiry"])
            for col, (xa, xb) in zip(("poi", "pa", "perm"), ((x1, x2), (x2, x3), (x3, x4))):
                yn_cell(xa, xb, rec[colkey[col]] if col in cols else None)
            # document number cell
            self.rect(x4, y, RM - x4, rh, lw=0.45)
            if kind == "none":
                self.rect(x4, y, RM - x4, rh, fill=Color(0.72, 0.72, 0.72), lw=0.45)
            elif kind == "aadhaar":
                num = str(rec["document_number"] or "")[-4:]
                n = 12
                cw = 10.4
                for i in range(n):
                    grey = i < 8
                    self.rect(x4 + 3 + i * cw, y + 1.5, cw, rh - 3, fill=Color(0.35, 0.35, 0.35) if grey else white, lw=0.4)
                for i, chh in enumerate(num):
                    self.txt(x4 + 3 + (8 + i) * cw + cw / 2, y + rh - 3.2, chh, 6.6, "BodyB", INK, "c")
            else:
                self.comb(x4 + 3, y + 1.5, 16, rec.get("document_number", ""), cw=10.4, ch=rh - 3, size=6.4,
                          name=key + " number")
            y += rh
        self.txt(LM, y + 7, "*Anyone of the OVD document details must be provided.", 5.4, "BodyB")
        return y + 10

    def comb_mini(self, x, y, iso):
        digits = ""
        if iso:
            yy, mm, dd = iso.split("-")
            digits = dd + mm + yy
        for i in range(8):
            self.rect(x + i * 5.4, y, 5.4, 8.0, lw=0.35)
        for i, chh in enumerate(digits):
            self.txt(x + i * 5.4 + 2.7, y + 6.3, chh, 5.0, "BodyB", INK, "c")

    # ===================================================================== PAGE 2
    def page2(self):
        a = self.a
        em = a["employment"]
        of = em["office_address"]
        y = 26.0
        # office address
        self.rect(LM, y + 1.5, 6, 6, fill=black, lw=0.3)
        self.txt(LM + 9, y + 7.6, "Office Address", 6.3, "BodyB")
        x0 = 134
        self.comb(x0, y, 50, of["line_1"], name="office line1")
        y += 13
        self.comb(x0, y, 50, of["line_2"], name="office line2")
        y += 13
        self.comb(x0, y, 20, of["line_3"], name="office line3")
        self.label(308, y, "Landmark")
        self.comb(346, y, 12, of["landmark"], name="office landmark")
        self.label(451, y, "*City")
        self.comb(476, y, 10, of["city"], name="office city")
        y += 13
        y = self.addr_loc(y, of, "*Pincode")
        y = self.addr_phone(y, of)
        self.label(LM, y, "E-mail ID (Office)")
        self.box(134, y, 256, em["office_email"], name="office email")
        self.label(398, y, "*Email statement")
        self.tick(466, y + 1.5, em["office_email_statement"])
        y += 13
        self.label(LM, y, "*Period In Current Employment/Business")
        self.comb(158, y, 2, self.num(em["years_in_current_employment"], True), align="r")
        self.label(177, y, "Years")
        self.comb(194, y, 2, self.num(em["months_in_current_employment"], True), align="r")
        self.label(213, y, "Months")
        self.label(244, y, "Total Employment Period")
        self.comb(324, y, 2, self.num(em["total_employment_years"], True), align="r")
        self.label(343, y, "Years")
        self.comb(362, y, 2, self.num(em["total_employment_months"], True), align="r")
        self.label(381, y, "Months")
        self.label(414, y, "Employee ID")
        self.box(456, y, RM - 456, em["employee_id"], name="employee id")
        y += 16

        # proposed loan
        y = self.banner(y, "Proposed Loan Details") + 3
        pl = a["proposed_loan"]
        lt = self.b["loan_terms"]
        self.label(LM, y, "Amount (₹)")
        self.comb(72, y, 7, self.num(pl["amount"]), align="r", name="loan amount")
        self.label(138, y, "Terms (Months)")
        self.comb(186, y, 2, self.num(pl["term_months"]), align="r", name="term")
        self.label(212, y, "P. Fee: @")
        self.uline(240, y, 26, self.num(lt["processing_fee_pct"]), size=6.6)
        self.label(268, y, "%")
        self.label(282, y, "ROI: @")
        self.uline(304, y, 30, self.num(lt["roi_pct"]), size=6.6)
        self.label(336, y, "%")
        self.label(358, y, "Repayment Mode")
        rm = pl["repayment_mode"]
        self.ticks_row(414, y, [(rm["pdc"], "PDC"), (rm["nach"], "NACH"), (rm["si"], "SI")])
        y += 13
        xx = self.label(LM, y, "Stamp duty charges as per State Stamp Act (₹)")
        self.uline(xx + 4, y, 90, self.num(lt["stamp_duty_amount"]), size=6.6)
        y += 15

        # financial details
        y = self.banner(y, "Financial Details") + 3
        fin = a["financial"]
        # bank accounts
        rh = 12.0
        cols = [(LM, 130), (130, 345), (345, RM)]
        self.rect(LM, y, 96, rh, fill=LGREY)
        self.txt(LM + 3, y + 8.3, "Bank Details", 6.0, "BodyB")
        for i, (xa, xb) in enumerate(cols[1:]):
            self.rect(xa, y, xb - xa, rh, fill=LGREY)
            self.txt((xa + xb) / 2, y + 8.3, ["Account I", "Account II"][i], 6.0, "BodyB", black, "c")
        y += rh
        for lab, key in (("Bank Name", "bank_name"), ("A/c Number", "account_number"), ("Type of Account", "account_type")):
            self.rect(LM, y, 96, rh)
            self.txt(LM + 3, y + 8.3, lab, 6.0, "BodyB")
            for i, (xa, xb) in enumerate(cols[1:]):
                self.rect(xa, y, xb - xa, rh)
                self.fit_text(xa + 3, y + 8.4, xb - xa - 6, str(fin["bank_accounts"][i][key]).upper(), 6.8, key)
            y += rh
        y += 4
        # loans
        lcols = [(LM, 100, "Loan Details"), (100, 250, "Financier Name"), (250, 320, "Loan Amount"),
                 (320, 400, "Type of Loan"), (400, 460, "EMI"), (460, RM, "Topup / BT")]
        for xa, xb, t in lcols:
            self.rect(xa, y, xb - xa, rh, fill=LGREY)
            self.txt((xa + xb) / 2 if t != "Loan Details" else xa + 3, y + 8.3, t, 6.0, "BodyB", black,
                     "c" if t != "Loan Details" else "l")
        y += rh
        for i, rl in enumerate(("Loan I", "Loan II", "Loan III")):
            ln = fin["existing_loans"][i] if i < len(fin["existing_loans"]) else {}
            vals = [rl, ln.get("financier_name", ""), self.num(ln.get("loan_amount", 0)), ln.get("type_of_loan", ""),
                    self.num(ln.get("emi", 0)), ln.get("topup_or_bt", "")]
            for (xa, xb, t), v in zip(lcols, vals):
                self.rect(xa, y, xb - xa, rh)
                if t == "Loan Details":
                    self.txt(xa + 3, y + 8.4, v, 6.0, "BodyB")
                else:
                    self.fit_text(xa + 3, y + 8.4, xb - xa - 6, str(v).upper(), 6.8, t)
            y += rh
        y += 5
        xx = self.label(LM, y, "*Annual Income", 6.3, True)
        self.uline(xx + 4, y, 140, self.num(fin["annual_income"]), name="annual income")
        self.txt(xx + 150, y + 7.4, "(Total of all income declared / only in absolute and numeric value)", 4.9,
                 "BodyI", MIDGREY)
        y += 13
        xx = self.label(LM, y, "Net Monthly Income (₹)")
        self.uline(xx + 4, y, 90, self.num(fin["net_monthly_income"]), name="net monthly income")
        xx = self.label(250, y, "*Total Annual house hold income", 6.3, True)
        self.uline(xx + 4, y, 100, self.num(fin["total_annual_household_income"]), name="household income")
        y += 13
        sf = fin["source_of_fund"]
        self.label(LM, y, "Source of Fund", 5.8, True)
        self.ticks_row(96, y, [(sf["salaried"], "Salaried"), (sf["investment"], "Investment"),
                               (sf["professional_fees"], "Professional Fees"),
                               (sf["business_earnings"], "Business Earnings"), (sf["commission"], "Commission"),
                               (sf["agriculture"], "Agriculture")], size=5.8)
        y += 12
        sw_ = fin["source_of_wealth"]
        self.label(LM, y, "Source of wealth", 5.8, True)
        xx = self.ticks_row(96, y, [(sw_["inherited_funds"], "Inherited funds"), (sw_["property"], "Property"),
                                    (sw_["investment"], "Investment"), (sw_["others"], "Others (Please Specify:")], size=5.8, gap=3)
        xx = self.uline(xx, y, 80, sw_["others_specify"], size=6.2, name="wealth others") + 2
        self.txt(xx, y + 7.4, "(if any)", 5.4)
        self.tick_label(xx + 28, y, sw_["nil"], "NIL", 5.8)
        xx2 = self.label(xx + 56, y, "Wealth (In Absolute Fig):", 5.8, True)
        self.uline(xx2 + 3, y, RM - xx2 - 3, self.num(fin["wealth_amount"]), size=6.2)
        y += 16

        # purpose
        y = self.banner(y, "Purpose of Loan*") + 3
        pu = a["purpose_of_loan"]
        xx = 40
        for key, lab in (("education", "Education"), ("home_renovation", "Home Renovation"), ("marriage", "Marriage"),
                         ("travel", "Travel"), ("consumer_durables", "Consumer Durables"), ("medical", "Medical"),
                         ("personal", "Personal")):
            xx = self.tick_label(xx, y, pu[key], lab, 6.4, 8.0) + 18
        y += 15

        # references
        y = self.banner(y, "Reference Details (One Reference has to be a Non-relative/Non-colleague)") + 0
        rcols = [(LM, 130), (130, 345), (345, RM)]
        self.rect(LM, y, 96, rh, fill=LGREY)
        for i, (xa, xb) in enumerate(rcols[1:]):
            self.rect(xa, y, xb - xa, rh, fill=LGREY)
            self.txt((xa + xb) / 2, y + 8.3, ["Reference I", "Reference II"][i], 6.2, "BodyB", black, "c")
        y += rh
        refs = a["references"]

        def rrow(h, label, fn, sub=None):
            nonlocal y
            self.rect(LM, y, 96, h)
            self.txt(LM + 3, y + 8.3, label, 6.0)
            if sub:
                self.txt(LM + 3, y + 14.3, sub, 4.3, "Body", MIDGREY)
            for i, (xa, xb) in enumerate(rcols[1:]):
                self.rect(xa, y, xb - xa, h)
                fn(xa + 3, xb - 3, refs[i])
            y += h

        def fld(key, w_cells=None):
            def f(xa, xb, r):
                self.fit_text(xa + 1, y + 8.6, xb - xa - 2, str(r[key]).upper(), 6.8, key)
            return f
        rrow(rh, "Name", fld("name"))
        rrow(15, "Relationship with Applicant", fld("relationship"), "(viz - Father, Mother, Brother, Sister etc.)")
        rrow(rh, "Address", fld("address_line_1"))
        rrow(rh, "", fld("address_line_2"))

        def pincity(xa, xb, r):
            yy = y + 1.2
            self.txt(xa, yy + 7.2, "*Pin", 5.6)
            self.comb(xa + 16, yy, 6, r["pincode"], cw=7.6, ch=9.6, size=6.4, name="ref pin")
            self.txt(xa + 70, yy + 7.2, "*City", 5.6)
            self.comb(xa + 88, yy, 12, r["city"], cw=7.6, ch=9.6, size=6.4, name="ref city")

        def statecountry(xa, xb, r):
            yy = y + 1.2
            self.txt(xa, yy + 7.2, "State", 5.6)
            self.comb(xa + 18, yy, 11, r["state"], cw=7.2, ch=9.6, size=6.2, name="ref state")
            self.txt(xa + 102, yy + 7.2, "*Country", 5.6)
            self.comb(xa + 128, yy, 10, r["country"], cw=7.2, ch=9.6, size=6.2, name="ref country")
        rrow(rh, "", pincity)
        rrow(rh, "", statecountry)
        rrow(rh, "Mobile No./Telephone", fld("mobile_or_telephone"))
        rrow(rh, "E-mail ID", fld("email"))
        y += 5

        # insurance
        y = self.banner(y, "Insurance Details") + 3
        ins = a["insurance"]
        self.txt(LM, y + 5.5, "Customer Sign-off Consent:", 5.8, "BodyB")
        y += 8
        self.tick_label(LM, y, ins["opt_in"], "Yes", 5.8)
        yy = self.flow(LM + 22, y, 505, [FT.INSURANCE_YES, ("f", ins["opt_in_policy_name"].upper(), 130), "."],
                       size=5.4)
        y = yy + 1.5
        self.tick_label(LM, y, ins["opt_out"], "No", 5.8)
        yy = self.flow(LM + 22, y, 505, [FT.INSURANCE_NO_A, ("f", ins["opt_out_policy_name"].upper(), 120),
                                         FT.INSURANCE_NO_B], size=5.4)
        y = yy + 1.5
        y = self.para(LM, y, 527, self.T(FT.INSURANCE_CLOSE), 5.4) + 3
        sp = a["signatures"]
        colw = 170
        for i, (key, cap) in enumerate((("primary_applicant", "Primary applicant's name"),
                                        ("co_applicant", "Co- applicant's name"),
                                        ("sales_representative", "Sales representative's name"))):
            xx = LM + i * (colw + 8.5)
            self.txt(xx, y + 9, "Signature", 5.4)
            self.sign_text(xx + 22, y - 3, colw - 26, 18, sp[key]["signature"], 17)
            self.line(xx + 22, y + 11, xx + colw - 6, y + 11, lw=0.35)
            self.line(xx, y + 25, xx + colw - 6, y + 25, lw=0.35)
            self.txt(xx, y + 21.5, sp[key]["name"].upper(), 6.2, "BodyB", INK)
            self.txt(xx, y + 31, cap, 5.0)
        y += 36

        # consent clauses
        y = self.banner(y, "Consent Clauses") + 2.5
        y = self.para(LM, y, 527, " ".join(self.T(s) for s in FT.CONSENT_AADHAAR), 5.15)
        y += 2.5
        self.txt(LM, y + 5.4, self.T(FT.CONSENT_LANG_INTRO), 5.4, "BodyB")
        pl_ = a["consents"]["preferred_language"]
        xx = LM + sw(FT.CONSENT_LANG_INTRO, "BodyB", 5.4) + 6
        langs = [("english", "English"), ("hindi", "Hindi"), ("marathi", "Marathi"), ("punjabi", "Punjabi"),
                 ("bengali", "Bengali"), ("odia", "Odia"), ("gujarati", "Gujarati"), ("kannada", "Kannada"),
                 ("malayalam", "Malayalam"), ("tamil", "Tamil"), ("telugu", "Telugu")]
        self.ticks_row(xx, y - 2.2, [(pl_[k], lab) for k, lab in langs], size=5.4, gap=4)
        y += 11
        y = self.para(LM, y, 527, " ".join(self.T(s) for s in FT.CONSENT_AFTER_LANG), 5.15)
        y += 3
        self.sig_box(RM - 118, y, 118, 32, sp["primary_applicant"]["signature"], "Applicant Signature")
        y += 34
        if y > H - 22:
            self.warn(f"page 2 content runs to y={y:.0f}")
        self.next_page()

    # ===================================================================== PAGE 3
    def page3(self):
        a = self.a
        sp = a["signatures"]
        y = 26.0
        y = self.banner(y, "Customer Declaration") + 3
        y = self.para(LM, y, 527, self.T(FT.DECL_OPEN), 5.2) + 2
        y = self.para(LM, y, 527, self.T(FT.DECL_UNDERTAKE), 5.2) + 2
        terms_y = y
        y = self.numbered(LM, y, 408, [self.T(t) for t in FT.DECL_TERMS], 5.2) + 2
        # photo + signature at the right of the terms
        px = RM - 108
        self.photo_box(px, terms_y, 108, 82, sp["photo"])
        self.sig_box(px, terms_y + 86, 108, 36, sp["primary_applicant"]["signature"], "Signature")
        y = max(y, terms_y + 124)
        self.tick(LM, y + 1.2, a["consents"]["declaration_not_pep"], 6.6)
        self.txt(LM + 10, y + 7.2, FT.DECL_PEP_LINE, 5.6, "BodyB")
        y += 13

        y = self.banner(y, "Information on Product and Offering") + 2.5
        y = self.para(LM, y, 527, self.T(FT.PRODUCT_OFFER), 5.1) + 3
        y = self.banner(y, "Cross Sell Consent") + 2.5
        y = self.para(LM, y, 500, self.T(FT.CROSS_SELL), 5.1)
        cs = a["consents"]
        self.tick_label(RM - 62, y - 7.5, cs["cross_sell_yes"], "YES", 5.8)
        self.tick_label(RM - 30, y - 7.5, cs["cross_sell_no"], "NO", 5.8)
        y += 3
        y = self.banner(y, "Declaration on Related Party / Specified Employee or Relative of Specified Employee:") + 2.5
        y = self.para(LM, y, 527, self.T(FT.RELATED_INTRO), 5.1)
        # items in two columns for compactness
        items = [self.T(s) for s in FT.RELATED_ITEMS]
        for it in items:
            y = self.para(LM + 6, y, 520, it, 5.1)
        y += 1.5
        self.txt(LM, y + 5.2, self.T(FT.RELATED_IF_YES), 5.3, "BodyB")
        y += 8
        rp = a["related_party_declaration"]
        heads = ["Name of Related Party / Specified Employee or relative of Specified Employee",
                 "Nature of classification (Related Party / Specified Employee / Relative of Specified Employee)",
                 "Details or Reason of such classification", "Relationship details (if relative)"]
        ws = [150, 150, 130, 97]
        xx = LM
        for hdr, w_ in zip(heads, ws):
            self.rect(xx, y, w_, 15, fill=LGREY)
            self.flow(xx + 2, y + 1.5, w_ - 4, [hdr], 4.6, 5.3)
            xx += w_
        y += 15
        entries = rp.get("entries", [])
        for i in range(2):
            e = entries[i] if i < len(entries) else {}
            xx = LM
            for k, w_ in zip(("name", "nature_of_classification", "reason", "relationship_details"), ws):
                self.rect(xx, y, w_, 11)
                if e.get(k):
                    self.fit_text(xx + 2, y + 8, w_ - 4, str(e[k]).upper(), 6.2, k)
                xx += w_
            y += 11
        y += 3
        y = self.para(LM, y, 527, self.T(FT.RELATED_CLOSE), 5.1) + 2
        half = 262
        self.rect(LM, y, half, 22)
        self.sign_text(LM, y, half, 22, sp["primary_applicant"]["signature"], 14)
        self.txt(LM + half - 3, y + 19.5, "Signature of the Applicant", 5.0, "Body", MIDGREY, "r")
        self.rect(LM + half, y, RM - LM - half, 22)
        if rp.get("authorized_signatory_name"):
            self.fit_text(LM + half + 3, y + 12, RM - LM - half - 6, rp["authorized_signatory_name"].upper(), 6.4)
        self.txt(LM + half + 3, y + 19.5, "Authorized Signatory (Name)", 5.0, "Body", MIDGREY)
        y += 24
        self.txt(LM, y + 5, FT.RELATED_SIGN_LINE, 5.2, "BodyB")
        y += 8
        for i, t in enumerate(FT.DEFINITIONS):
            y = self.para(LM, y, 527, self.T(t), 4.75, font="BodyB" if i == 0 else "Body") + 0.8
        y += 3
        # tear-off line + acknowledgement slip
        self.line(LM, y + 3, RM, y + 3, lw=0.5, color=MIDGREY, dash=(3, 2))
        y += 7
        ack = self.b["acknowledgement"]
        y = self.banner(y, "Acknowledgment for Receipt of Application Form") + 3
        self.label(LM, y, "Date", 6.3, True)
        self.date_boxes(58, y, ack["date"], name="ack date")
        self.label(136, y, "To,", 6.3, True)
        self.uline(150, y, 300, ack["addressee_name"], name="ack addressee")
        self.rect(RM - 98, y - 1, 98, 40, lw=0.6, color=MIDGREY)
        self.txt(RM - 92, y + 10, "Serial No.", 8, "Body", MIDGREY)
        self.txt(RM - 49, y + 32, self.b["serial_no"], 8.5, "BodyB", INK, "c")
        y += 14
        y = self.flow(LM, y, 420, [FT.ACK_TEXT.split("1. ")[0] + self.T("{bank_name} has received your application for a Personal Loan of ₹"),
                                   ("f", self.num(ack["loan_amount"]), 70)], 5.4)
        y = self.para(LM, y + 1, 420, self.T(FT.ACK_TEXT), 5.0) + 3
        rows = [("For any queries clarifications, please contact landline number", ack["contact_landline"]),
                ("Sales Manager", ack["sales_manager"]), ("DSA", ack["dsa"]),
                ("Sales Executive", ack["sales_executive"]), ("E-mail ID", ack["email"])]
        for lab, val in rows:
            self.rect(LM, y, 250, 10.5)
            self.txt(LM + 3, y + 7.6, lab, 5.8)
            self.rect(LM + 250, y, 277, 10.5)
            self.fit_text(LM + 254, y + 7.8, 270, str(val).upper(), 6.4)
            y += 10.5
        if y > H - 22:
            self.warn(f"page 3 content runs to y={y:.0f}")
        # margin version string
        self.c.saveState()
        self.c.setFont("Body", 4.8)
        self.c.setFillColor(MIDGREY)
        self.c.translate(W - 12, H - 330)
        self.c.rotate(90)
        self.c.drawString(0, 0, self.meta["form_version"])
        self.c.restoreState()
        self.next_page()

    # ===================================================================== PAGE 4
    def page4(self):
        a, b = self.a, self.b
        sp = a["signatures"]
        so = b["sourcing"]
        y = 26.0
        y = self.banner(y, "Sourcing Details (For official use only)") + 3
        self.label(LM, y, "Sales Centre Name", 6.3, True)
        self.comb(112, y, 28, so["sales_centre_name"], name="sales centre")
        y += 13
        ch = so["channel"]
        self.label(LM, y, "Channel")
        self.ticks_row(70, y, [(ch["dsa"], "DSA"), (ch["open_market"], "Open Market"),
                               (ch["branch_channel"], "Branch Channel"), (ch["direct"], "Direct"),
                               (ch["campaign_activity"], "Campaign Activity"), (ch["digital"], "Digital"),
                               (ch["connector"], "Connector"),
                               (ch["service_recovery_digital_servicing"], "Service Recovery & Digital Servicing")],
                       size=5.8, gap=5)
        y += 13
        sc = so["source_code"]
        self.label(LM, y, "Source Code", 5.9, True)
        self.txt(LM, y + 14, "(For digital only)", 4.6, "Body", MIDGREY)
        self.ticks_row(96, y, [(sc["sms"], "SMS"), (sc["emailer"], "E-mailer"), (sc["mobile"], "Mobile"),
                               (sc["internet_banking"], "Internet Banking"), (sc["website"], "Website"),
                               (sc["atm"], "ATM"), (sc["aggregator"], "Aggregator"), (sc["connector"], "Connector")],
                       size=5.8, gap=5)
        y += 12
        self.ticks_row(96, y, [(sc["phone_banking"], "Phone Banking"), (sc["corporate_banner"], "Corporate Banner"),
                               (sc["service_recovery_digital_servicing"], "Service Recovery & Digital Servicing"),
                               (sc["open_market"], "Open Market")], size=5.8, gap=5)
        y += 14
        self.label(LM, y, "Referrer Branch Name")
        self.comb(112, y, 22, so["referrer_branch_name"], name="ref branch")
        self.label(312, y, "Referrer Branch ID")
        self.comb(378, y, 6, so["referrer_branch_id"], name="ref branch id")
        y += 13
        self.label(LM, y, "CRM ID")
        self.comb(112, y, 14, so["crm_id"], name="crm id")
        self.label(260, y, "ASM Employee Nos.")
        self.comb(330, y, 10, so["asm_employee_no"], name="asm")
        y += 13
        self.label(LM, y, "TL/DSA/Connector Name")
        self.comb(112, y, 18, so["tl_dsa_connector_name"], name="tl name")
        self.label(272, y, "TL/DSA/Connector Code")
        self.comb(356, y, 10, so["tl_dsa_connector_code"], name="tl code")
        y += 13
        self.label(LM, y, "DME Name")
        self.comb(112, y, 18, so["dme_name"], name="dme name")
        self.label(272, y, "DME Code")
        self.comb(356, y, 10, so["dme_code"], name="dme code")
        self.sig_box(RM - 112, y - 12, 112, 36, so["agent_signature"], "Signature of Sourcing Agent")
        y += 18
        rm = b["rm_sm"]
        self.label(LM, y, "RM/SM details", 6.3, True)
        y += 13
        self.label(LM, y, self.meta["bank_name"] + " RM/ SM")
        self.comb(112, y, 22, rm["name"], name="rm name")
        self.label(RM - 112, y - 1, "")
        y += 13
        self.label(LM, y, "Designation")
        self.comb(112, y, 22, rm["designation"], name="rm designation")
        self.label(312, y, "Employee ID")
        self.comb(362, y, 8, rm["employee_id"], name="rm emp id")
        y += 13
        self.label(LM, y, "Employee Branch")
        self.comb(112, y, 22, rm["employee_branch"], name="rm branch")
        self.sig_box(RM - 112, y - 10, 112, 24, rm["signature"], "Signature of Sourcing Agent")
        y += 18
        # OSV block
        osv = b["osv"]
        self.rect(LM, y, RM - LM, 66, lw=0.5)
        self.txt(LM + 150, y + 8, "In person verification- OSV done by (For CKYC entry)", 6.0, "BodyB")
        yy = y + 11
        for lab, key in ((self.meta["bank_name"] + " Staff Name", "staff_name"),
                         ("Designation (as per HR grade)", "designation"),
                         ("Branch/Location", "branch_location"), ("Employee ID", "employee_id")):
            self.label(LM + 3, yy, lab, 5.9, True)
            self.comb(LM + 120, yy, 24, osv[key], name="osv " + key)
            yy += 13
        self.sig_box(RM - 118, y + 14, 112, 46, osv["signature"], "Signature")
        y += 66
        self.txt(LM, y + 6.5, "(Filling of all the fields is mandatory and No. field should be left Blank. User should "
                              "either provide details or should mention NA to avoid any data fudging in blank spaces)",
                 4.6, "BodyI")
        y += 10

        # FATCA
        y = self.banner(y, "FATCA- CRS DECLARATION") + 3
        fa = a["fatca_crs"]
        self.txt(LM, y + 5.5, "(Please tick the applicable tax resident declaration (Any one)*", 5.8)
        y += 8
        self.tick_label(LM, y, fa["tax_resident_india_only"], FT.FATCA_TEXT_INDIA, 5.8)
        self.tick_label(300, y, fa["tax_resident_other_countries"], FT.FATCA_TEXT_OTHER, 5.8)
        y += 11
        self.txt(LM, y + 5.5, FT.FATCA_INTRO, 5.8)
        y += 9
        self.label(LM, y, "City of Birth*", 6.0)
        self.comb(90, y, 14, fa["city_of_birth"], name="city of birth")
        y += 13
        self.label(LM, y, "Country of Birth*", 6.0)
        self.comb(90, y, 14, fa["country_of_birth"], name="country of birth")
        y += 13
        at = fa["address_type"]
        self.label(LM, y, "Address Type for Tax Purposes*", 6.0)
        self.ticks_row(150, y, [(at["resident"], "Resident"), (at["business"], "Business"),
                                (at["registered_office"], "Registered office")], size=5.9, gap=14)
        y += 14
        # table
        cws = [90, 100, 90, 82, 82, 83]
        heads = ["Country#", "Tax Identification Number %", "Identification Type (TIN or Other, please specify)%",
                 "Communication Address", "Permanent Address", "Please note the address below"]
        xx = LM
        self.txt(LM + 90 + 100 + 90 + 82 * 1, y - 2, "", 5)
        for w_, hd in zip(cws, heads):
            self.rect(xx, y, w_, 22, fill=LGREY)
            self.flow(xx + 2, y + 2, w_ - 4, [hd], 5.0, 5.8, "BodyB")
            xx += w_
        self.txt(LM + 90 + 100 + 90, y - 1.5, "Address for Tax Purpose*", 5.0, "BodyB")
        y += 22
        tr = fa.get("tax_residencies", [])
        for i in range(2):
            r = tr[i] if i < len(tr) else {}
            ad = r.get("address_for_tax", {})
            vals = [r.get("country", ""), r.get("tax_identification_number", ""), r.get("identification_type", "")]
            xx = LM
            for w_, v in zip(cws[:3], vals):
                self.rect(xx, y, w_, 12)
                self.fit_text(xx + 3, y + 8.6, w_ - 6, str(v).upper(), 6.4)
                xx += w_
            self.rect(xx, y, cws[3], 12)
            self.tick(xx + cws[3] / 2 - 3.3, y + 2.7, bool(ad.get("communication_address")))
            xx += cws[3]
            self.rect(xx, y, cws[4], 12)
            self.tick(xx + cws[4] / 2 - 3.3, y + 2.7, bool(ad.get("permanent_address")))
            xx += cws[4]
            self.rect(xx, y, cws[5], 12)
            oth = ad.get("other", {})
            if any(oth.values()):
                # full address is printed in the Landmark/PIN/State/Country row below the table
                self.fit_text(xx + 3, y + 8.6, cws[5] - 6, "SEE ADDRESS BELOW", 5.6)
            y += 12
        y += 4
        oth = next((r["address_for_tax"]["other"] for r in tr
                    if any(r.get("address_for_tax", {}).get("other", {}).values())), {})
        self.label(LM, y, "Landmark", 5.9)
        self.uline(76, y, 150, oth.get("landmark", ""), size=6.2)
        self.label(240, y, "*PIN", 5.9)
        self.comb(262, y, 6, oth.get("pin", ""), cw=8.0, ch=9.6, size=6.4)
        self.label(318, y, "*State", 5.9)
        self.comb(342, y, 10, oth.get("state", ""), cw=7.4, ch=9.6, size=6.2)
        self.label(424, y, "*Country", 5.9)
        self.uline(456, y, RM - 456, oth.get("country", ""), size=6.2)
        y += 13
        self.txt(LM, y + 5, FT.FATCA_NOTE_HASH, 5.2)
        self.txt(LM, y + 12, FT.FATCA_NOTE_PCT, 5.2)
        y += 17
        y = self.para(LM, y, 395, FT.FATCA_CERT, 5.2)
        self.sig_box(RM - 112, y - 24, 112, 32, sp["primary_applicant"]["signature"], "Signature")
        y += 10

        # charges footer
        self.line(LM, y, RM, y, lw=0.5, color=MIDGREY, dash=(3, 2))
        y += 5
        self.txt(LM, y + 6, "DETAILS OF CHARGES", 5.6, "BodyB")
        y += 9
        lt = b["loan_terms"]
        colx = [(LM, 166), (LM + 172, 186), (LM + 364, 163)]
        sz = 4.95
        # left
        yl = y
        for toks in FT.CHARGES_LEFT:
            tk = []
            for t in toks:
                if isinstance(t, tuple):
                    tk.append(("f", self.num(lt["processing_fee_pct"]) if t[1] == "pf" else self.num(lt["roi_pct"]), 20))
                else:
                    tk.append(t)
            yl = self.flow(colx[0][0], yl, colx[0][1], tk, sz) + 1.4
        ym = y
        for t in FT.CHARGES_MID:
            ym = self.para(colx[1][0], ym, colx[1][1], self.T(t), sz,
                           font="BodyB" if t.startswith("Disbursed") else "Body") + 1.4
        yr = y
        for t in FT.CHARGES_RIGHT:
            yr = self.para(colx[2][0], yr, colx[2][1], self.T(t), sz) + 1.4
        y = max(yl, ym, yr) + 3
        # strip + EMI grid
        ys = y
        for i, t in enumerate(FT.CHARGES_STRIP):
            ys = self.para(LM, ys, 340, self.T(t), 4.8, font="BodyB" if t.startswith("DOCUMENTATION") else "Body") + 1.2
        gx, gw = RM - 180, 180
        self.txt(gx, y + 6, "The EMI date for Personal loan will be as per following grid:", 4.9, "BodyB")
        gy = y + 9
        for i, (c1, c2) in enumerate(FT.EMI_GRID):
            self.rect(gx, gy, gw / 2, 10, fill=LGREY if i == 0 else None)
            self.rect(gx + gw / 2, gy, gw / 2, 10, fill=LGREY if i == 0 else None)
            self.txt(gx + 3, gy + 7.2, c1, 5.0, "BodyB" if i == 0 else "Body")
            self.txt(gx + gw / 2 + 3, gy + 7.2, c2, 5.0, "BodyB" if i == 0 else "Body")
            gy += 10
        self.sig_box(gx + 70, gy + 3, 110, 30, b["authorised_signature"], self.T("For {bank_name}, Authorised Official"))
        y = max(ys, gy + 33)
        if y > H - 22:
            self.warn(f"page 4 content runs to y={y:.0f}")
        self.footer()
        self.c.showPage()

    def render(self):
        self.page1()
        self.page2()
        self.page3()
        self.page4()
        self.c.save()


def b_get(b, k):
    return b.get(k, "")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sample_applicant.json")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "sample_application.pdf")
    with open(src) as f:
        data = json.load(f)
    form = Form(data, out)
    form.render()
    print("wrote", out)
    for w in form.warnings:
        print("WARN:", w)


if __name__ == "__main__":
    main()
