import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import from the app package
from app.services.data_processor import build_customer_profile
from app.services.risk_engine import (
    rule_unusually_large_transfer,
    rule_new_payee_burst,
    rule_odd_hours,
    rule_pattern_deviation,
    run_risk_rules,
)
from app.models.transaction import Transaction


def test_rule_unusually_large_transfer_normal():
    """Test Rule 1 with normal transactions - should find no large transfers."""
    # Create normal transactions
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Grocery store", payee="Super Market", amount=500.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 2), time="14:00",
            description="Gas station", payee="Fuel Corp", amount=2000.0,
            channel="Card", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    results = rule_unusually_large_transfer(txns, profile)
    
    # With normal amounts, should have no results
    assert len(results) == 0, f"Expected 0 results, got {len(results)}"
    print("✅ Test 1 passed: Normal transactions - no large transfers flagged")


def test_rule_unusually_large_transfer_large():
    """Test Rule 1 with an unusually large transaction."""
    # Create transactions with one very large one, plus many normal ones
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Grocery store", payee="Super Market", amount=500.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 2), time="14:00",
            description="Gas station", payee="Fuel Corp", amount=2000.0,
            channel="Card", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-3", date=datetime(2024, 1, 3), time="09:00",
            description="Restaurant", payee="Dining", amount=1500.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-4", date=datetime(2024, 1, 4), time="16:00",
            description="Transfer", payee="Bank", amount=5000.0,
            channel="Bank Transfer", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-5", date=datetime(2024, 1, 15), time="14:00",
            description="Large transfer", payee="Unknown Payee", amount=50000.0,
            channel="Bank Transfer", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    results = rule_unusually_large_transfer(txns, profile)
    
    # Should detect the large transaction
    assert len(results) > 0, "Expected at least 1 result for large transaction"
    assert results[0].rule_name == "Unusually Large Transfer"
    print("✅ Test 2 passed: Large transaction flagged correctly")


def test_rule_new_payee_burst():
    """Test Rule 2: burst of payments to new payee."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Payment 1", payee="New Vendor", amount=20000.0,
            channel="Bank Transfer", is_new_payee=True,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 2), time="14:00",
            description="Payment 2", payee="New Vendor", amount=30000.0,
            channel="Bank Transfer", is_new_payee=True,
        ),
        Transaction(
            transaction_id="TXN-3", date=datetime(2024, 1, 3), time="16:00",
            description="Payment 3", payee="New Vendor", amount=40000.0,
            channel="Bank Transfer", is_new_payee=True,
        ),
    ]
    
    profile = build_customer_profile(txns)
    results = rule_new_payee_burst(txns, profile)
    
    # Should detect the burst
    assert len(results) > 0, f"Expected at least 1 result for payee burst, got {len(results)}"
    assert results[0].rule_name == "New Payee Burst"
    print("✅ Test 3 passed: New payee burst detected")


def test_rule_odd_hours():
    """Test Rule 3: odd-hours transactions."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="09:00",
            description="Day transaction", payee="Payee A", amount=1000.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 1), time="03:00",
            description="Odd-hours transaction", payee="Payee B", amount=500.0,
            channel="ATM", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    results = rule_odd_hours(txns, profile)
    
    # Should detect the odd-hours transaction
    assert len(results) > 0, f"Expected at least 1 result for odd hours, got {len(results)}"
    assert results[0].rule_name == "Odd-Hours Activity"
    print("✅ Test 4 passed: Odd-hours transaction detected")


def test_rule_pattern_deviation():
    """Test Rule 4: pattern deviations."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Normal transaction", payee="Known Payee", amount=1000.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 1), time="10:00",
            description="Normal transaction 2", payee="Known Payee", amount=1500.0,
            channel="UPI", is_new_payee=False,
        ),
Transaction(
            transaction_id="TXN-3", date=datetime(2024, 1, 1), time="10:00",
            description="Normal transaction 3", payee="Known Payee", amount=1200.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-4", date=datetime(2024, 1, 1), time="10:00",
            description="Unusual channel", payee="Known Payee", amount=50000.0,
            channel="ATM", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-5", date=datetime(2024, 1, 1), time="14:00",
            description="Large amount", payee="Known Payee", amount=100000.0,
            channel="UPI", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    results = rule_pattern_deviation(txns, profile)
    
    # Should detect the unusual channel/amount deviation
    assert len(results) > 0, f"Expected at least 1 result for pattern deviation, got {len(results)}"
    print("✅ Test 5 passed: Pattern deviation detected")


def test_customer_profile_creation():
    """Test customer profile building."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Grocery", payee="Super Market", amount=500.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 2), time="14:00",
            description="Gas", payee="Fuel", amount=2000.0,
            channel="Card", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-3", date=datetime(2024, 1, 3), time="16:00",
            description="Transfer", payee="Bank", amount=10000.0,
            channel="Bank Transfer", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    
    assert profile.average_amount > 0
    assert profile.median_amount > 0
    assert profile.min_amount > 0
    assert profile.max_amount > 0
    assert profile.std_dev >= 0
    print(f"✅ Test 6 passed: Profile created - avg: ₹{profile.average_amount:.2f}, range: ₹{profile.typical_range[0]:.0f}-₹{profile.typical_range[1]:.0f}")


def test_run_risk_rules_end_to_end():
    """Test the full risk engine."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Grocery", payee="Super Market", amount=500.0,
            channel="UPI", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-2", date=datetime(2024, 1, 15), time="03:00",
            description="Large transfer", payee="Unknown", amount=50000.0,
            channel="Bank Transfer", is_new_payee=False,
        ),
        Transaction(
            transaction_id="TXN-3", date=datetime(2024, 1, 2), time="14:00",
            description="New payee payment", payee="New Vendor", amount=25000.0,
            channel="Bank Transfer", is_new_payee=True,
        ),
    ]
    
    profile = build_customer_profile(txns)
    risk_results = run_risk_rules(profile, txns)
    
    assert "score" in risk_results
    assert "risk_level" in risk_results
    assert "findings" in risk_results
    assert 0 <= risk_results["score"] <= 100
    print(f"✅ Test 7 passed: Full risk engine - score: {risk_results['score']}, level: {risk_results['risk_level']}, findings: {len(risk_results['findings'])}")


def test_edge_case_limited_history():
    """Test edge case with very limited transaction history."""
    txns = [
        Transaction(
            transaction_id="TXN-1", date=datetime(2024, 1, 1), time="10:00",
            description="Single transaction", payee="Payee A", amount=1000.0,
            channel="UPI", is_new_payee=False,
        ),
    ]
    
    profile = build_customer_profile(txns)
    risk_results = run_risk_rules(profile, txns)
    
    # With limited history, should handle gracefully
    assert "score" in risk_results
    assert "risk_level" in risk_results
    print("✅ Test 8 passed: Edge case with limited history handled gracefully")


if __name__ == "__main__":
    test_rule_unusually_large_transfer_normal()
    test_rule_unusually_large_transfer_large()
    test_rule_new_payee_burst()
    test_rule_odd_hours()
    test_rule_pattern_deviation()
    test_customer_profile_creation()
    test_run_risk_rules_end_to_end()
    test_edge_case_limited_history()
    print("\n🎉 All tests passed!")