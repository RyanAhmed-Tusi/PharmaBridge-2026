"""Bridge Layer API routes.

POST /api/bridge/scan        -> scan both streams, persist any new convergent signals
GET  /api/bridge/signals     -> list convergent signals (filterable by status)
GET  /api/bridge/alerts      -> list care-team alerts
"""

from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from services.claude_bridge import scan_for_convergent_signals
from services.supabase_client import supabase

router = APIRouter()


def _thirty_days_ago_iso() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()


def build_msl_summary(insights: list) -> str:
    """Builds a readable summary of MSL insights for a drug."""
    if not insights:
        return "No MSL insights available."

    summary_parts = []
    for i in insights:
        summary_parts.append(
            f"- [{i.get('insight_type')}] {i.get('description')} "
            f"(Confidence: {i.get('confidence')}, Region: {i.get('msl_region', 'Unknown')})"
        )

    return f"Total MSL reports: {len(insights)}\n" + "\n".join(summary_parts)


def build_patient_summary(patients: list) -> str:
    """Builds a readable summary of patient barrier data for a drug."""
    if not patients:
        return "No patient data available."

    total = len(patients)
    barriers: dict[str, int] = {}
    total_adherence = 0.0

    for p in patients:
        barrier = p.get("primary_barrier") or "Unknown"
        barriers[barrier] = barriers.get(barrier, 0) + 1
        total_adherence += float(p.get("adherence_rate") or 100)

    avg_adherence = total_adherence / total if total > 0 else 100.0

    barrier_breakdown = ", ".join(
        [
            f"{b}: {c} patients ({round(c / total * 100)}%)"
            for b, c in barriers.items()
        ]
    )

    return (
        f"Total patients tracked: {total}\n"
        f"Average adherence rate: {round(avg_adherence, 1)}%\n"
        f"Barrier breakdown: {barrier_breakdown}"
    )


@router.post("/scan")
async def run_bridge_scan():
    """Scans both data streams and detects convergent signals.

    This is the core Bridge Layer function.
    """
    thirty_days_ago = _thirty_days_ago_iso()

    msl_result = (
        supabase.table("msl_insights")
        .select(
            "drug_name, insight_type, description, confidence, kol_sentiment, "
            "msl_region, created_at"
        )
        .gte("created_at", thirty_days_ago)
        .execute()
    )

    patient_result = (
        supabase.table("patient_profiles")
        .select(
            "drug_name, primary_barrier, barrier_confidence, "
            "adherence_rate, barrier_details"
        )
        .execute()
    )

    msl_by_drug: dict[str, list] = defaultdict(list)
    for insight in msl_result.data or []:
        if insight.get("drug_name"):
            msl_by_drug[insight["drug_name"]].append(insight)

    patient_by_drug: dict[str, list] = defaultdict(list)
    for patient in patient_result.data or []:
        if patient.get("drug_name"):
            patient_by_drug[patient["drug_name"]].append(patient)

    common_drugs = set(msl_by_drug.keys()) & set(patient_by_drug.keys())

    new_signals = []

    for drug_name in common_drugs:
        msl_insights = msl_by_drug[drug_name]
        patients = patient_by_drug[drug_name]

        if len(msl_insights) < 1 or len(patients) < 1:
            continue

        msl_summary = build_msl_summary(msl_insights)
        patient_summary = build_patient_summary(patients)

        signal_result = await scan_for_convergent_signals(
            drug_name, msl_summary, patient_summary
        )

        if not signal_result.get("convergent_signal_detected"):
            continue

        existing = (
            supabase.table("convergent_signals")
            .select("id")
            .eq("drug_name", drug_name)
            .eq("status", "Active")
            .execute()
        )
        if existing.data:
            continue

        db_record = {
            "drug_name": drug_name,
            "signal_type": signal_result.get("signal_type", "Unknown"),
            "confidence": signal_result.get("confidence", "Medium"),
            "velocity": signal_result.get("velocity", "Stable"),
            "msl_evidence": msl_summary,
            "patient_evidence": patient_summary,
            "msl_insight_count": len(msl_insights),
            "patient_count": len(patients),
            "signal_summary": signal_result.get("signal_summary", ""),
            "recommended_actions": signal_result.get("recommended_actions", []),
            "status": "Active",
        }
        result = supabase.table("convergent_signals").insert(db_record).execute()
        if result.data:
            new_signals.append(result.data[0])

    return {
        "success": True,
        "drugs_analyzed": len(common_drugs),
        "new_signals_detected": len(new_signals),
        "signals": new_signals,
        "message": (
            f"Bridge scan complete. Analyzed {len(common_drugs)} drugs. "
            f"Found {len(new_signals)} new convergent signals."
        ),
    }


@router.get("/signals")
async def get_convergent_signals(status: str = "Active"):
    """Returns convergent signals from the database, filtered by status."""
    result = (
        supabase.table("convergent_signals")
        .select("*")
        .eq("status", status)
        .order("created_at", desc=True)
        .execute()
    )
    return {"signals": result.data or [], "count": len(result.data or [])}


@router.get("/alerts")
async def get_care_team_alerts():
    """Returns the most recent care-team alerts."""
    result = (
        supabase.table("care_team_alerts")
        .select("*")
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )
    return {"alerts": result.data or []}
