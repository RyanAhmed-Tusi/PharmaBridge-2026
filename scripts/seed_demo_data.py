"""PharmaBridge Database Seed Script.

This script does TWO things:

  1. BASE DATA - realistic pre-existing data that makes the app feel
     like it has been running for 3-4 weeks. When you open PharmaBridge
     for the first time, it looks like a live, active system rather than
     an empty shell.

  2. DEMO DATA - the specific Cardivex/fatigue scenario used in the
     judge presentation. These rows are timed to trigger a convergent
     signal the moment you click "Run Bridge Scan."

Run this ONCE before your demo:
    cd pharmabridge/scripts
    python seed_demo_data.py

It is safe to run multiple times - it checks for existing data and
skips records that are already present.

Usage:
    python seed_demo_data.py           # Both base + demo data
    python seed_demo_data.py --demo    # Demo data only
    python seed_demo_data.py --base    # Base data only
    python seed_demo_data.py --wipe    # Clear ALL data then re-seed everything
"""

import os
import random
import sys
from datetime import date, datetime, timedelta, timezone

# Use the Windows / OS native certificate store for TLS — required on
# corporate networks where outbound HTTPS is SSL-inspected.
import truststore

truststore.inject_into_ssl()

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from supabase import create_client  # noqa: E402

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in backend/.env")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────


def ago(days: float = 0, hours: float = 0, minutes: float = 0) -> str:
    """Returns an ISO timestamp N days/hours/minutes in the past."""
    dt = datetime.now(timezone.utc) - timedelta(
        days=days, hours=hours, minutes=minutes
    )
    return dt.isoformat()


def rand_ago(min_days: float = 1, max_days: float = 30) -> str:
    return ago(days=random.uniform(min_days, max_days))


def wipe_all() -> None:
    print("Wiping all data...")
    for table in (
        "convergent_signals",
        "care_team_alerts",
        "patient_conversations",
        "patient_profiles",
        "msl_insights",
        "kol_profiles",
    ):
        try:
            supabase.table(table).delete().neq(
                "id", "00000000-0000-0000-0000-000000000000"
            ).execute()
        except Exception as e:  # noqa: BLE001
            print(f"  WARN: could not wipe {table}: {e}")
    print("  Done.\n")


def already_seeded(table: str, check_field: str, check_value: str) -> bool:
    result = (
        supabase.table(table).select("id").eq(check_field, check_value).execute()
    )
    return bool(result.data)


# ─────────────────────────────────────────────────────────────────
# (1) BASE MSL INSIGHTS - weeks of realistic background intelligence
# ─────────────────────────────────────────────────────────────────

