"""Static printed text of the form. {bank_name} and {bank_website} are filled from form_meta."""

INSURANCE_YES = ("I/We wish to protect my/our family from the loan liability in case of an eventuality i.e. "
                 "Loss / Damage / Hospitalisation / Death (whichever is applicable) and voluntarily would like "
                 "to opt for (Type/Name of Policy)")
INSURANCE_NO_A = "I/We have been informed by {bank_name} about (Type/Name of Policy)"
INSURANCE_NO_B = (", but I/We have decided not to opt for it and. I/We completely understand that in case of an "
                  "eventuality i.e. Loss / Damage / Hospitalisation / Death (whichever is applicable), the "
                  "responsibility for EMI payment / loan repayment would remain & could fall on my /our family / "
                  "firm, failing which, {bank_name} would take necessary action(s) for recovery.")
INSURANCE_CLOSE = ("I understand I can opt in or opt out of the insurance policy anytime prior to loan disbursal by "
                   "sending an email from my registered / mailing email id to {bank_name} representative.")

CONSENT_AADHAAR = [
    "I hereby give my consent to and authorize {bank_name} to fetch my personal details from UIDAI.",
    "I hereby state that I have no objection in authenticating myself with Aadhaar based authentication system and I "
    "voluntarily consent to providing my Aadhaar number / VID number, Biometric information and/or One Time Pin (OTP) "
    "data (and/or any similar authentication data) for the purpose of personal loan application.",
    "I understand that the biometric and/or OTP and/or any other authentication data I may provide for authentication "
    "shall be used only for authenticating my identity through the Aadhaar authentication system for the specific "
    "transaction or as per requirement of law and for no other purposes.",
    "I confirm that I have been informed about the alternatives to submission of identity information and I have agreed "
    "to authenticate myself through Aadhaar based authentication system with full understanding of alternatives to "
    "submission of identity information.",
    "I understand that {bank_name} shall ensure security and confidentiality of my personal identity data provided for "
    "the purpose of Aadhaar based authentication.",
    "I authorize {bank_name} to verify and authenticate my Aadhaar data during processing my personal loan.",
    "I further authorize the Bank to share my Aadhaar related details/information with regulatory/statutory bodies as "
    "and when required.",
]
CONSENT_LANG_INTRO = "I confirm my preferred language of communication is:"
CONSENT_AFTER_LANG = [
    "I confirm that the Bank has explained and provided me the above information in my local language before collecting "
    "my personal details for the purpose of Aadhaar based authentication.",
    "I hereby expressly consent to and authorize the Bank (whether acting by itself or through any of its service "
    "providers, and whether in automated manner or otherwise), to collect, store and process my application details, "
    "personal data and sensitive information about me, information, papers and data relating to know your customer "
    "(KYC), credit information, and any other information about me/pertaining to me or not as may be deemed relevant by "
    "the Bank (collectively, \"Information\") and I hereby also expressly consent to and authorize the Bank to download "
    "KYC details from the CKYC registry using my CKYC ID for the purpose of personal loan application.",
    "I expressly consent Bank to share and disclose the Information to service providers, consultants, credit "
    "information companies, information utilities, other banks and financial institutions, affiliates, group "
    "companies, subsidiaries, regulators, investigating agencies, judicial, quasi-judicial and statutory authorities, "
    "or to other persons/institutions/entities as may be necessary in connection with the contractual or legal "
    "requirements or in the legitimate interests of the Bank or as per the consent, undertake to process information "
    "including by way of storing, structuring, organizing, reproducing, copying, using, profiling, etc. as may be "
    "deemed fit by the Bank and for the purposes of credit appraisal, fraud detection, anti-money laundering "
    "obligations, for entering into contract, for developing credit scoring models and business strategies, for "
    "monitoring, for evaluating and improving the quality of services and products, or for any purposes as the Bank "
    "may deem fit.",
]

