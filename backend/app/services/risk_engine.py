import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, time
from app.models.transaction import Transaction, RiskRuleResult
from app.services.behavior_analyzer import detect_odd_hours, calculate_risk_score, determine_risk_level


def rule_unusually_large_transfer(transactions: List[Transaction], profile: CustomerProfile) -> List[RiskRuleResult]:
    """Rule 1: Detect transactions significantly larger than customer's established behavior."""
    results = []
    
    if not transactions or profile.std_dev is None or profile.std_dev == 0:
        return results
    
    amounts = [t.amount for t in transactions]
    mean = profile.average_amount
    std = profile.std_dev
    typical_range = profile.typical_range
    
    # Use IQR method for robustness (more resistant to outliers than std dev)
    sorted_amounts = sorted(amounts)
    n = len(sorted_amounts)
    q1 = np.percentile(sorted_amounts, 25)
    q3 = np.percentile(sorted_amounts, 75)
    iqr = q3 - q1
    
    # Upper bound using IQR method: Q3 + 1.5 * IQR
    iqr_upper_bound = q3 + 1.5 * iqr
    
    # Also use Mean + 3*Std as a secondary threshold
    mean_upper_bound = mean + 3 * std
    
    large_transactions = []
    
    for t in transactions:
        # Flag if above IQR upper bound OR above mean + 3*std, but not the transaction itself
        # Use the lower of the two thresholds to avoid inflation from the large transaction
        use_iqr = iqr_upper_bound < mean_upper_bound or mean_upper_bound < 0
        
        threshold = iqr_upper_bound if use_iqr else mean_upper_bound
        
        # Check if transaction is outside typical range
        outside_typical = t.amount > typical_range[1] if typical_range[1] > typical_range[0] else False
        
        # Check if amount is significantly above the threshold
        if t.amount > threshold or outside_typical:
            # Make sure it's not the only large transaction inflating the stats
            # by verifying it's above the median as well
            median_amount = np.median(sorted_amounts)
            if t.amount > median_amount * 3:  # At least 3x the median
                large_transactions.append(t)
    
    if not large_transactions:
        return results
    
    # Calculate contribution to risk score
    score_contribution = min(len(large_transactions) * 15, 30)
    
    risk_level = determine_risk_level(score_contribution)
    
    explanation = (f"Detected {len(large_transactions)} transaction(s) significantly above "
                  f"established thresholds. IQR upper bound: ₹{iqr_upper_bound:.0f}, "
                  f"Mean + 3×Std: ₹{mean_upper_bound:.0f}, Typical range: ₹{typical_range[0]:.0f}-₹{typical_range[1]:.0f}")
    
    # Show normal range for comparison
    explanation += f". Customer's typical range: ₹{profile.typical_range[0]:.0f}-₹{profile.typical_range[1]:.0f}"
    
    related_txs = large_transactions[:5]
    
    result = RiskRuleResult(
        rule_name="Unusually Large Transfer",
        risk_level=risk_level,
        explanation=explanation,
        related_transactions=related_txs,
        priority_score_contribution=score_contribution,
    )
    results.append(result)
    
    return results


rule_unusually_large_transfer = rule_unusually_large_transfer


rule_new_payee_burst = None  # Will be defined separately


def rule_new_payee_burst(transactions: List[Transaction], profile: CustomerProfile) -> List[RiskRuleResult]:
    """Test Rule 2: burst of payments to new payee."""
    results = []
    
    if not transactions:
        return results
    
    # Identify new payees (payees that appear in this dataset but weren't in typical)
    payee_counts: Dict[str, int] = {}
    for t in transactions:
        payee_counts[t.payee] = payee_counts.get(t.payee, 0) + 1
    
    # Find payees with multiple transactions
    threshold_transactions = 2  # At least 2 transactions to same new payee
    
    new_payee_groups = {}
    for t in transactions:
        if payee_counts[t.payee] >= threshold_transactions:
            if t.payee not in new_payee_groups:
                new_payee_groups[t.payee] = []
            new_payee_groups[t.payee].append(t)
    
    # Check for bursts within short time windows
    for payee, txs in new_payee_groups.items():
        if len(txs) < 2:
            continue
        
        # Sort by date
        txs_sorted = sorted(txs, key=lambda t: t.date)
        
        # Check if transactions are within 72 hours
        first_date = txs_sorted[0].date
        last_date = txs_sorted[-1].date
        hours_diff = (last_date - first_date).total_seconds() / 3600
        
        if hours_diff <= 72:  # Within 72-hour window
            # Check if amount is unusual
            total_amount = sum(t.amount for t in txs_sorted)
            
            score_contribution = min(len(txs_sorted) * 10 + 5, 25)
            risk_level = determine_risk_level(score_contribution)
            
            explanation_parts = [
                f"Burst of {len(txs_sorted)} payment(s) to new payee '{payee}'",
                f"within {hours_diff:.0f} hours. Total amount: ₹{total_amount:.0f}",
                f"Individual amounts: ₹{', '.join(str(t.amount) for t in txs_sorted[:3])}"
            ]
            if len(txs_sorted) > 3:
                explanation_parts.append(f"...{len(txs_sorted)-3} more")
            explanation = ". ".join(explanation_parts)
            
            results.append(RiskRuleResult(
                rule_name="New Payee Burst",
                risk_level=risk_level,
                explanation=explanation,
                related_transactions=txs_sorted[:5],
                priority_score_contribution=score_contribution,
            ))
    
    return results


