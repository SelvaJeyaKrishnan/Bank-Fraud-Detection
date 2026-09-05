# 🏦 Sentinel AI – Bank Fraud Investigation Assistant

## Overview

Sentinel AI is an AI-assisted investigation system for a bank's fraud desk. It analyzes a customer's transaction history to detect unusual patterns that may require investigator attention, using explainable risk rules that compare activity against the customer's own historical behavior.

**Critical Safety**: This system identifies activity requiring review. Final investigation decisions remain with authorized human investigators. Never states that fraud has occurred, never labels a customer as a fraudster, and never treats the risk score as a probability of fraud.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

### Installation

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173` (frontend) and `http://localhost:8000` (backend).

## 📁 Project Structure

```
banking-hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point with all endpoints
│   │   ├── models/
│   │   │   ├── transaction.py  # Transaction and Pydantic models
│   │   │   └── report.py       # Report models
│   │   ├── services/
│   │   │   ├── data_processor.py    # File upload and validation
│   │   │   ├── behavior_analyzer.py # Customer profile analysis
│   │   │   ├── risk_engine.py       # 4 risk detection rules
│   │   │   ├── connection_engine.py # Transaction connection logic
│   │   │   └── report_generator.py  # Investigation report generation
│   │   ├── rules/
│   │   │   ├── large_transfer.py    # Rule 1: Unusually Large Transfer
│   │   │   ├── new_payee_burst.py   # Rule 2: New Payee Burst
│   │   │   ├── odd_hours.py         # Rule 3: Odd-Hours Activity
│   │   │   └── pattern_deviation.py # Rule 4: Pattern Deviation
│   │   └── utils/
│   │       └── validators.py        # Data validation utilities
│   ├── tests/             # Test suite (8 test cases)
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.tsx        # Main app with routing
│   │   ├── main.tsx       # React entry point
│   │   ├── components/
│   │   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   │   ├── StatusCard.tsx       # Overall status display
│   │   │   ├── RiskScore.tsx        # Priority score display
│   │   │   ├── FindingCard.tsx      # Individual finding display
│   │   │   ├── TransactionTable.tsx # Transaction explorer table
│   │   │   └── UploadPanel.tsx      # File upload interface
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx          # Main dashboard view
│   │   │   ├── Upload.tsx           # File upload page
│   │   │   ├── Investigation.tsx    # Investigation report page
│   │   │   └── Transactions.tsx     # Transaction explorer page
│   │   └── services/
│   │       └── api.ts          # API service functions
│   ├── package.json         # npm dependencies
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── postcss.config.js    # PostCSS configuration
└── README.md              # This file
```

## 🎯 Core Features

### 1. Transaction History Upload

- **Supported formats**: CSV, Excel (.xlsx)
- **Required columns**: Date, Description, Payee, Amount, Channel
- **Optional columns**: Transaction ID, Time
- **Validation**: Useful error messages if required columns are missing

### 2. Customer Behaviour Baseline

Before detecting suspicious activity, the system analyzes the customer's historical behavior:

- **Transaction Amount Behaviour**: Average, median, min, max, standard deviation, typical range
- **Payee Behaviour**: Frequently used payees, new payees, transactions per payee, total amount per payee
- **Time Behaviour**: Typical transaction hours, odd-hours detection (customer-configured or default)
- **Channel Behaviour**: Card, UPI, Bank Transfer, ATM, Online Banking, Mobile Banking usage patterns

### 3. Risk Detection Rules (Explainable AI)

Four rule-based detection rules, each returning: rule name, risk level, explanation, related transactions, and why it differs from normal behavior.

**Rule 1: Unusually Large Transfer**
- Detects transactions significantly above the customer's established behavior
- Uses Mean + 3×Std Dev and IQR methods for robustness
- Avoids false positives for customers with naturally high-value transactions

**Rule 2: New Payee Burst**
- Detects multiple payments to a newly added payee within a short time window (configurable, default 72 hours)
- Groups connected transactions as one investigation finding

**Rule 3: Odd-Hours Activity**
- Detects transactions outside the customer's normal transaction hours
- Uses customer-established hours or configurable default (late-night: 10 PM - 6 AM)

**Rule 4: Pattern Deviation**
- Detects deviations in amount, payee, channel, time, or frequency
- Compares primarily against THIS customer's own historical behavior
- Does not flag globally unusual transactions

### 4. Transaction Connection Engine

Logic that connects related transactions:

- **Same Payee**: Multiple unusual transactions to the same new payee
- **Time Proximity**: Transactions within 1 hour, 24 hours, or 72 hours
- **Multiple Risk Signals**: A transaction becomes more important when multiple rules are triggered

### 5. Risk Scoring (0-100)

Explainable risk score, not a probability of fraud:

- **Low Priority**: 0-30
- **Medium Priority**: 31-60
- **High Priority**: 61-100

Score breakdown example:
```
Large Transfer: +30
New Payee Burst: +25
Odd Hours: +20

Investigation Priority Score: 75/100
```

### 6. Investigation Report

Generated report with the following structure:

**Overall Finding** (always first section):
- ✅ No Activity Requiring Attention
- ⚠️ Activity Requiring Investigation

