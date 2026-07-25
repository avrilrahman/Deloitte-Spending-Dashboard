# Ryan D'Souza Spending Dashboard
## Deloitte AI Challenge Submission

## Overview

This dashboard analyzes one month (May 2026) of TD chequing transactions for Ryan D'Souza, a 24-year-old data analyst in Toronto, to answer one question: **where is he wasting money, and what's the opportunity cost against his $3,000 emergency fund goal?**

The solution is built to be repeatable — any future month of TD chequing statement data can be dropped in and automatically classified using the same rules, with any ambiguous transactions flagged for manual review rather than silently miscategorized.

## Ryan's Situation

- Take-home pay: $3,950/month (Maple Analytics Inc.)
- Rent share: $900/month (shared 2-bed in the Annex)
- Goal: $3,000 emergency fund — currently ends up broke before each payday
- GoodLife Fitness membership, used only 1-2x/month
- 5 active streaming subscriptions, but only Netflix and Spotify are actually used
- Leftover LinkedIn Premium subscription from a job search that ended 9 months ago
- Unexplained ATM cash withdrawals with no memory of where the money went
- Hit an overdraft fee on May 31

## Methodology

### Defining "Wasted Spending"

Rather than treating all non-essential spending as waste, five categories were defined with explicit criteria:

| Category | Definition | Examples |
|---|---|---|
| Wasteful | Recurring or one-time cost providing little to no ongoing value | GoodLife membership, LinkedIn Premium, Disney Plus, Crave TV, Amazon Prime, overdraft fee |
| Essential subscriptions | Recurring services Ryan confirmed he actively uses | Netflix, Spotify |
| Essential | Fixed, non-negotiable costs | Rent, groceries, Rogers Wireless, Presto/TTC |
| Discretionary | Flexible lifestyle spending that could be adjusted | Dining out, bars, entertainment, LCBO, travel |
| Unclear cash | ATM withdrawals with no confirmed destination | All ATM withdrawals |

The overdraft fee is classified as wasteful rather than essential because it's a penalty with no product or value exchanged — unlike rent or groceries, it was fully avoidable and reflects cash flow mismanagement rather than a necessary cost.

### Classification Logic

Transactions are matched against category-specific keyword lists (e.g., `ESSENTIAL_KEYWORDS`, `WASTE_KEYWORDS`) in a `classify_transaction()` function. Any transaction that doesn't confidently match a keyword falls into a `needs_review` bucket rather than being defaulted into "discretionary" — this avoids silently misclassifying ambiguous spend and surfaces it for a human check via `get_review_flags()`.


## Key Findings

- **Confirmed wasteful subscriptions:** GoodLife Fitness, LinkedIn Premium, Disney Plus, Crave TV, and Amazon Prime total $143.95/month in recoverable savings.
- **Overdraft fee:** A single $45 avoidable charge from May 31, tied directly to cash flow mismanagement.
- **Untracked cash:** $560/month in ATM withdrawals with no confirmed purpose — flagged as "unclear cash" for manual review rather than assumed to be one single bad habit, since withdrawals occurred at different points across the month and likely reflect several distinct spending patterns.
- **Billing duplicates identified:** Netflix's second May charge ($7.99) reflects an intentional add-on profile Ryan actively uses, not a billing error — unlike the Crave TV renewal charge, which is a genuine duplicate tied to an unused service.

## Final Recommendation to Ryan

Cancel GoodLife Fitness, LinkedIn Premium, Disney Plus, Crave TV, and Amazon Prime — services confirmed unused or redundant — for **$143.95/month** in immediate, confirmed savings. Avoid the $45 overdraft fee by tracking balance more closely near month-end. Separately investigate the $560/month in untracked ATM withdrawals, since the cause is unconfirmed rather than assumed.

Combined recoverable total: **$768.94/month** (19.5% of take-home pay), reaching the $3,000 emergency fund goal in approximately **4.1 months**, assuming no interest and no other spending changes.

## AI Collaboration

The full prompt transcript, including where the AI's reasoning was correct and where it required correction, is documented in `prompt.md`. Notable corrections included re-classifying the Rogers Wireless preauthorized payment as essential rather than discretionary, and separating the Netflix add-on charge from the genuine Crave TV duplicate.

## Repo Structure
├── data/
│   └── ryan_dsouza_may2026_TD_statement.csv
├── src/
│   ├── __init__.py
│   ├── categorize.py
│   └── metrics.py
├── app.py #Streamlit Dashboard
├── prompt.md
├──README.md
├── requirements.txt
