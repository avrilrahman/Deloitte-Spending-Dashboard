import pandas as pd

WASTE_KEYWORDS = ["GOODLIFE", "LINKEDIN PREMIUM", "CRAVE TV", "DISNEY PLUS", "AMAZON PRIME", "OVERDRAFT HANDLING" ]
ESSENTIAL_SUB_KEYWORDS = ["NETFLIX", "SPOTIFY"]
GROCERY_KEYWORDS = ["GROCERY", "LOBLAWS", "METRO", "FRESHCO", "NO FRILLS", "SHOPPERS"]

def classify_transaction(description: str) -> str:
    d = description.upper()
    if "PAYROLL" in d or "DEP -" in d:
        return "income"
    if any(k in d for k in WASTE_KEYWORDS):
        return "wasteful"
    if "ABM WITHDRAWAL" in d:
        return "unclear_cash"
    if any(k in d for k in ESSENTIAL_SUB_KEYWORDS):
        return "essential_sub"
    if "RENT" in d or "PRESTO FARE" in d or "TTC" in d:
        return "essential"
    if any(k in d for k in GROCERY_KEYWORDS):
        return "essential"
    return "discretionary"