BASE_MSL_INSIGHTS = [
    # ── Neurovax (positive drug - advocacy and evidence gaps) ──
    {
        "msl_name": "Aisha Okafor",
        "msl_region": "East Africa",
        "kol_name": "Prof. Samuel Mbeki",
        "kol_institution": "University of Nairobi Medical Center",
        "kol_specialty": "Neurology",
        "drug_name": "Neurovax",
        "indication": "Alzheimer's Prevention",
        "insight_type": "Advocacy",
        "description": "Prof. Mbeki expressed strong enthusiasm for Neurovax's mechanism of action. He has observed measurable cognitive stabilisation in 4 early-stage patients over 6 months and is keen to co-author a case series. He offered to present at the East African Neurology Congress in October.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Positive",
        "debrief_summary": "Prof. Mbeki is an outstanding Neurovax advocate. Case series opportunity identified. Conference speaker confirmed.",
        "created_at": rand_ago(25, 28),
    },
    {
        "msl_name": "David Kim",
        "msl_region": "West Coast",
        "kol_name": "Dr. Linda Yoshida",
        "kol_institution": "UCSF Memory and Aging Center",
        "kol_specialty": "Neuropsychiatry",
        "drug_name": "Neurovax",
        "indication": "Alzheimer's Prevention",
        "insight_type": "Evidence Gap",
        "description": "Dr. Yoshida asked whether there is any data on Neurovax in patients with early-onset Alzheimer's (under 65). Current label is for 65+. She has a patient cohort of 40 and believes earlier intervention may show stronger outcomes.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "R&D",
        "kol_sentiment": "Positive",
        "debrief_summary": "Evidence gap identified: no Neurovax data in under-65 early-onset population. Potential R&D study opportunity.",
        "created_at": rand_ago(18, 22),
    },
    {
        "msl_name": "Priya Krishnamurthy",
        "msl_region": "Southeast",
        "kol_name": "Dr. Marcus Webb",
        "kol_institution": "Emory Brain Health Center",
        "kol_specialty": "Neurology",
        "drug_name": "Neurovax",
        "indication": "Alzheimer's Prevention",
        "insight_type": "Label Question",
        "description": "Dr. Webb questioned the dosing interval for Neurovax in patients with moderate renal impairment. The label suggests standard dosing but he has seen slower clearance in two elderly patients and wants dose adjustment guidance.",
        "confidence": "Medium",
        "urgency": "Normal",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Neutral",
        "debrief_summary": "Renal dosing guidance requested for Neurovax. Two patients showing slower clearance.",
        "created_at": rand_ago(10, 14),
    },
    # ── Hypertex (solid performer - competitor threats) ──
    {
        "msl_name": "James Chen",
        "msl_region": "North America",
        "kol_name": "Dr. Patricia O'Brien",
        "kol_institution": "Mayo Clinic - Cardiology",
        "kol_specialty": "Cardiology",
        "drug_name": "Hypertex",
        "indication": "Hypertension",
        "insight_type": "Advocacy",
        "description": "Dr. O'Brien considers Hypertex her first-line choice for hypertension in patients over 50. She highlighted the once-daily dosing and the consistent BP reduction data in the HEARTSTRONG trial. Will recommend it at the upcoming ACC regional meeting.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Positive",
        "debrief_summary": "Strong Hypertex advocacy from Mayo. ACC conference opportunity confirmed.",
        "created_at": rand_ago(20, 24),
    },
    {
        "msl_name": "Sarah Williams",
        "msl_region": "Mid-Atlantic",
        "kol_name": "Dr. Jonathan Reeves",
        "kol_institution": "Johns Hopkins - Hypertension Clinic",
        "kol_specialty": "Internal Medicine",
        "drug_name": "Hypertex",
        "indication": "Hypertension",
        "insight_type": "Competitive Intel",
        "description": "Dr. Reeves mentioned that the new PharmaRiv ARB (RivaTen) is being aggressively marketed in his hospital with a 40% co-pay reduction card. Three of his residents are defaulting to RivaTen for new patients. He personally prefers Hypertex but expressed concern about the cost disparity.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "Commercial",
        "kol_sentiment": "Neutral",
        "debrief_summary": "RivaTen competitive pressure growing at JHH. Cost disparity driving resident prescribing behaviour.",
        "created_at": rand_ago(8, 12),
    },
    {
        "msl_name": "Lena Fischer",
        "msl_region": "Europe - DACH",
        "kol_name": "Prof. Hans Zimmermann",
        "kol_institution": "Charité Universitätsmedizin Berlin",
        "kol_specialty": "Cardiology",
        "drug_name": "Hypertex",
        "indication": "Hypertension",
        "insight_type": "Unmet Need",
        "description": "Prof. Zimmermann noted a significant unmet need in hypertension management for patients with concurrent Type 2 diabetes. He questioned whether Hypertex has interaction data with GLP-1 agonists, which are increasingly used alongside antihypertensives in this population.",
        "confidence": "High",
        "urgency": "Normal",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Neutral",
        "debrief_summary": "Hypertex + GLP-1 agonist interaction data requested. Growing clinical need.",
        "created_at": rand_ago(5, 8),
    },
    # ── Cardivex (DEMO DRUG - negative signal building, fatigue emerging) ──
    {
        "msl_name": "David Kim",
        "msl_region": "West Coast",
        "kol_name": "Dr. Samuel Rodriguez",
        "kol_institution": "Stanford Medical Center",
        "kol_specialty": "Neurology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Competitive Intel",
        "description": "Dr. Rodriguez highlighted the APEX trial, in which CompetitorDrug-X showed a 1.2% superior HbA1c reduction in patients over 60. He is considering switching several stable patients to CompetitorDrug-X and asked for any comparative head-to-head data.",
        "confidence": "Medium",
        "urgency": "Normal",
        "routing_target": "Commercial",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "APEX trial data creating competitive headwinds for Cardivex in elderly diabetics. Need head-to-head response.",
        "created_at": rand_ago(22, 26),
    },
    {
        "msl_name": "Aisha Okafor",
        "msl_region": "East Africa",
        "kol_name": "Dr. Fatima Al-Rashid",
        "kol_institution": "Aga Khan University Hospital - Nairobi",
        "kol_specialty": "Endocrinology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Advocacy",
        "description": "Dr. Al-Rashid reported excellent HbA1c outcomes in 15 patients on Cardivex over 9 months. She highlighted patient satisfaction with the once-daily dosing and minimal GI side effects. Strong advocate - willing to speak at regional diabetes conferences.",
        "confidence": "High",
        "urgency": "Low",
        "routing_target": "Medical Affairs",
        "kol_sentiment": "Positive",
        "debrief_summary": "Strong Cardivex advocate in East Africa. Positive patient outcomes reported. Conference speaker opportunity.",
        "created_at": rand_ago(15, 18),
    },
    # ── OncoBind (oncology - serious safety signal early) ──
    {
        "msl_name": "Lena Fischer",
        "msl_region": "Europe - DACH",
        "kol_name": "Prof. Klaus Brandt",
        "kol_institution": "University Hospital Munich - Oncology",
        "kol_specialty": "Oncology",
        "drug_name": "OncoBind",
        "indication": "Non-Small Cell Lung Cancer",
        "insight_type": "Safety Observation",
        "description": "Prof. Brandt reported two patients developing grade 3 hepatotoxicity within 8 weeks of initiating OncoBind at the standard 200mg dose. Both patients required hospitalisation and dose suspension. He has reported to the local ethics committee and requests urgent medical monitoring guidance.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Negative",
        "debrief_summary": "URGENT: Grade 3 hepatotoxicity in 2 OncoBind patients. PV review mandatory. Prof. Brandt requests immediate medical guidance.",
        "created_at": rand_ago(3, 5),
    },
    {
        "msl_name": "Sarah Williams",
        "msl_region": "Mid-Atlantic",
        "kol_name": "Dr. Carol Zhang",
        "kol_institution": "Memorial Sloan Kettering",
        "kol_specialty": "Oncology",
        "drug_name": "OncoBind",
        "indication": "Non-Small Cell Lung Cancer",
        "insight_type": "Safety Observation",
        "description": "Dr. Zhang observed elevated liver enzymes (AST/ALT > 3x ULN) in one patient on OncoBind, flagged as a possible early hepatotoxicity signal. Patient is under close monitoring. She asks whether other centres have reported similar findings.",
        "confidence": "Medium",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "Possible hepatotoxicity signal at MSK - one patient with elevated liver enzymes on OncoBind.",
        "created_at": rand_ago(1, 2),
    },
]


