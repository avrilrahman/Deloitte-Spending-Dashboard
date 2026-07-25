import pandas as pd

WASTE_KEYWORDS = [
    "GOODLIFE",
    "LINKEDIN PREMIUM",
    "CRAVE TV",
    "DISNEY PLUS",
    "AMAZON PRIME",
    "OVERDRAFT HANDLING",
]

ESSENTIAL_SUB_KEYWORDS = [
    "NETFLIX",
    "SPOTIFY",
    "ROGERS",
]

GROCERY_KEYWORDS = [
    "GROCERY",
    "LOBLAWS",
    "METRO",
    "FRESHCO",
    "NO FRILLS",
    "SHOPPERS",
]

ESSENTIAL_KEYWORDS = [
    "RENT",
    "PRESTO FARE",
    "TTC",
]


def classify_transaction(description: str) -> str:
    if pd.isna(description):
        return "discretionary"

    d = str(description).upper()

    if "PAYROLL" in d or "DEP -" in d or d.startswith("DEP"):
        return "income"

    if any(k in d for k in WASTE_KEYWORDS):
        return "wasteful"

    if "ABM WITHDRAWAL" in d or "ATM WITHDRAWAL" in d:
        return "unclear_cash"

    if any(k in d for k in ESSENTIAL_SUB_KEYWORDS):
        return "essential_sub"

    if any(k in d for k in ESSENTIAL_KEYWORDS):
        return "essential"

    if any(k in d for k in GROCERY_KEYWORDS):
        return "essential"

    return "discretionary"