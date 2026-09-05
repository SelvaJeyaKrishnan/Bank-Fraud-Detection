import re
from typing import Set, Optional
from datetime import datetime


def validate_transaction_data(df: any) -> list:
    """Validate transaction data and return list of errors."""
    errors = []
    
    required_columns = {'date', 'description', 'payee', 'amount', 'channel'}
    missing = required_columns - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")
    
    # Validate amount is numeric
    if 'amount' in df.columns:
        try:
            pd.to_numeric(df['amount'], errors='coerce')
        except Exception:
            errors.append("Amount column contains non-numeric values")
    
    # Validate date format
    if 'date' in df.columns:
        try:
            pd.to_datetime(df['date'], errors='coerce')
        except Exception:
            errors.append("Date column has invalid format")
    
    # Validate channel values
    valid_channels = {'Card', 'UPI', 'Bank Transfer', 'ATM', 'Online Banking', 'Mobile Banking'}
    if 'channel' in df.columns:
        invalid_channels = set(df['channel'].astype(str)) - valid_channels
        if invalid_channels:
            errors.append(f"Invalid channel values: {', '.join(invalid_channels)}")
    
    # Check for negative amounts
    amounts = pd.to_numeric(df['amount'], errors='coerce')
    if amounts.isna().any():
        errors.append("Some amounts could not be parsed as numbers")
    
    return errors


def format_amount(amount: float, currency: str = "₹") -> str:
    """Format amount with currency symbol."""
    return f"{currency}{amount:,.2f}"


def classify_risk_level(score: float) -> str:
    """Classify risk level from score 0-100."""
    if score <= 30:
        return "Low"
    elif score <= 60:
        return "Medium"
    else:
        return "High"


def is_valid_transaction_amount(amount: float) -> bool:
    """Check if amount is a valid positive number."""
    return isinstance(amount, (int, float)) and amount > 0