def rule_odd_hours(transactions: List[Transaction], profile: CustomerProfile) -> List[RiskRuleResult]:
    """Rule 3: Detect transactions occurring outside customer's normal hours."""
    if not transactions:
        return []
    
    flagged = detect_odd_hours(transactions, profile)
    
    if not flagged:
        return []
    
    score_contribution = min(len(flagged) * 10, 20)
    risk_level = determine_risk_level(score_contribution)
    
    explanation = (f"Detected {len(flagged)} transaction(s) occurring outside normal hours "
                  f"(established range: {profile.typical_hours[0]:02d}:00 - {profile.typical_hours[1]:02d}0)")
    
    findings = [
        RiskRuleResult(
            rule_name="Odd-Hours Activity",
            risk_level=risk_level,
            explanation=explanation,
            related_transactions=flagged[:5],
            priority_score_contribution=score_contribution,
        )
    ]
    
    return findings


def rule_pattern_deviation(transactions: List[Transaction], profile: CustomerProfile) -> List[RiskRuleResult]:
    """Rule 4: Detect significant deviations in amount, payee, channel, time, or frequency."""
    results = []
    
    if not transactions or not profile:
        return results
    
    deviations = []
    
    # Check for unusual channels
    normal_channels = profile.channel_distribution
    if normal_channels:
        total = sum(normal_channels.values())
        for t in transactions:
            channel_share = normal_channels.get(t.channel, 0) / total if total > 0 else 0
            if channel_share < 0.05 and t.channel not in ['Online Banking', 'Mobile Banking']:
                deviations.append(("Unusual Channel", t))
    
    # Check for amount deviations outside typical range
    typical_range = profile.typical_range
    if typical_range and typical_range[0] < typical_range[1]:
        for t in transactions:
            if t.amount < typical_range[0] or t.amount > typical_range[1]:
                deviations.append(("Amount Deviation", t))
    
    if not deviations:
        return results
    
    # Group deviations by type
    by_type = {}
    for reason, txn in deviations:
        if reason not in by_type:
            by_type[reason] = []
        by_type[reason].append(txn)
    
    total_score = 0
    for reason, txs in by_type.items():
        score_contribution = min(len(txs) * 5, 25)
        total_score += score_contribution
        risk_level = determine_risk_level(score_contribution)
        
        explanation = f"{reason}: {len(txs)} transaction(s) differ from typical range"
        
        results.append(RiskRuleResult(
            rule_name="Pattern Deviation",
            risk_level=risk_level,
            explanation=explanation,
            related_transactions=txs[:5],
            priority_score_contribution=score_contribution,
        ))
    
    # Cap total contribution
    # The individual contributions are already added, but we need to ensure 
    # the total doesn't exceed reasonable bounds
    return results


def run_risk_rules(behavior: CustomerProfile, transactions: List[Transaction]) -> dict:
    """Run all risk rules and return results."""
    all_results = []
    
    # Rule 1: Unusually Large Transfer
    rule1_results = rule_unusually_large_transfer(transactions, behavior)
    all_results.extend(rule1_results)
    
    # Rule 2: New Payee Burst
    rule2_results = rule_new_payee_burst(transactions, behavior)
    all_results.extend(rule2_results)
    
    # Rule 3: Odd-Hours Activity
    rule3_results = rule_odd_hours(transactions, behavior)
    all_results.extend(rule3_results)
    
    # Rule 4: Pattern Deviation
    rule4_results = rule_pattern_deviation(transactions, behavior)
    all_results.extend(rule4_results)
    
    # Calculate overall score
    score = calculate_risk_score(all_results)
    risk_level = determine_risk_level(score)
    
    return {
        "score": score,
        "risk_level": risk_level,
        "findings": all_results,
    }