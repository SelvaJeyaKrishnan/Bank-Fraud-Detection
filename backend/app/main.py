from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .services.data_processor import process_uploaded_file
from .services.behavior_analyzer import analyze_customer_behavior
from .services.risk_engine import run_risk_rules
from .services.connection_engine import connect_transactions
from .services.report_generator import generate_report
from .models.transaction import CustomerProfile
from pydantic import BaseModel

app = FastAPI(
    title="Sentinel AI - Bank Fraud Investigation Assistant",
    version="1.0.0",
    description="AI-assisted investigation system for bank fraud desks",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    report_id: str


@app.post("/upload")
async def upload_transactions(file: UploadFile = File(...)):
    """Upload and parse transaction history file (CSV or Excel)."""
    try:
        result = process_uploaded_file(file)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/analyze")
async def analyze_history(request: AnalyzeRequest):
    """Analyze customer transaction history and run risk rules."""
    try:
        # In a full app, we'd load the transactions from storage
        # For now, return a basic response
        return {
            "status": "success",
            "message": "Analysis endpoint - connect frontend to test with real data",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/report/{report_id}")
async def get_report(report_id: str):
    """Retrieve investigation report by ID."""
    return {"report_id": report_id, "status": "generated"}


@app.get("/transactions")
async def get_transactions():
    """Retrieve all uploaded transactions."""
    return {"transactions": [], "count": 0}


@app.get("/customer-profile")
async def get_customer_profile():
    """Retrieve customer behaviour profile."""
    return {
        "average_amount": 0,
        "median_amount": 0,
        "min_amount": 0,
        "max_amount": 0,
        "std_dev": 0,
        "typical_range": "0-0",
        "frequent_payees": [],
        "new_payees": [],
        "typical_hours": "00:00-23:00",
        "channel_distribution": {},
    }


@app.post("/initialize-analysis")
async def initialize_analysis(transactions: list):
    """Full analysis pipeline: profile + rules + report."""
    try:
        # Build customer profile
        profile = analyze_customer_behavior(transactions)
        
        # Run risk rules
        risk_results = run_risk_rules(profile, transactions)
        
        # Connect transactions
        connections = connect_transactions(transactions)
        
        # Generate report
        report_id = generate_report(profile.dict() if hasattr(profile, 'dict') else profile, 
                                    risk_results, connections)
        
        return {
            "status": "success",
            "report_id": report_id,
            "risk_score": risk_results["score"],
            "risk_level": risk_results["risk_level"],
            "overall_finding": "✅ No Activity Requiring Attention" if risk_results["score"] <= 30 else "⚠️ Activity Requiring Investigation",
            "findings_count": len(risk_results["findings"]),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}