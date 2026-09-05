import sys
sys.path.insert(0, '.')
import pandas as pd
import numpy as np
import io
from datetime import datetime
from app.services.data_processor import process_uploaded_file, build_customer_profile
from app.services.risk_engine import run_risk_rules


# Test Dataset 1: Normal Customer (should produce 'No Activity Requiring Attention')
print('=== TESTING DATASET 1: Normal Customer ===')
normal_data = '''transaction_id,date,description,payee,amount,channel
TXN-001,2024-01-01,Grocery store,Super Market,500.0,UPI
TXN-002,2024-01-02,Gas station,Fuel Corp,2000.0,Card
TXN-003,2024-01-03,Restaurant,Dining,1500.0,UPI
TXN-004,2024-01-04,Transfer,Bank,5000.0,Bank Transfer
TXN-005,2024-01-05,Salary credit,Employer,15000.0,Bank Transfer
TXN-006,2024-01-06,Movie tickets,Cinema,800.0,UPI
TXN-007,2024-01-07,Pharmacy,Drug Store,120.0,Card
TXN-008,2024-01-08,Utility payment,Power Co,3000.0,Bank Transfer
TXN-009,2024-01-09,Coffee shop,Cafe,250.0,UPI
TXN-010,2024-01-10,Transfer to savings,Bank,2000.0,Bank Transfer
'''

df = pd.read_csv(io.StringIO(normal_data))
result = process_uploaded_file(type('obj', (object,), {'filename': 'normal.csv', 'file': io.BytesIO(df.to_csv().encode())})())
txns = result['transactions']
profile = build_customer_profile(txns)

print('Average amount:', profile.average_amount)
print('Typical range:', profile.typical_range)
print('Channels:', profile.channel_distribution)

risk_results = run_risk_rules(profile, txns)
score = risk_results["score"]
level = risk_results["risk_level"]
findings_count = len(risk_results["findings"])
overall = "No Activity Requiring Attention" if score <= 30 else "Activity Requiring Investigation"
print('Risk score:', score)
print('Risk level:', level)
print('Findings:', findings_count)
print('Overall:', overall)
print()

# Test Dataset 2: Investigation Scenario
print('=== TESTING DATASET 2: Investigation Scenario ===')
investigation_data = '''transaction_id,date,description,payee,amount,channel
TXN-001,2024-03-01,Salary credit,Employer,15000.0,Bank Transfer
TXN-002,2024-03-15,Large transfer,Unknown Payee,250000.0,Bank Transfer
TXN-003,2024-03-16,Payment to new vendor,New Vendor,20000.0,Bank Transfer
TXN-004,2024-03-17,Payment to new vendor,New Vendor,30000.0,Bank Transfer
TXN-005,2024-03-18,Payment to new vendor,New Vendor,40000.0,Bank Transfer
TXN-006,2024-03-19,Odd hour transaction,Payee B,500.0,ATM
TXN-007,2024-03-20,Gas station,Fuel Corp,2000.0,Card
TXN-008,2024-03-21,Online purchase,Online Store,1500.0,UPI
'''

df2 = pd.read_csv(io.StringIO(investigation_data))
result2 = process_uploaded_file(type('obj', (object,), {'filename': 'investigation.csv', 'file': io.BytesIO(df2.to_csv().encode())})())
txns2 = result2['transactions']
profile2 = build_customer_profile(txns2)

print('Average amount:', profile2.average_amount)
print('Typical range:', profile2.typical_range)
print('New payees:', profile2.new_payees)

risk_results2 = run_risk_rules(profile2, txns2)
score2 = risk_results2["score"]
level2 = risk_results2["risk_level"]
findings_count2 = len(risk_results2["findings"])
overall2 = "No Activity Requiring Attention" if score2 <= 30 else "Activity Requiring Investigation"
print('Risk score:', score2)
print('Risk level:', level2)
print('Findings:', findings_count2)
for f in risk_results2['findings']:
    print(' -', f.rule_name, ':', f.explanation[:80])
print('Overall:', overall2)