DECL_OPEN = (
    "I/We declare that the particulars and information given in the application form are true, correct, complete and up "
    "to date in all respects and I/we have not withheld any information. I/We confirm that I/We have no insolvency "
    "proceeding initiated against me/us nor have I/We ever been abjudicated insolvent. I/We have read the application "
    "form and am/are aware of all terms and conditions of availing finance from {bank_name}. I/We authorize "
    "{bank_name} to make reference and inquiries relating to information in this application which the bank considers "
    "necessary. I/We authorize the bank to exchange, part/share with all information relating to my/our loan details and "
    "repayment history to other banks/financial institutions etc. as may be required and shall not hold the bank liable "
    "for use of this information. I/We undertake to inform the bank regarding change in my residence/employment and to "
    "provide any further information that the bank may require. I/We agree that my/our loan shall be governed by the "
    "rules of the bank which may be in force from time to time. I/We understand that the Bank has the right to reject "
    "my/our application without providing any reason thereof. The borrower(s)/guarantor(s) agree(s) to have given "
    "his/their express consent to the Bank to disclose all information and data furnished by them to Credit information "
    "companies (CIC's) or any other credit bureau permitted to operate in India. The borrower(s)/guarantor(s) further "
    "agree(s) that they shall execute such additional documents as may be necessary for the purpose. I/We confirm that "
    "I/We have received a copy of the \"Code of Bank's commitment to Customers\". I/We have been explained the content "
    "of the same and also understand that it is available on-line at the Bank's website, \"{bank_website}\". I hereby "
    "declare that the details furnished above are true and correct to the best of my/our knowledge and belief and I "
    "undertake to inform you of any changes therein, immediately. In case any of the above information is found to be "
    "false or untrue or misleading or misrepresenting, I/We am/are aware that I/we may be held liable for it. My "
    "personal / KYC details may be shared with Central KYC Registry. I hereby consent to receiving information from "
    "Central KYC Registry through SMS/Email on the above registered number/email address."
)
DECL_UNDERTAKE = (
    "I/We undertake that the proceeds of this facility shall not be used for investment in the capital market or "
    "purchase of gold in any form including primary gold, gold bullion, gold jewellery, gold coins, units of gold "
    "Exchange Traded Funds (ETF) and units of gold Mutual Funds & Small saving instruments and for speculative "
    "purpose. I/We also confirm that I have been explained the following:"
)
DECL_TERMS = [
    "{bank_name} will convey its decision within 30 working days from the date of receipt of the application provided "
    "the application is complete in all respects and is submitted along with all the documents as per 'check list' "
    "provided in the application for loan and/or any additional documents as may be required by the bank for proper "
    "appraisal of the application. The computation of 30 days shall start from the day on which all documents required "
    "for a proper appraisal of the application are provided by the Customer to the bank.",
    "The bank may at its sole discretion sanction or decline the application. The bank shall convey, the reasons, which "
    "in its opinion after due consideration, have led to rejection of the application. The Bank will decide and assign "
    "the loan amount and no commitment has been given to us for the same.",
    "The DSA/DST or any other executive (has not collected any commission/brokerage or any other fee by way of cash or "
    "cheque or any other mode.",
    "{bank_name} reserves the right to retain photographs and documents submitted with this application and will not "
    "return the same to the applicant.",
    "As per RBI guidelines, classification of accounts as NPA is done Borrower wise and not Facility wise and hence, it "
    "may be noted that in case of non-payment of dues by the customer in case of any facility availed from the Bank and "
    "consequently the account is to be classified as NPA, all other loan accounts of the Borrower/Card Holder, with the "
    "Bank also shall be classified as NPA as per the guidelines issued by RBI and it shall entitle the Bank to recall "
    "all such loans/Facilities availed by the customer in such accounts.",
    "I/we authorize {bank_name} to Verify/Authenticate my/our KYC OVDs/Aadhaar number/loan documents during processing "
    "my/our loan application through third party agencies via digitally/physically for legitimate business purpose.",
    "I/We authorize {bank_name} to verify and authenticate my/our Aadhaar number during processing my/our application "
    "for legitimate Business purposes. I/We further authorize the Bank to share my Aadhaar related "
    "details/information with regulatory / statutory bodies as and when required.",
    "We understand the Loan amount/ Rate Of Interest / Fees and charges mentioned in the application are only "
    "indicative and the terms of the Loan will be guided by the terms of the Personal Loan Agreement/ sanction letter "
    "accepted by me/us prior to disbursement.",
    "I/We undertake to inform the Bank in case of any update in the information provided or documents submitted by "
    "me/us for the grant of personal loan by the Bank at the time of establishment of business relationship and "
    "thereafter, as necessary; I/we shall submit to the Bank the update of such information/documents. I/We agree to "
    "do the aforementioned within 30 days of the update to any such information/documents for the purpose of updating "
    "the records at the Banks' end.",
    "Politically Exposed Persons\" (PEPs) are individuals who are or have been entrusted with prominent public "
    "functions by a foreign country, including the Heads of States/ Governments, senior politicians, senior government "
    "or judicial or military officers, senior executives of state-owned corporations and important political party "
    "officials.",
]
DECL_PEP_LINE = ("I declare that I am not a Politically Exposed Person (PEP) nor I am related to any Politically "
                 "Exposed Person (PEP)")