# ─────────────────────────────────────────────────────────────────
# (2) BASE PATIENT PROFILES (10 patients across 3 drugs)
# ─────────────────────────────────────────────────────────────────

BASE_PATIENTS = [
    # ── Hypertex ──
    {
        "patient_name": "Mary Chen",
        "patient_code": "PT-003",
        "age_group": "31-45",
        "condition": "Hypertension",
        "drug_name": "Hypertex",
        "drug_start_date": "2025-03-10",
        "care_team_email": "dr.chen@example.com",
        "adherence_rate": 72.0,
        "consecutive_days_tracked": 21,
        "primary_barrier": "Forgetfulness",
        "barrier_confidence": "High",
        "barrier_details": "Patient consistently forgets the evening dose when her schedule changes. Morning doses are reliable.",
        "barrier_detected_at": ago(days=7),
        "current_strategy": "Routine anchoring - linking evening dose to dinner time",
        "intervention_stage": 2,
        "last_checkin_at": ago(days=1, hours=2),
    },
    {
        "patient_name": "George Osei",
        "patient_code": "PT-006",
        "age_group": "60+",
        "condition": "Hypertension",
        "drug_name": "Hypertex",
        "drug_start_date": "2025-01-05",
        "care_team_email": "dr.osei@example.com",
        "adherence_rate": 90.5,
        "consecutive_days_tracked": 35,
        "primary_barrier": "Unknown",
        "barrier_confidence": "Low",
        "barrier_details": None,
        "barrier_detected_at": None,
        "current_strategy": "General support - high adherence, monitoring",
        "intervention_stage": 1,
        "last_checkin_at": ago(days=1),
    },
    {
        "patient_name": "Nadia Patel",
        "patient_code": "PT-007",
        "age_group": "31-45",
        "condition": "Hypertension",
        "drug_name": "Hypertex",
        "drug_start_date": "2025-04-01",
        "care_team_email": "dr.sharma@example.com",
        "adherence_rate": 61.0,
        "consecutive_days_tracked": 14,
        "primary_barrier": "Belief",
        "barrier_confidence": "Medium",
        "barrier_details": "Patient feels her BP is now normal and questions whether she still needs daily medication.",
        "barrier_detected_at": ago(days=4),
        "current_strategy": "Motivational interview scheduled - disease progression education needed",
        "intervention_stage": 2,
        "last_checkin_at": ago(hours=18),
    },
    # ── Neurovax ──
    {
        "patient_name": "Eleanor Voss",
        "patient_code": "PT-008",
        "age_group": "60+",
        "condition": "Alzheimer's Prevention",
        "drug_name": "Neurovax",
        "drug_start_date": "2025-02-20",
        "care_team_email": "dr.webb@example.com",
        "adherence_rate": 95.0,
        "consecutive_days_tracked": 42,
        "primary_barrier": "Unknown",
        "barrier_confidence": "Low",
        "barrier_details": None,
        "barrier_detected_at": None,
        "current_strategy": "General support - excellent adherence",
        "intervention_stage": 1,
        "last_checkin_at": ago(hours=6),
    },
    {
        "patient_name": "Arthur Fitzwilliam",
        "patient_code": "PT-009",
        "age_group": "60+",
        "condition": "Alzheimer's Prevention",
        "drug_name": "Neurovax",
        "drug_start_date": "2025-01-12",
        "care_team_email": "dr.webb@example.com",
        "adherence_rate": 78.5,
        "consecutive_days_tracked": 30,
        "primary_barrier": "Complexity",
        "barrier_confidence": "High",
        "barrier_details": "Patient is on 6 other medications and frequently confuses Neurovax with his statin. Has missed 3 doses in the last 2 weeks.",
        "barrier_detected_at": ago(days=9),
        "current_strategy": "Medication reconciliation - pill organiser recommended, care team notified",
        "intervention_stage": 3,
        "last_checkin_at": ago(days=1, hours=4),
    },
    {
        "patient_name": "Iris Nakamura",
        "patient_code": "PT-010",
        "age_group": "46-60",
        "condition": "Alzheimer's Prevention",
        "drug_name": "Neurovax",
        "drug_start_date": "2025-03-25",
        "care_team_email": "dr.yoshida@example.com",
        "adherence_rate": 55.0,
        "consecutive_days_tracked": 18,
        "primary_barrier": "Access",
        "barrier_confidence": "High",
        "barrier_details": "Patient lives 45 minutes from the nearest pharmacy. She runs out between refills and cannot always make the trip. Has missed 8 doses in 3 weeks.",
        "barrier_detected_at": ago(days=5),
        "current_strategy": "Mail-order pharmacy referral initiated - care team alerted",
        "intervention_stage": 4,
        "last_checkin_at": ago(hours=22),
    },
    # ── Cardivex patients (DEMO DRUG - 3 with Side Effect barrier) ──
    {
        "patient_name": "Sarah Johnson",
        "patient_code": "PT-001",
        "age_group": "46-60",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-01-15",
        "care_team_email": "dr.patel@example.com",
        "adherence_rate": 68.5,
        "consecutive_days_tracked": 14,
        "primary_barrier": "Side Effect",
        "barrier_confidence": "High",
        "barrier_details": "Patient reports persistent afternoon fatigue correlated with lunchtime Cardivex dosing. Pattern confirmed over 3 consecutive days.",
        "barrier_detected_at": ago(days=3),
        "current_strategy": "Side effect investigation - dose timing adjustment pending care team review",
        "intervention_stage": 3,
        "last_checkin_at": ago(hours=20),
    },
    {
        "patient_name": "Robert Martinez",
        "patient_code": "PT-002",
        "age_group": "60+",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-02-01",
        "care_team_email": "dr.torres@example.com",
        "adherence_rate": 45.0,
        "consecutive_days_tracked": 10,
        "primary_barrier": "Side Effect",
        "barrier_confidence": "High",
        "barrier_details": "Significant fatigue and reduced energy levels. Patient discontinued medication 4 days ago without informing physician.",
        "barrier_detected_at": ago(days=5),
        "current_strategy": "Urgent care team referral - medication discontinuation detected",
        "intervention_stage": 4,
        "last_checkin_at": ago(days=1, hours=8),
    },
    {
        "patient_name": "James Williams",
        "patient_code": "PT-004",
        "age_group": "60+",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-01-20",
        "care_team_email": "dr.morris@example.com",
        "adherence_rate": 74.0,
        "consecutive_days_tracked": 18,
        "primary_barrier": "Side Effect",
        "barrier_confidence": "Medium",
        "barrier_details": "Patient mentions feeling 'run down' in the afternoons. Hesitant to attribute it directly to Cardivex - needs follow-up session to confirm.",
        "barrier_detected_at": ago(days=4),
        "current_strategy": "Side effect monitoring - one more session to confirm fatigue pattern",
        "intervention_stage": 2,
        "last_checkin_at": ago(hours=14),
    },
    {
        "patient_name": "Lisa Thompson",
        "patient_code": "PT-005",
        "age_group": "46-60",
        "condition": "Type 2 Diabetes",
        "drug_name": "Cardivex",
        "drug_start_date": "2025-02-15",
        "care_team_email": "dr.smith@example.com",
        "adherence_rate": 91.0,
        "consecutive_days_tracked": 28,
        "primary_barrier": "Unknown",
        "barrier_confidence": "Low",
        "barrier_details": None,
        "barrier_detected_at": None,
        "current_strategy": "General support - monitoring adherence trend",
        "intervention_stage": 1,
        "last_checkin_at": ago(hours=5),
    },
]


