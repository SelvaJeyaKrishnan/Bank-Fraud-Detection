from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: Optional[str] = Field(None, description="Unique transaction identifier")
    date: datetime = Field(..., description="Transaction date")
    time: Optional[str] = Field(None, description="Transaction time (HH:MM)")
    description: str = Field(..., description="Transaction description")
    payee: str = Field(..., description="Payee/beneficiary name")
    amount: float = Field(..., description="Transaction amount")
    channel: str = Field(..., description="Transaction channel (e.g., Card, UPI, Bank Transfer)")
    is_new_payee: bool = Field(False, description="Whether this is a new payee")


class CustomerProfile(BaseModel):
    average_amount: float = 0.0
    median_amount: float = 0.0
    min_amount: float = 0.0
    max_amount: float = 0.0
    std_dev: float = 0.0
    typical_range: tuple = (0.0, 0.0)
    frequent_payees: List[str] = []
    new_payees: List[str] = []
    typical_hours: tuple = (0, 23)
    channel_distribution: dict = {}


class RiskRuleResult(BaseModel):
    rule_name: str
    risk_level: str  # "Low", "Medium", "High"
    explanation: str
    related_transactions: List[Transaction]
    priority_score_contribution: float = 0.0


class InvestigationFinding(BaseModel):
    finding_number: int
    rule_triggered: str
    risk_level: str
    priority_score: float  # 0-100
    transactions: List[Transaction]
    why_flagged: str
    normal_behaviour: str
    connected_activity: List[Transaction]
    investigator_questions: List[str]