**Finding Format** for each flagged pattern:
- Finding number and rule triggered
- Risk level (Low/Medium/High)
- Investigation priority score
- Transactions involved (table with ID, date, time, description, payee, amount, channel)
- Why it was flagged (explanation of deviation from normal behavior)
- Customer's normal behaviour (comparison data)
- Connected activity
- Investigator questions (authorization, payee knowledge, device/login behavior, related transactions)

### 7. Dashboard UI

Modern, premium banking/security theme with:

- **Sidebar**: Dashboard, Upload History, Investigation Reports, Rules & Settings
- **Header**: "Sentinel AI" / "Transaction Investigation Assistant"
- **Status Card**: Green (no activity) or Red (investigation required)
- **Risk Score**: Large circular score (0-100) with level label
- **Customer Behaviour Summary Cards**: Typical amount, most common channel, number of payees, typical hours
- **Risk Findings**: Expandable cards with priority level
- **Visualizations**: Transaction timeline, frequency over time, channel distribution, payee activity, highlighted unusual transactions

### 8. Transaction Explorer

Searchable and filterable transaction table:

- Search by description, payee, channel, or amount
- Filter by date, payee, channel
- Show flagged transactions
- Click to view transaction details
- Every transaction referenced in investigation reports links back here

### 9. API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/upload` | POST | Upload transaction history file (CSV/Excel) |
| `/analyze` | POST | Analyze customer history and run risk rules |
| `/report/{report_id}` | GET | Retrieve investigation report by ID |
| `/transactions` | GET | Retrieve all uploaded transactions |
| `/customer-profile` | GET | Retrieve customer behaviour profile |
| `/initialize-analysis` | POST | Full analysis pipeline (profile + rules + report) |

### 10. Demo Datasets

**Dataset 1: Normal Customer**
- Several months of routine activity
- Expected result: ✅ No Activity Requiring Attention

**Dataset 2: Investigation Scenario**
- Includes: new payee, multiple payments in short period, unusually large transfer, odd-hours transactions, normal transactions for comparison
- Expected result: ⚠️ Activity Requiring Investigation

## 🧪 Testing

Run the test suite:

```bash
cd backend
python -m pytest tests/ -v
```

Test cases include:
1. Normal transactions (no rules triggered)
2. Large transaction (Rule 1 triggered)
3. New payee burst (Rule 2 triggered)
4. Odd-hours transaction (Rule 3 triggered)
5. Multiple combined risk signals
6. Edge cases with limited transaction history
7. Normal customer produces "No Activity Requiring Attention"
8. Suspicious dataset produces investigation findings

## ⚠️ Critical Safety and Product Requirements

### ✅ The application:
- Flags unusual activity
- Explains why it was flagged
- Shows exact source transactions
- Compares activity against the customer's own history
- Connects related transactions
- Gives investigators clear priorities

### ❌ The application never:
- Claims fraud has occurred
- Claims a customer is guilty
- Invents transactions
- References transactions not present in the uploaded data
- Treats the risk score as a probability of fraud

**Always displayed message**:
> "This system identifies activity requiring review. Final investigation decisions remain with authorized human investigators."

## 🔧 Development Notes

### Backend (FastAPI + Python)

The backend implements a clean architecture with separation of concerns:

- **Services**: Data processing, behavior analysis, risk rules, connections, report generation
- **Rules**: Individual rule implementations (4 rules, each in its own file)
- **Models**: Pydantic models for transactions, profiles, and risk results
- **API**: FastAPI with CORS enabled, all required endpoints

Key implementation decisions:
- Uses IQR method alongside Mean + 3×Std Dev for robust outlier detection
- Customer behavior is compared primarily against the customer's own history
- Risk score is explainable and configurable
- Never claims fraud or guilt
- All findings traceable to actual uploaded transactions

### Frontend (React + TypeScript + Tailwind)

- Dark professional banking theme with cyan/amber accent colors
- Responsive design working on mobile and desktop
- Redux Toolkit for state management
- React Router for navigation
- Tailwind CSS for styling with custom banking color palette
- Modular component architecture matching the specified structure

### Frontend-Backend Communication

The frontend communicates with the real FastAPI backend via:
- `http://localhost:8000/api/` - all API endpoints
- File upload via multipart/form-data
- JSON responses for all data
- Real-time analysis after upload

## 📊 Sample Data Verification

The system has been verified with two realistic datasets:

| Dataset | Description | Risk Score | Outcome |
|---|---|---|---|
| Normal Customer | Several months of routine activity | 20/100 (Low) | ✅ No Activity Requiring Attention |
| Investigation Scenario | New payee burst + large transfer + odd hours | 45/100 (Medium) | ⚠️ Activity Requiring Investigation |

Both datasets contain clearly synthetic transaction data. All findings are traceable to actual transactions in the uploaded data.

## 🛠️ Troubleshooting

### Common Issues

1. **CORS errors**: Ensure the frontend development server is running and the backend is on port 8000
2. **Upload failures**: Verify CSV/Excel format and required columns (Date, Description, Payee, Amount, Channel)
3. **Analysis hangs**: Ensure the backend has sufficient memory for the transaction dataset
4. **False positives**: The system uses customer-relative comparison; customers with naturally high-value transactions may need rule threshold adjustments

### Need Help?

- Check the backend logs at `backend/backend.log`
- Verify the frontend is connecting to `http://localhost:8000/api/`
- Ensure both servers are running simultaneously