# ─────────────────────────────────────────────────────────────────
# (3) DEMO MSL INSIGHTS (the 3 Cardivex fatigue reports)
# ─────────────────────────────────────────────────────────────────

DEMO_MSL_INSIGHTS = [
    {
        "msl_name": "James Chen",
        "msl_region": "North America",
        "kol_name": "Dr. Rachel Patel",
        "kol_institution": "Johns Hopkins Medical Center",
        "kol_specialty": "Endocrinology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Patel reported two patients experiencing significant afternoon fatigue 3-4 weeks after initiating Cardivex. She suspects a link to the lunchtime dosing schedule and asked whether timing adjustment guidance is available. She also noted one patient considered stopping treatment.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "Dr. Patel raised fatigue safety concerns for two Cardivex patients. Lunchtime dosing may be implicated. One patient near discontinuation.",
        "created_at": ago(days=7, hours=3),
    },
    {
        "msl_name": "Sarah Williams",
        "msl_region": "Mid-Atlantic",
        "kol_name": "Dr. Michael Torres",
        "kol_institution": "Mayo Clinic",
        "kol_specialty": "Cardiology",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Torres mentioned two elderly patients who discontinued Cardivex citing fatigue and reduced energy levels. He is exploring evening dosing as a mitigation strategy and would like any pharmacokinetic data on time-of-day effects for Cardivex.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Skeptical",
        "debrief_summary": "Fatigue-driven discontinuation in elderly Cardivex patients at Mayo. Evening dosing question raised.",
        "created_at": ago(days=5, hours=1),
    },
    {
        "msl_name": "Priya Krishnamurthy",
        "msl_region": "Southeast",
        "kol_name": "Dr. Helen Morris",
        "kol_institution": "Emory University Hospital",
        "kol_specialty": "Internal Medicine",
        "drug_name": "Cardivex",
        "indication": "Type 2 Diabetes",
        "insight_type": "Safety Observation",
        "description": "Dr. Morris flagged fatigue as a recurring patient complaint specifically in patients over 65 on Cardivex. She asked whether post-marketing surveillance data shows age-specific fatigue patterns and whether a dose reduction protocol exists for this population.",
        "confidence": "High",
        "urgency": "Urgent",
        "routing_target": "Pharmacovigilance",
        "kol_sentiment": "Neutral",
        "debrief_summary": "Third regional fatigue signal for Cardivex in elderly patients. Evidence Gap: no age-stratified fatigue safety data available.",
        "created_at": ago(days=2, hours=5),
    },
]