PRODUCT_OFFER = (
    "I expressly consent to the Bank to share and disclose my information, including personal information, to credit "
    "information companies, bureaus, regulators or governmental authorities, investigating agencies, judicial, "
    "quasi-judicial and statutory authorities, group companies, business partners, collaborators, cobrand entity/ "
    "partner, card associations, settlement, transfer and processing intermediaries, distributor (for legal and "
    "regulatory requirements only), information utilities, other banks and financial institutions, merchant "
    "aggregators, payment gateways, other players/ intermediaries or to other persons/entities, as may be necessary in "
    "connection with the contractual, regulatory or legal requirements for processing such information including by "
    "way of wholly or partly performing automated or physical operations, including collection, recording, organizing, "
    "structuring, storing, adapting, retrieving, using, profiling, aligning, indexing, sharing, disseminating or "
    "otherwise making available, as may be deemed fit by the Bank and for the purposes of customer services and "
    "operations, collections and recovery, audit, investigation, monitoring and fraud prevention, credit appraisal, "
    "legal and regulatory requirements including KYC verification and reporting to regulatory and statutory "
    "authorities, security, testing, for entering into contract, for developing credit scoring models and business "
    "strategies, for monitoring, for evaluating and improving the quality of Bank's products and services/ cross "
    "selling."
)
CROSS_SELL = (
    "I expressly agree to the Bank, its service providers, agents and/or its affiliates for using the information, "
    "including personal information, for marketing, promotion, research and analytics, and cross-selling of products "
    "and services of the Bank and of the Bank's subsidiaries, affiliates/ group companies from time to time via "
    "telephone, SMS and/or email. Further, I hereby acknowledge that the Bank has provided me with an option to "
    "withdraw consent to the purpose herein at any time by intimation through letter or email. However, if I withdraw "
    "my consent, I accept that the Bank will stop processing my personal data except where such processing is "
    "mandatory as per applicable law and that any personal data that has already been processed shall remain "
    "unaffected by the withdrawal of such consent."
)

RELATED_INTRO = ("Having understood the definitions provided below and to the best of my / our knowledge and belief, "
                 "I / We do hereby solemnly declare and confirm that I / We are not:")
