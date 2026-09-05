from typing import List, Dict, Any
from app.models.transaction import Transaction


def connect_transactions(transactions: List[Transaction]) -> Dict[str, Any]:
    """Connect related transactions based on payee, time proximity, and multiple risk signals."""
    
    connections = {
        "groups": [],
        "signal_counts": {},
    }
    
    if not transactions:
        return connections
    
    # Group by same payee
    payee_groups: Dict[str, List[Transaction]] = {}
    for t in transactions:
        if t.payee not in payee_groups:
            payee_groups[t.payee] = []
        payee_groups[t.payee].append(t)
    
    same_payee_groups = []
    for payee, txs in payee_groups.items():
        if len(txs) >= 2:
            # Check time proximity
            txs_sorted = sorted(txs, key=lambda t: t.date)
            first_date = txs_sorted[0].date
            last_date = txs_sorted[-1].date
            hours_diff = (last_date - first_date).total_seconds() / 3600
            
            # Time proximity groups
            time_groups = []
            current_group = [txs_sorted[0]]
            
            for i in range(1, len(txs_sorted)):
                hours_since = (txs_sorted[i].date - txs_sorted[i-1].date).total_seconds() / 3600
                if hours_since <= 72:  # Within 72 hours
                    current_group.append(txs_sorted[i])
                else:
                    if len(current_group) >= 2:
                        time_groups.append(current_group)
                    current_group = [txs_sorted[i]]
            
            if len(current_group) >= 2:
                time_groups.append(current_group)
            
            if time_groups:
                same_payee_groups.extend(time_groups)
    
    connections["groups"].extend(same_payee_groups)
    
    # Identify multiple risk signals per transaction
    signal_count = 0
    signal_transactions = []
    
    for t in transactions:
        signals = []
        
        # Check if transaction appears in multiple rule contexts
        # Same payee count
        if t.payee in payee_groups and len(payee_groups[t.payee]) >= 2:
            signals.append("Same Payee")
        
        # Time proximity - within 24h of another flagged transaction
        # (will be determined by the rule engine)
        
        if signals:
            signal_count += len(signals)
            signal_transactions.append(t)
    
    if signal_transactions:
        connections["signal_counts"]["total_signal_transactions"] = len(signal_transactions)
        connections["signal_counts"]["signal_types"] = list(set(
            s for t in signal_transactions for s in ["Same Payee"]
        ))
    
    return connections