# ─────────────────────────────────────────────────────────────────
# (4) DEMO PATIENT CONVERSATIONS - Sarah's 3-day fatigue arc (PT-001)
# ─────────────────────────────────────────────────────────────────

DEMO_CONVERSATIONS_PT001 = [
    # Day 1 - vague fatigue mention
    {
        "role": "companion",
        "message": "Good morning, Sarah! How are you feeling today? Did you take your Cardivex this morning?",
        "session_date": str(date.today() - timedelta(days=3)),
        "session_number": 1,
    },
    {
        "role": "patient",
        "message": "I took it. But I've been really tired in the afternoons lately. Not sure if it's the medication or just stress.",
        "session_date": str(date.today() - timedelta(days=3)),
        "session_number": 1,
        "barrier_signal": "Side Effect",
        "signal_strength": "Weak",
    },
    {
        "role": "companion",
        "message": "I'm glad you took it. The tiredness is worth paying attention to - does it happen at around the same time each day?",
        "session_date": str(date.today() - timedelta(days=3)),
        "session_number": 1,
    },
    {
        "role": "patient",
        "message": "Yes, always around 2-3pm. That's funny because I take my pill at lunch.",
        "session_date": str(date.today() - timedelta(days=3)),
        "session_number": 1,
        "barrier_signal": "Side Effect",
        "signal_strength": "Strong",
    },
    {
        "role": "companion",
        "message": "That timing is really useful to know. Many patients notice this with lunchtime dosing. Let's keep an eye on this tomorrow - and if it happens again, let me know.",
        "session_date": str(date.today() - timedelta(days=3)),
        "session_number": 1,
    },
    # Day 2 - fatigue confirmed again
    {
        "role": "companion",
        "message": "Good morning Sarah! How did yesterday afternoon go - did the tiredness come back?",
        "session_date": str(date.today() - timedelta(days=2)),
        "session_number": 2,
    },
    {
        "role": "patient",
        "message": "Yes, it happened again. About an hour after lunch I just felt so heavy and could barely concentrate. Did take my pill though.",
        "session_date": str(date.today() - timedelta(days=2)),
        "session_number": 2,
        "barrier_signal": "Side Effect",
        "signal_strength": "Strong",
    },
    {
        "role": "companion",
        "message": "Thank you for telling me, and I'm glad you still took your medication. The afternoon fatigue pattern is consistent now over two days. I want to make sure your care team knows about this - are you okay with me flagging it?",
        "session_date": str(date.today() - timedelta(days=2)),
        "session_number": 2,
    },
    {
        "role": "patient",
        "message": "Please do. I thought I just had to deal with it but it's affecting my work.",
        "session_date": str(date.today() - timedelta(days=2)),
        "session_number": 2,
    },
    {
        "role": "companion",
        "message": "You absolutely don't have to just deal with it. I've notified your care team and they'll review whether a timing change might help. I'll check in again tomorrow to see how you're doing.",
        "session_date": str(date.today() - timedelta(days=2)),
        "session_number": 2,
    },
    # Day 3 - patient considering stopping
    {
        "role": "companion",
        "message": "Good morning Sarah! Did you take your Cardivex today?",
        "session_date": str(date.today() - timedelta(days=1)),
        "session_number": 3,
    },
    {
        "role": "patient",
        "message": "I did, but honestly I'm thinking of stopping. The fatigue is just too much. My productivity at work has dropped completely.",
        "session_date": str(date.today() - timedelta(days=1)),
        "session_number": 3,
        "barrier_signal": "Side Effect",
        "signal_strength": "Strong",
    },
    {
        "role": "companion",
        "message": "I really hear you, and I'm sorry this is affecting your work. Please don't stop without speaking to your doctor first - stopping suddenly can be risky. Your care team has been alerted and they're reviewing your case right now. Can we make a deal to wait for their call before making any changes?",
        "session_date": str(date.today() - timedelta(days=1)),
        "session_number": 3,
    },
    {
        "role": "patient",
        "message": "Okay, I'll wait. But please make sure someone calls me soon.",
        "session_date": str(date.today() - timedelta(days=1)),
        "session_number": 3,
    },
    {
        "role": "companion",
        "message": "I've flagged this as urgent for your care team. They should be in touch today. You're doing the right thing by staying on it for now. I'll check in tomorrow morning.",
        "session_date": str(date.today() - timedelta(days=1)),
        "session_number": 3,
    },
]


