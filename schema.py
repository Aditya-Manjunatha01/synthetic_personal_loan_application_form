"""Blank application dictionary: every key the form can take, with empty/false defaults.

Key names follow the field-map doc. Tick boxes are booleans (True = filled black box),
text is a string, amounts are integers, dates are ISO strings (YYYY-MM-DD).
"""
import copy


def _bools(*names):
    return {n: False for n in names}


def _name():
    return {"prefix": "", "first_name": "", "middle_name": "", "last_name": ""}


def _yn():
    return {"yes": False, "no": False}


def _address(extra_ownership):
    return {
        "line_1": "", "line_2": "", "line_3": "", "landmark": "", "city": "", "state": "",
        "country": "", "pincode": "", "mobile_number": "", "phone_number": "",
        "is_mailing_address": False,
        "ownership": _bools(*extra_ownership),
    }


def blank():
    present = _address(["self_owned", "parental", "owned_mortgaged", "company_provided",
                        "paying_guest", "rental", "relative"])
    present.update({"years_at_residence": 0, "months_at_residence": 0,
                    "years_in_city": 0, "months_in_city": 0})
    permanent = _address(["self_owned", "parental", "owned_mortgaged", "rental", "relative"])

    office = {k: v for k, v in _address([]).items() if k != "ownership"}

    ckyc = {
        "aadhaar": {"proof_of_identity": _yn(), "present_address": _yn(), "permanent_address": _yn(), "document_number": ""},
        "voter_id": {"proof_of_identity": _yn(), "present_address": _yn(), "permanent_address": _yn(), "document_number": ""},
        "pan": {"proof_of_identity": _yn(), "document_number": ""},
        "passport": {"proof_of_identity": _yn(), "present_address": _yn(), "permanent_address": _yn(),
                     "document_number": "", "date_of_issue": "", "date_of_expiry": ""},
        "driving_license": {"proof_of_identity": _yn(), "present_address": _yn(), "permanent_address": _yn(),
                            "document_number": "", "date_of_issue": "", "date_of_expiry": ""},
        "utility_bill": {"present_address": _yn(), "document_number": ""},
        "npr_letter": {"permanent_address": _yn(), "document_number": ""},
        "pension_order": {"present_address": _yn(), "document_number": ""},
        "narega": {"present_address": _yn(), "permanent_address": _yn(), "document_number": ""},
        "internal_banking": {"present_address": _yn(), "permanent_address": _yn()},
        "ckyc_identifier": {"permanent_address": _yn(), "document_number": ""},
    }

    reference = {"name": "", "relationship": "", "address_line_1": "", "address_line_2": "",
                 "pincode": "", "city": "", "state": "", "country": "",
                 "mobile_or_telephone": "", "email": ""}

    applicant = {
        "application_date": "",
        "existing_customer": {"customer_id": "", "savings_account_yes": False,
                              "savings_account_no": False, "account_no": ""},
        "loan_type": {"pre_approved": False, "premium_scheme": False, "topup_with_closure": False,
                      "parallel": False, "external_bt_loan_account_no": ""},
        "personal_details": {
            "name_as_per_id": _name(), "name_as_per_pan": _name(), "maiden_name": _name(),
            "father_name": _name(), "mother_maiden_name": _name(),
            "email": "", "email_statement": False,
            "constitution": _bools("resident_indian", "non_resident_indian", "foreign_national",
                                   "overseas_citizen_of_india", "person_of_indian_origin"),
            "nationality": {"indian": False, "other_selected": False, "other_text": ""},
            "pep_yes": False, "pep_no": False,
            "community": {**_bools("hindu", "muslim", "buddhist", "christian", "sikh", "zoroastrian",
                                   "jain", "parsi", "others"), "others_specify": ""},
            "category": {**_bools("general", "obc", "scheduled_caste", "scheduled_tribe", "others"),
                         "others_specify": ""},
            "gender": _bools("male", "female", "third_gender"),
            "status": _bools("resident", "nri", "pio", "oci", "foreign_national"),
            "dob_as_per_id": "", "dob_as_per_pan": "",
            "marital_status": _bools("married", "single", "others"),
            "dependents": 0,
            "disability_yes": False, "disability_no": False,
            "education": _bools("matriculate", "undergraduate", "graduate", "postgraduate",
                                "professional", "others"),
        },
        "present_address": present,
        "permanent_address": permanent,
        "employment": {
            "occupation": _bools("salaried", "consultant"),
            "designation": "", "department": "",
            "organisation_type": _bools("pvt_ltd", "public_ltd", "proprietorship", "partnership_firm",
                                        "public_sector", "government", "mnc",
                                        "trust_association_society_club"),
            "nature_of_employment": "", "employer_name": "",
            "office_address": office,
            "office_email": "", "office_email_statement": False,
            "years_in_current_employment": 0, "months_in_current_employment": 0,
            "total_employment_years": 0, "total_employment_months": 0,
            "employee_id": "",
        },
        "police_defense": {"belt_no": "", "pis_or_employee_no": "", "rank": "", "regiment_unit_details": ""},
        "ckyc": ckyc,
        "proposed_loan": {"amount": 0, "term_months": 0, "repayment_mode": _bools("pdc", "nach", "si")},
        "financial": {
            "bank_accounts": [{"bank_name": "", "account_number": "", "account_type": ""} for _ in range(2)],
            "existing_loans": [{"financier_name": "", "loan_amount": 0, "type_of_loan": "", "emi": 0,
                                "topup_or_bt": ""} for _ in range(3)],
            "annual_income": 0, "net_monthly_income": 0, "total_annual_household_income": 0,
            "source_of_fund": _bools("salaried", "investment", "professional_fees", "business_earnings",
                                     "commission", "agriculture"),
            "source_of_wealth": {**_bools("inherited_funds", "property", "investment", "others"),
                                 "others_specify": "", "nil": False},
            "wealth_amount": 0,
        },
        "purpose_of_loan": _bools("education", "home_renovation", "marriage", "travel",
                                  "consumer_durables", "medical", "personal"),
        "references": [copy.deepcopy(reference) for _ in range(2)],
        "insurance": {"opt_in": False, "opt_in_policy_name": "", "opt_out": False, "opt_out_policy_name": ""},
        "consents": {
            "preferred_language": _bools("english", "hindi", "marathi", "punjabi", "bengali", "odia",
                                         "gujarati", "kannada", "malayalam", "tamil", "telugu"),
            "cross_sell_yes": False, "cross_sell_no": False,
            "declaration_not_pep": False,
        },
        "related_party_declaration": {"entries": [], "authorized_signatory_name": ""},
        "fatca_crs": {
            "tax_resident_india_only": False, "tax_resident_other_countries": False,
            "city_of_birth": "", "country_of_birth": "",
            "address_type": _bools("resident", "business", "registered_office"),
            "tax_residencies": [],
        },
        "signatures": {
            "primary_applicant": {"signature": "", "name": ""},
            "co_applicant": {"signature": "", "name": ""},
            "sales_representative": {"signature": "", "name": ""},
            "photo": "",
        },
    }

    bank_use = {
        "serial_no": "", "company_code": "",
        "promo": {"code": "", **_bools("seven_year_tenure", "regional_police", "police",
                                       "premium_scheme", "credit_card_balance_transfer")},
        "loan_terms": {"processing_fee_pct": 0.0, "roi_pct": 0.0, "stamp_duty_amount": 0},
        "sourcing": {
            "sales_centre_name": "",
            "channel": _bools("dsa", "open_market", "branch_channel", "direct", "campaign_activity",
                              "digital", "connector", "service_recovery_digital_servicing"),
            "source_code": _bools("sms", "emailer", "mobile", "internet_banking", "website", "atm",
                                  "aggregator", "connector", "phone_banking", "corporate_banner",
                                  "service_recovery_digital_servicing", "open_market"),
            "referrer_branch_name": "", "referrer_branch_id": "", "crm_id": "", "asm_employee_no": "",
            "tl_dsa_connector_name": "", "tl_dsa_connector_code": "", "dme_name": "", "dme_code": "",
            "agent_signature": "",
        },
        "rm_sm": {"name": "", "employee_id": "", "designation": "", "employee_branch": "", "signature": ""},
        "osv": {"staff_name": "", "designation": "", "branch_location": "", "employee_id": "", "signature": ""},
        "acknowledgement": {"date": "", "addressee_name": "", "loan_amount": 0, "contact_landline": "",
                            "sales_manager": "", "dsa": "", "sales_executive": "", "email": ""},
        "authorised_signature": "",
    }

    return {
        "form_meta": {
            "bank_name": "bank logo", "bank_tagline": "bank tagline",
            "bank_website": "www.example-bank.com",
            "form_title": "Application For Personal Loan", "form_code": "PL02",
            "form_version": "RA/PL/App Form/April2026/ Version 1.00",
        },
        "applicant": applicant,
        "bank_use": bank_use,
    }