RELATED_ITEMS = [
    "a) a related person / reciprocally related person, or",
    "b) a reciprocally related person, or",
    "c) a specified employee of {bank_name}, or",
    "d) a relative of specified employee of {bank_name}, or",
    "e) a firm in which any of the directors or the spouse or dependent / minor child of directors of {bank_name} is / "
    "are interested as a partner, manager, employee or guarantor, or",
    "f) a company (incl. holding company or subsidiary incl. step-down subsidiary) of which any of the directors or the "
    "spouse or dependent / minor child of directors of {bank_name} is / are a director, managing agent, manager, "
    "employee or guarantor or they hold substantial interest, or",
    "g) an individual in respect of whom any of directors of {bank_name} / spouse or dependent / minor child of "
    "directors is / are a partner or guarantor, or",
    "h) an entity in which {bank_name}'s promoters and their relatives or shareholders with shareholding of 10% or more "
    "in the paid-up equity capital of {bank_name}, have significant influence or control (as defined under Accounting "
    "Standards Ind AS 28 and Ind AS 110).",
]
RELATED_IF_YES = "If answer to any of the above is \"Yes\", please furnish the following details:"
RELATED_CLOSE = (
    "I / We declare that I / We am / are making the aforesaid declaration solemnly and sincerely believing the same to "
    "be true and complete, and in case of any change on the above, I / We shall immediately inform {bank_name} of such "
    "change. I/we understand any suppression or misstatement of facts may lead to actions incl. recall of the "
    "facilities availed or regulatory reporting."
)
RELATED_SIGN_LINE = "Signature of the Applicant / Co-Applicant / Guarantor / Authorized Signatory (Name, Designation)"
DEFINITIONS = [
    "Definitions as per Reserve Bank of India (Commercial Banks - Credit Risk Management) - Directions, 2025 as amended "
    "from time to time:",
    "'Related Person' shall mean a person, and the relatives of such a person, where the person: a. is either a "
    "promoter or a director, or a KMP of {bank_name}; or b. owns more than 5% of paid-up equity share capital of "
    "{bank_name} or can, either singly or jointly, exercise more than 5% of the voting rights of {bank_name} on account "
    "of either ownership or voting agreement or through shareholders' agreement or through any other arrangement; or "
    "c. can, through an agreement with {bank_name}, nominate a director to its Board; or d. is either singly or "
    "jointly, in control of {bank_name}.",
    "'Reciprocally Related Person (RRP)' means an individual who is either: a. a director (including independent "
    "director / Nominee director appointed by the Government or RBI or a statutory body) of another Bank (other than "
    "{bank_name}) commercial bank, or an All-India Financial Institution (AIFI), or a scheduled cooperative bank, or a "
    "subsidiary of a commercial bank (including {bank_name}); or b. a trustee of a mutual fund or an alternate "
    "investment fund established by any of these regulated entities (Commercial Bank / AIFI / Scheduled Co-op Bank / "
    "Subsidiary of Commercial Bank); or c. a relative of such a director or a trustee.",
    "'Related Party' shall mean a person, or any of the following entities in which a related person or a reciprocally "
    "related person is: a. a partner, manager, KMP, director or a promoter; or b. a shareholder with more than 10% of "
    "equity capital; or c. having control, whether singly or jointly with another person; or d. in a position to "
    "control > 20% of voting rights on account of ownership or through a voting agreement or through any other "
    "arrangement; or e. having the power to nominate a director to its board; or f. in a position to influence the "
    "entity to act on their advice, direction, or instruction; or g. a guarantor or a surety; or h. is a trustee or an "
    "author or a beneficiary and where the entity is in the form of a private trust, or i. is related as a subsidiary "
    "or a parent company or a holding company or a joint venture.",
    "Provided that: i) nothing in sub-clause (a) above shall apply in cases where the authority to nominate a director "
    "arises exclusively from a lending or financing arrangement. ii) nothing in sub-clause (f) above shall apply to "
    "the advice, directions or instructions given in a professional capacity. iii) Government of India / State "
    "Government-owned or controlled entities shall not be treated as related parties to a government-owned bank just "
    "by virtue of the fact that the Government has the common ownership or control of such entities.",
    "'Key Managerial Personnel (KMP)' of a bank shall have the same meaning as defined in Section 2(51) of the "
    "Companies Act, 2013. 'Specified Employee' with respect to {bank_name} is any employee at {bank_name} with a "
    "designation President and above. 'Relative' with regard to a natural person shall have the same meaning as "
    "defined in Section 2(77) of the Companies Act, 2013 and rules framed therein. 'Substantial interest' shall have "
    "the same meaning as assigned to it in Section 5(ne) of the Banking Regulation Act, 1949.",
]

ACK_TEXT = (
    "1. {bank_name} will Convey its decision within 30 working days from the date of receipt of the application "
    "provided the application is complete in all respects and is submitted along with all the documents as per 'check "
    "list' provided in the application for loan and/or any additional documents as may be required by the bank for "
    "proper appraisal of the application. The computation of 30 days shall start from the day on which all documents "
    "required for proper appraisal of the application are provided by the Customer to the bank."
)

FATCA_TEXT_INDIA = "I am a tax resident of India and not resident of any other country OR"
FATCA_TEXT_OTHER = "I am a tax resident of the country/ies mentioned in the table below:"
FATCA_INTRO = ("Please indicate the county/ies in which the entity is a resident for tax purposes and the "
               "associated Tax Number below:")
FATCA_NOTE_HASH = "#To also include USA, where the individual is citizen/green card holder of USA"
FATCA_NOTE_PCT = "% In case Tax Identification number is not available, kindly provide functional equivalent"
FATCA_CERT = (
    "FATCA-CRS Certification: I have understood the information requirements of this form (read along with the "
    "FATCA/CRS instructions and Terms & Conditions) and hereby confirm that the information provided by me/us on this "
    "Form is true, correct, and complete and hereby accept the same."
)