# ─────────────────────────────────────────────────────────────────
# (5) KOL PROFILES (background relationship data)
# ─────────────────────────────────────────────────────────────────

KOL_PROFILES = [
    {
        "kol_name": "Dr. Rachel Patel",
        "institution": "Johns Hopkins Medical Center",
        "specialty": "Endocrinology",
        "region": "North America",
        "drug_name": "Cardivex",
        "sentiment_trend": "Skeptical",
        "total_interactions": 3,
        "last_interaction_at": ago(days=7),
    },
    {
        "kol_name": "Dr. Michael Torres",
        "institution": "Mayo Clinic",
        "specialty": "Cardiology",
        "region": "Mid-Atlantic",
        "drug_name": "Cardivex",
        "sentiment_trend": "Skeptical",
        "total_interactions": 2,
        "last_interaction_at": ago(days=5),
    },
    {
        "kol_name": "Dr. Helen Morris",
        "institution": "Emory University Hospital",
        "specialty": "Internal Medicine",
        "region": "Southeast",
        "drug_name": "Cardivex",
        "sentiment_trend": "Neutral",
        "total_interactions": 2,
        "last_interaction_at": ago(days=2),
    },
    {
        "kol_name": "Prof. Samuel Mbeki",
        "institution": "University of Nairobi Medical Center",
        "specialty": "Neurology",
        "region": "East Africa",
        "drug_name": "Neurovax",
        "sentiment_trend": "Positive",
        "total_interactions": 4,
        "last_interaction_at": ago(days=25),
    },
    {
        "kol_name": "Dr. Patricia O'Brien",
        "institution": "Mayo Clinic - Cardiology",
        "specialty": "Cardiology",
        "region": "North America",
        "drug_name": "Hypertex",
        "sentiment_trend": "Positive",
        "total_interactions": 5,
        "last_interaction_at": ago(days=20),
    },
    {
        "kol_name": "Prof. Klaus Brandt",
        "institution": "University Hospital Munich - Oncology",
        "specialty": "Oncology",
        "region": "Europe - DACH",
        "drug_name": "OncoBind",
        "sentiment_trend": "Negative",
        "total_interactions": 1,
        "last_interaction_at": ago(days=3),
    },
]


