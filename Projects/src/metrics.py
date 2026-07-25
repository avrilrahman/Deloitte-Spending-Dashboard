def wasted_spend_total(df):
    waste_cats = ["wasteful", "fee", "unclear_cash"]
    return df[df["category"].isin(waste_cats)]["Debit"].sum()

def spend_by_category(df):
    return df.groupby("category")["Debit"].sum().sort_values(ascending=False)

def waste_pct_of_income(df, take_home=3950):
    total_waste = wasted_spend_total(df)
    return round((total_waste / take_home) * 100, 1)

def months_to_goal(monthly_savings, goal=3000):
    if monthly_savings <= 0:
        return None
    return round(goal / monthly_savings, 1)