CHARGES_LEFT = [
    ["Processing Fees Charges ", ("f", "pf"), " % of the loan amount+GST (As applicable)"],
    ["Rate of interest @ ", ("f", "roi"), " % per annum"],
    ["Penal Charge : Financial default - 8% p.a. above applicable interest rate (subject to the aggregate not "
     "exceeding 24% per instance)"],
    ["• There should be no capitalization of Penal Charges."],
    ["• Financial Default includes all types of payment or financial defaults/irregularities with respect to the "
     "loan account"],
    ["Material Terms & Conditions: Non-payment of interest / installment on due date"],
    ["Foreclosure charges shall be levied on principal outstanding."],
    ["Disbursed Loan Amount less than Rs 10 lacs: Up to 36 paid EMIs = 3%; After 36 paid EMIs = 2%"],
]
CHARGES_MID = [
    "Disbursed Loan Amount greater than or equals to Rs 10 Lacs",
    "• Own Funds: Charges if closure from own funds before 12 paid EMIs: 3% of Principal Outstanding; Charges if "
    "closure from own funds after 12 paid EMIs: Nil",
    "• Other than Own Funds: Charges if the closure is not from own funds: Up to 36 paid EMIs = 3%; After 36 paid "
    "EMIs = 2%",
    "No Lock-in period for foreclosing the loan.",
    "Part-payment charges: Part Payment charges shall be levied on the amount being prepaid. Up to 36 paid EMIs = 3%; "
    "After 36 paid EMIs = 2%. Excluding pre- EMI/broken period interest.",
    "Customer will be allowed to pre-pay up to 25% of principal outstanding, every year during the loan tenure without "
    "any charges after completion of 12 paid EMIs. There shall be a gap of 12 paid EMI's between two such part "
    "payments.",
    "Customer will be allowed for part payment if: 1. Part payment is done before completion of 12 paid EMIs 2. Part "
    "payment is greater than 25% of principal outstanding in a year. 3. Gap between 2 part payments is less than 12 "
    "paid EMIs.",
    "No Lock-in period for making part payment of the loan",
]
CHARGES_RIGHT = [
    "Instruction/Instrument Return charges: 339/- per instance of dishonour of Cheque/ SI/ECS/NACH debit instruction + "
    "GST as applicable",
    "Cheque/Instrument Swap charges: 500/-+GST (As applicable) per instance",
    "Duplicate statement issuance charges / charges on customer-initiated request for copies of documents: 250/-+GST "
    "(As applicable) per instance",
    "Duplicate No Dues Certificate/NOC",
    "Duplicate Amortization schedule issuance charges: 50/- per instance per set + GST (As applicable)",
    "Credit Information Companies (CIC's) Report Issuance Charges: 250/-+GST (As applicable) per document set",
    "Stamp Duty Charges: As per State Stamp Act",
    "Loan Cancellation Charges (No of days, Applicable charges*): 0-3 days: Interest till the date of cancellation, "
    "Processing Fee, Stamp duty, other statutory charges (if applicable and when) and GST would not be "
    "waived/refunded# in case of loan cancellation. >3 days: It will be considered as pre-payment.",
    "*The above Charge is applicable for Full / Partial / DD cancellation cases as well",
]
CHARGES_STRIP = [
    "\"Goods and Services tax (GST) will be charged extra as per the applicable rates, on all the charges and fees "
    "(wherever GST is applicable)\"",
    "DOCUMENTATION*",
    "• Application form  • KYC document (Proof of Identity, Proof of Address)  • Income Document (latest 2 "
    "Salary Slip)  • Bank Statement (last three month bank statement)  • For NACH - 4 Security PDCs and for SI "
    "as repayment mode - 1 Security PDCs  • For PDC Repayment mode - PDCs equivalent to the tenure of loan to be "
    "provided",
    "#{bank_name} Ltd. may request for additional documents other than those requested above in connection with the "
    "application.",
]
EMI_GRID = [
    ("Last disbursal date", "EMI due date"),
    ("1st to 6th of Month", "10th of same month"),
    ("7th to 26th of Month", "5th of next month"),
    ("27th to 30th/31st of month", "10th of next month"),
]