# ─────────────────────────────────────────────────────────────────
# (6) HISTORICAL RESOLVED CONVERGENT SIGNAL (lived-in feel)
# ─────────────────────────────────────────────────────────────────

HISTORICAL_SIGNAL = {
    "drug_name": "Hypertex",
    "signal_type": "Tolerability",
    "confidence": "Medium",
    "velocity": "Declining",
    "msl_evidence": (
        "Total MSL reports: 2\n"
        "- [Label Question] Dosing question for patients with concurrent GLP-1 therapy (Medium, Europe - DACH)\n"
        "- [Competitive Intel] RivaTen co-pay card driving new prescriber behaviour (High, Mid-Atlantic)"
    ),
    "patient_evidence": (
        "Total patients tracked: 3\n"
        "Average adherence rate: 74.5%\n"
        "Barrier breakdown: Forgetfulness: 1 patients (33%), Belief: 1 patients (33%), Unknown: 1 patients (33%)"
    ),
    "msl_insight_count": 2,
    "patient_count": 3,
    "signal_summary": "Two MSL reports from different regions flagged adherence-related concerns for Hypertex - one on drug interactions (GLP-1 co-medication) and one on competitive pricing pressure. Patient data showed moderate adherence dip with two confirmed barriers (Forgetfulness and Belief). The signal was moderate confidence and resolved after Medical Affairs issued updated dosing guidance and Commercial introduced a co-pay assistance card.",
    "recommended_actions": [
        "Issue updated GLP-1 co-administration guidance to MSL team",
        "Activate co-pay card program in Mid-Atlantic region",
        "Schedule KOL advisory board to review competitive positioning",
    ],
    "status": "Resolved",
    "resolved_at": ago(days=10),
    "resolved_by": "Medical Affairs + Commercial",
    "created_at": ago(days=18),
}


# ─────────────────────────────────────────────────────────────────
# MAIN RUNNERS
# ─────────────────────────────────────────────────────────────────


def seed_base() -> dict:
    print("Seeding base MSL insights...")
    count = 0
    for insight in BASE_MSL_INSIGHTS:
        if not already_seeded(
            "msl_insights", "description", insight["description"][:60]
        ):
            r = supabase.table("msl_insights").insert(insight).execute()
            if r.data:
                count += 1
                print(
                    f"  [+] [{insight['insight_type']}] {insight['kol_name']} re: {insight['drug_name']}"
                )
    print(f"   Added {count} new base insights (skipped duplicates)\n")

    print("Seeding patient profiles...")
    patient_ids: dict[str, str] = {}
    for patient in BASE_PATIENTS:
        if already_seeded("patient_profiles", "patient_code", patient["patient_code"]):
            r = (
                supabase.table("patient_profiles")
                .select("id")
                .eq("patient_code", patient["patient_code"])
                .single()
                .execute()
            )
            if r.data:
                patient_ids[patient["patient_code"]] = r.data["id"]
            print(
                f"  [=] {patient['patient_name']} ({patient['patient_code']}) already exists - skipped"
            )
        else:
            r = supabase.table("patient_profiles").insert(patient).execute()
            if r.data:
                patient_ids[patient["patient_code"]] = r.data[0]["id"]
                print(
                    f"  [+] {patient['patient_name']} ({patient['patient_code']}) - {patient['primary_barrier']} barrier"
                )
    print()

    print("Seeding KOL profiles...")
    for kol in KOL_PROFILES:
        try:
            supabase.table("kol_profiles").upsert(
                kol, on_conflict="kol_name,drug_name"
            ).execute()
            print(
                f"  [+] {kol['kol_name']} - {kol['drug_name']} ({kol['sentiment_trend']})"
            )
        except Exception as e:  # noqa: BLE001
            print(f"  WARN KOL profile error: {e}")
    print()

    print("Seeding historical convergent signal...")
    if not already_seeded("convergent_signals", "drug_name", "Hypertex"):
        supabase.table("convergent_signals").insert(HISTORICAL_SIGNAL).execute()
        print("  [+] Historical Hypertex signal (Resolved) - shows system has been running")
    else:
        print("  [=] Historical signal already exists")
    print()

    return patient_ids


