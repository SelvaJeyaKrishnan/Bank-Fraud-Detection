import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.transaction import Transaction, CustomerProfile


def process_uploaded_file(uploaded_file) -> Dict[str, Any]:
    """Process an uploaded CSV or Excel file and return transaction data."""
    filename = uploaded_file.filename
    
    if filename.endswith('.csv'):
        df = pd.read_csv(uploaded_file.file)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file.file)
    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel (.xlsx).")
    
    # Validate required columns
    required_columns = {'date', 'description', 'payee', 'amount', 'channel'}
    optional_columns = {'transaction_id', 'time'}
    
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    
    # Parse time if available
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
    else:
        df['time'] = None
    
    # Ensure amount is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Generate transaction IDs if not present
    if 'transaction_id' not in df.columns:
        df['transaction_id'] = [f"TXN-{i+1}" for i in range(len(df))]
    
    # Convert to Transaction objects
    transactions = []
    for _, row in df.iterrows():
        txn = Transaction(
            transaction_id=str(row['transaction_id']),
            date=row['date'],
            time=row['time'],
            description=str(row['description']),
            payee=str(row['payee']),
            amount=float(row['amount']),
            channel=str(row['channel']),
            is_new_payee=False,  # Will be set during analysis
        )
        transactions.append(txn)
    
    # Sort by date
    transactions.sort(key=lambda t: t.date)
    
    return {
        'transactions': transactions,
        'dataframe': df,
        'count': len(transactions),
    }


def build_customer_profile(transactions) -> CustomerProfile:
    """Build a customer behaviour profile from transactions."""
    amounts = [t.amount for t in transactions]
    
    if not amounts:
        return CustomerProfile()
    
    avg_amount = float(np.mean(amounts))
    median_amount = float(np.median(amounts))
    min_amount = float(min(amounts))
    max_amount = float(max(amounts))
    std_dev = float(np.std(amounts))
    
    # Typical range: mean ± 1 std dev, clamped to min-max
    lower = max(min_amount, avg_amount - std_dev) if std_dev > 0 else min_amount
    upper = min(max_amount, avg_amount + std_dev) if std_dev > 0 else max_amount
    
    # Channel distribution
    channel_dist = {}
    for ch in set(t.channel for t in transactions):
        channel_dist[ch] = sum(1 for t in transactions if t.channel == ch)
    
    # Typical hours
    hours = []
    for t in transactions:
        if t.time:
            try:
                h = int(t.time.split(':')[0])
                hours.append(h)
            except (ValueError, IndexError):
                pass
    
    typical_hours = (0, 23)
    if hours:
        typical_hours = (min(hours), max(hours))
    
    # Frequent payees
    payee_counts = {}
    for t in transactions:
        payee_counts[t.payee] = payee_counts.get(t.payee, 0) + 1
    frequent_payees = sorted(payee_counts.keys(), key=lambda p: payee_counts[p], reverse=True)[:10]
    
    return CustomerProfile(
        average_amount=avg_amount,
        median_amount=median_amount,
        min_amount=min_amount,
        max_amount=max_amount,
        std_dev=std_dev,
        typical_range=(lower, upper),
        frequent_payees=frequent_payees,
        typical_hours=typical_hours,
        channel_distribution=channel_dist,
    )