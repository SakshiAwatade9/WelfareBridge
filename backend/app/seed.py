from .extensions import db, bcrypt
from .models import User, Scheme


def seed_admin():
    if User.query.filter_by(email="admin@welfarebridge.gov.in").first():
        return
    admin = User(
        name="Platform Admin",
        email="admin@welfarebridge.gov.in",
        password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
        role="ADMIN",
    )
    db.session.add(admin)
    db.session.commit()
    print(">>> Seeded demo admin account: admin@welfarebridge.gov.in / admin123")


def seed_schemes():
    if Scheme.query.count() > 0:
        return

    schemes_data = [
        dict(name="National Education Support Scheme", department="Ministry of Education", category="Education",
             benefit="Annual scholarship of Rs. 25,000 for tuition fees and study material.",
             description="Provides direct financial assistance to students from low-income households to reduce dropout rates and support continued education.",
             min_age=16, max_age=30, max_income=250000, state="All India", occupation="student", gender="any", senior_only=False,
             documents="Aadhaar Card, Income Certificate, College Admission Proof, Bank Passbook",
             deadline="31 Oct 2026", apply_link="https://scholarships.gov.in"),

        dict(name="Direct Farm Income Support", department="Ministry of Agriculture", category="Agriculture",
             benefit="Rs. 6,000 per year paid directly to the farmer's bank account in three instalments.",
             description="Income support for landholding farmer families to help meet input costs for agricultural activities.",
             min_age=None, max_age=None, max_income=None, state="All India", occupation="farmer", gender="any", senior_only=False,
             documents="Aadhaar Card, Land Records, Bank Passbook",
             deadline="Open year-round", apply_link="https://pmkisan.gov.in"),

        dict(name="Girl Child Education Grant", department="Maharashtra Women & Child Development", category="Education",
             benefit="One-time grant of Rs. 15,000 to support school enrollment and retention.",
             description="State-level grant to encourage families to enrol and retain girl children in school through secondary level.",
             min_age=5, max_age=18, max_income=None, state="Maharashtra", occupation="any", gender="female", senior_only=False,
             documents="Aadhaar Card, Birth Certificate, School Enrollment Certificate",
             deadline="15 Sep 2026", apply_link="https://www.womenchild.maharashtra.gov.in"),

        dict(name="Employment Guarantee Wage Scheme", department="Ministry of Rural Development", category="Employment",
             benefit="Up to 100 days of guaranteed wage employment per household per year.",
             description="Provides a legal guarantee of wage employment to rural households willing to do unskilled manual work.",
             min_age=18, max_age=None, max_income=None, state="All India", occupation="unemployed", gender="any", senior_only=False,
             documents="Aadhaar Card, Job Card, Bank Passbook",
             deadline="Open year-round", apply_link="https://nrega.nic.in"),

        dict(name="Affordable Housing Interest Subsidy", department="Ministry of Housing & Urban Affairs", category="Housing",
             benefit="Interest subsidy on home loans of up to Rs. 2.6 lakh over the loan tenure.",
             description="Reduces the effective interest burden on home loans for economically weaker and lower-income households.",
             min_age=21, max_age=None, max_income=300000, state="All India", occupation="any", gender="any", senior_only=False,
             documents="Aadhaar Card, Income Certificate, Property Documents, Bank Statement",
             deadline="31 Dec 2026", apply_link="https://pmaymis.gov.in"),

        dict(name="Senior Citizen Pension Scheme", department="Ministry of Social Justice", category="Social Security",
             benefit="Monthly pension of Rs. 1,000 credited directly to a bank or post office account.",
             description="Provides a basic monthly income to senior citizens from economically vulnerable households.",
             min_age=60, max_age=None, max_income=200000, state="All India", occupation="any", gender="any", senior_only=True,
             documents="Aadhaar Card, Age Proof, Income Certificate, Bank Passbook",
             deadline="Open year-round", apply_link="https://nsap.dord.gov.in"),

        dict(name="Women Entrepreneurship Support Grant", department="Ministry of Skill Development", category="Employment",
             benefit="Collateral-free loan of up to Rs. 10 lakh for setting up or expanding a small business.",
             description="Encourages self-employment among women by providing accessible, collateral-free credit.",
             min_age=18, max_age=55, max_income=500000, state="All India", occupation="any", gender="female", senior_only=False,
             documents="Aadhaar Card, Business Plan, Bank Passbook, Income Certificate",
             deadline="30 Nov 2026", apply_link="https://www.mudra.org.in"),

        dict(name="Universal Health Insurance Scheme", department="Ministry of Health & Family Welfare", category="Healthcare",
             benefit="Cashless hospital treatment up to Rs. 5 lakh per family per year.",
             description="Provides health cover for secondary and tertiary care hospitalisation to economically vulnerable families.",
             min_age=None, max_age=None, max_income=250000, state="All India", occupation="any", gender="any", senior_only=False,
             documents="Aadhaar Card, Income Certificate, Ration Card",
             deadline="Open year-round", apply_link="https://pmjay.gov.in"),

        dict(name="Skill Development Training Program", department="Ministry of Skill Development", category="Employment",
             benefit="Free vocational training with an industry-recognised certification on completion.",
             description="Short-term skill training aligned with industry demand, aimed at improving employability of unemployed youth.",
             min_age=18, max_age=35, max_income=None, state="All India", occupation="unemployed", gender="any", senior_only=False,
             documents="Aadhaar Card, Educational Certificate, Bank Passbook",
             deadline="15 Jan 2027", apply_link="https://pmkvyofficial.org"),

        dict(name="Farmer Crop Insurance Scheme", department="Ministry of Agriculture", category="Agriculture",
             benefit="Compensation for crop loss due to natural calamities, pests, or disease.",
             description="Provides financial support to farmers in the event of crop failure, stabilising farm income.",
             min_age=None, max_age=None, max_income=None, state="All India", occupation="farmer", gender="any", senior_only=False,
             documents="Aadhaar Card, Land Records, Sowing Certificate",
             deadline="31 Jul 2026", apply_link="https://pmfby.gov.in"),

        dict(name="Disability Support Allowance", department="Ministry of Social Justice", category="Social Security",
             benefit="Monthly allowance of Rs. 1,500 along with support for assistive devices.",
             description="Financial and equipment support for persons with disabilities from low-income households.",
             min_age=None, max_age=None, max_income=300000, state="All India", occupation="any", gender="any", senior_only=False,
             documents="Aadhaar Card, Disability Certificate, Income Certificate",
             deadline="Open year-round", apply_link="https://disabilityaffairs.gov.in"),

        dict(name="Maharashtra Student Laptop Scheme", department="Maharashtra Higher & Technical Education", category="Education",
             benefit="Free laptop for students pursuing higher education in government-recognised institutions.",
             description="Supports digital access for higher-education students from economically weaker sections in Maharashtra.",
             min_age=17, max_age=26, max_income=100000, state="Maharashtra", occupation="student", gender="any", senior_only=False,
             documents="Aadhaar Card, College ID, Income Certificate",
             deadline="20 Sep 2026", apply_link="https://mahadbt.maharashtra.gov.in"),

        dict(name="Rural Housing Development Scheme", department="Ministry of Rural Development", category="Housing",
             benefit="Grant of Rs. 1.2 lakh for construction of a pucca house.",
             description="Provides financial assistance for house construction to rural households living in kutcha or dilapidated houses.",
             min_age=18, max_age=None, max_income=150000, state="All India", occupation="any", gender="any", senior_only=False,
             documents="Aadhaar Card, Land Ownership Proof, Income Certificate, Bank Passbook",
             deadline="Open year-round", apply_link="https://pmayg.nic.in"),

        dict(name="Maternity Benefit Scheme", department="Ministry of Women & Child Development", category="Healthcare",
             benefit="Cash benefit of Rs. 5,000 for the first live birth, paid in instalments.",
             description="Partial compensation for wage loss during pregnancy and after childbirth, and to encourage adequate nutrition and care.",
             min_age=19, max_age=45, max_income=None, state="All India", occupation="any", gender="female", senior_only=False,
             documents="Aadhaar Card, Pregnancy Certificate, Bank Passbook",
             deadline="Open year-round", apply_link="https://pmmvy.wcd.gov.in"),
    ]

    for data in schemes_data:
        db.session.add(Scheme(**data))

    db.session.commit()
    print(f">>> Seeded {len(schemes_data)} sample welfare schemes.")


def run_seed():
    seed_admin()
    seed_schemes()