def seed_demo(patient_ids: dict[str, str] | None = None) -> None:
    print("Seeding DEMO data (Cardivex fatigue convergent signal)...")

    print("   MSL fatigue reports...")
    for insight in DEMO_MSL_INSIGHTS:
        if not already_seeded(
            "msl_insights", "description", insight["description"][:60]
        ):
            supabase.table("msl_insights").insert(insight).execute()
            print(
                f"  [+] [{insight['insight_type']}] {insight['msl_name']} - {insight['kol_name']}"
            )
        else:
            print(f"  [=] {insight['kol_name']} insight already exists")

    if not patient_ids:
        patient_ids = {}
        for code in ("PT-001", "PT-002", "PT-004"):
            r = (
                supabase.table("patient_profiles")
                .select("id")
                .eq("patient_code", code)
                .execute()
            )
            if r.data:
                patient_ids[code] = r.data[0]["id"]

    if "PT-001" in patient_ids:
        existing_convs = (
            supabase.table("patient_conversations")
            .select("id")
            .eq("patient_id", patient_ids["PT-001"])
            .execute()
        )
        if not existing_convs.data:
            print("   Seeding Sarah's 3-day conversation arc...")
            for conv in DEMO_CONVERSATIONS_PT001:
                conv_copy = dict(conv)
                conv_copy["patient_id"] = patient_ids["PT-001"]
                supabase.table("patient_conversations").insert(conv_copy).execute()
            print("  [+] Sarah's conversation history (3-day fatigue arc)")
        else:
            print("  [=] Sarah's conversations already exist")

    for code, patient_name, drug, barrier_details in (
        (
            "PT-001",
            "Sarah Johnson",
            "Cardivex",
            "Consistent afternoon fatigue correlated with lunchtime dosing. Pattern confirmed over 3 days. Patient considering stopping medication.",
        ),
        (
            "PT-002",
            "Robert Martinez",
            "Cardivex",
            "Patient has discontinued Cardivex without physician notification. Fatigue cited as primary reason.",
        ),
    ):
        if code in patient_ids:
            existing = (
                supabase.table("care_team_alerts")
                .select("id")
                .eq("patient_id", patient_ids[code])
                .execute()
            )
            if not existing.data:
                supabase.table("care_team_alerts").insert(
                    {
                        "patient_id": patient_ids[code],
                        "patient_code": code,
                        "drug_name": drug,
                        "alert_type": "Barrier Detected",
                        "alert_message": f"Patient {patient_name} ({code}): {barrier_details}",
                        "barrier_type": "Side Effect",
                        "barrier_details": barrier_details,
                        "recommended_action": "Schedule clinical review of dose timing. Consider evening dosing trial. Pharmacovigilance report if pattern persists.",
                        "status": "Pending",
                    }
                ).execute()
                print(f"  [+] Care team alert for {patient_name} ({code})")
    print()


def main() -> None:
    args = sys.argv[1:]

    if "--wipe" in args:
        confirm = input(
            "WARNING: This will DELETE ALL PharmaBridge data. Type 'yes' to confirm: "
        )
        if confirm.strip().lower() != "yes":
            print("Aborted.")
            return
        wipe_all()

    if "--demo" in args:
        seed_demo()
    elif "--base" in args:
        seed_base()
    else:
        patient_ids = seed_base()
        seed_demo(patient_ids)

    print("-" * 55)
    print("PharmaBridge database is ready!\n")
    print("What's in the database:")
    print("   Base MSL insights  ->  10 insights across 4 drugs")
    print("   Demo MSL insights  ->  3 Cardivex fatigue reports")
    print("   Patients           ->  10 enrolled (various barriers)")
    print("   KOL profiles       ->  6 relationship records")
    print("   Historical signal  ->  1 resolved Hypertex signal")
    print("   Conversations      ->  Sarah's 3-day fatigue arc")
    print("   Care team alerts   ->  2 pending (PT-001, PT-002)")
    print()
    print("Next step: Open the HQ Dashboard and click 'Run Bridge Scan'")
    print(
        "   This will detect the Cardivex convergent signal from the live data above."
    )


if __name__ == "__main__":
    main()
