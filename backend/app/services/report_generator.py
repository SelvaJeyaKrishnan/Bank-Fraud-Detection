import json
from datetime import datetime
from typing import List, Dict, Any
from app.models.transaction import Transaction, InvestigationFinding
from app.services.connection_engine import connect_transactions


def generate_report(behavior: dict, risk_results: dict, connections: dict) -> str:
    """Generate investigation report ID and store the findings."""
    # Create a report ID based on timestamp
    report_id = f"REPORT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Determine overall finding
    score = risk_results.get("score", 0)
    findings = risk_results.get("findings", [])
    
    if score <= 30 or not findings:
        overall_finding = "✅ No Activity Requiring Attention"
        finding_text = "No activity requiring attention was identified based on the configured risk rules and the customer's established transaction behavior."
    else:
        overall_finding = "⚠️ Activity Requiring Investigation"
        finding_text = "One or more transaction patterns differ materially from the customer's established behavior and should be reviewed by an investigator."
    
    # Generate investigation findings
    investigation_findings = []
    
    # Sort findings by risk level and score
    sorted_findings = sorted(findings, key=lambda f: f.priority_score_contribution, reverse=True)
    
    for i, finding in enumerate(sorted_findings, 1):
        # Get connected activity
        connected = connections.get("groups", [])
        
        # Determine investigator questions
        questions = []
        if finding.rule_name == "Unusually Large Transfer":
            questions = [
                "Was the transaction authorized?",
                "Is the payee known to the customer?",
                "Was the device or login behavior unusual?",
                "Were there other transactions immediately before or after this activity?"
            ]
        elif finding.rule_name == "New Payee Burst":
            questions = [
                "Was the new payee added by the customer or someone else?",
                "Are these transactions consistent with the customer's normal activity patterns?",
                "Was the device or login behavior unusual?",
                "Were there other transactions to the same payee outside this burst period?"
            ]
        elif finding.rule_name == "Odd-Hours Activity":
            questions = [
                "Was the customer aware of making these transactions?",
                "Was the device or login behavior unusual?",
                "Is there a legitimate reason for the timing (e.g., travel, shift work)?",
                "Were there other transactions around the same time?"
            ]
        else:
            questions = [
                "Was the transaction authorized?",
                "Is the payee known to the customer?",
                "Was the device or login behavior unusual?",
                "Were there other transactions immediately before or after the activity?"
            ]
        
        investigation_finding = InvestigationFinding(
            finding_number=i,
            rule_triggered=finding.rule_name,
            risk_level=finding.risk_level,
            priority_score=finding.priority_score_contribution,
            transactions=finding.related_transactions,
            why_flagged=finding.explanation,
            normal_behaviour=f"Previous transfers typically ranged between ₹{behavior.get('min_amount', 0):.0f} and ₹{behavior.get('max_amount', 0):.0f}.",
            connected_activity=connected,
            investigator_questions=questions,
        )
        
        investigation_findings.append(investigation_finding)
    
    # Store report data (in a full app, this would be a database)
    report_data = {
        "report_id": report_id,
        "overall_finding": overall_finding,
        "finding_text": finding_text,
        "investigation_findings": [f.dict() for f in investigation_findings],
        "risk_score": score,
        "risk_level": risk_results.get("risk_level", "Low"),
        "behavior_profile": behavior,
        "connections": connections,
        "generated_at": datetime.now().isoformat(),
    }
    
    # In a real app, save to database here
    # save_report(report_id, report_data)
    
    return report_id


def get_report_by_id(report_id: str) -> dict:
    """Retrieve a generated report by ID."""
    # In a real app, this would query the database
    return {
        "report_id": report_id,
        "status": "generated",
        "message": "Report retrieved from storage",
    }