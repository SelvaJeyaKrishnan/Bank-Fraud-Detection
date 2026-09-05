import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, time
from app.models.transaction import Transaction, CustomerProfile, RiskRuleResult
from app.services.data_processor import build_customer_profile


def analyze_customer_behavior(transactions: List[Transaction]) -> CustomerProfile:
    """Analyze customer transaction history and return behaviour profile."""
    if not transactions:
        return CustomerProfile()
    
    return build_customer_profile(transactions)


def detect_odd_hours(transactions: List[Transaction], profile: CustomerProfile, 
                     late_night_hour_threshold: int = 22) -> List[Transaction]:
    """Detect transactions occurring outside normal hours."""
    flagged = []
    
    # Use customer's established typical hours, with fallback default
    typical_start, typical_end = profile.typical_hours
    
    # If customer has very narrow typical hours, use configurable default
    if typical_start >= typical_end or (typical_end - typical_start) < 4:
        # Default: late night is after 10 PM and before 6 AM
        for t in transactions:
            if t.time:
                try:
                    hour = int(t.time.split(':')[0])
                    if hour >= late_night_hour_threshold or hour < 6:
                        flagged.append(t)
                except (ValueError, IndexError):
                    pass
    else:
        # Use customer's established hours
        for t in transactions:
            if t.time:
                try:
                    hour = int(t.time.split(':')[0])
                    if hour < typical_start or hour >= typical_end:
                        flagged.append(t)
                except (ValueError, IndexError):
                    pass
    
    return flagged


def calculate_risk_score(rules_results: List[RiskRuleResult]) -> float:
    """Calculate overall investigation priority score from 0-100."""
    total_score = sum(
        r.priority_score_contribution for r in rules_results 
        if r.priority_score_contribution > 0
    )
    return min(total_score, 100.0)


def determine_risk_level(score: float) -> str:
    """Determine risk level based on score."""
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    else:
        return "High"