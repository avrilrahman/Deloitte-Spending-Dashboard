# AI Collaboration Log — Ryan D'Souza Spending Dashboard
## Deloitte AI Challenge Submission

## Approach

I used an AI assistant (Perplexity - Claude Sonnet 5) throughout the build process to iterate on a Streamlit dashboard analyzing Ryan D'Souza's May 2026 TD chequing statement. The goal was to answer the brief's core question: "Where am I wasting money — and what's the opportunity cost?" My workflow was conversational and iterative — I would build/test a piece of the dashboard, screenshot the result, and describe bugs or visual issues in plain language, then walk through the category logic and recommendations step by step before writing any code.

## Prompt Transcript

---

**Prompt 1:**
"I'm analyzing one month (May 2026) of bank transactions for Ryan D'Souza, a 24-year-old data analyst in Toronto, 9 months into his first job. Key facts: take-home pay $3,950/month, rent share $900/month, goal is a $3,000 emergency fund but he keeps ending up broke before payday, GoodLife gym membership he uses 1-2x/month, 5 active streaming subscriptions (only uses Netflix and Spotify), a leftover LinkedIn Premium subscription from a job search that ended, unexplained ATM cash withdrawals, and an overdraft fee on May 31. I'll share his transaction CSV next. Acknowledge you understand this context before I share the data."

**Response 1:**
Confirmed understanding of Ryan's full profile: income, rent, savings goal, gym usage pattern, subscription overlap, dormant LinkedIn Premium, unexplained cash withdrawals, and the overdraft fee. Ready for the CSV.

---

**Prompt 2:**
"Based on Ryan's profile, propose 4-5 categories of 'wasted spending' with clear criteria for each (e.g., unused subscriptions = recurring charge with usage below X times/month). For each category, explain the reasoning, not just the label. I want to review and adjust these definitions before we build anything."

**Response 2:**
Proposed five categories with reasoning:
- Wasteful spend: unused GoodLife membership, dormant LinkedIn Premium, redundant streaming (Crave TV, Disney Plus, Amazon Prime), and the overdraft fee — services/costs providing little to no ongoing value.
- Essential subscriptions: Netflix and Spotify, kept separate since Ryan confirmed active use.
- Unclear cash: all ATM withdrawals, isolated because Ryan said he has no memory of where most of it went.
- Essential: rent, groceries — non-negotiable fixed costs.
- Discretionary: dining out, bars, entertainment, one-off purchases — flexible lifestyle spend.

---

**Prompt 3:**
"These categories look good to bin the data that we have. I have a question for the overdraft handling fee. Is that considered as a wasteful spend because it could have been avoided? Please explain your reasoning for this action of binning."

**Response 3:**
Confirmed the overdraft fee belongs in "wasteful" because it's a penalty charge with no product or value exchanged — unlike essential or discretionary spend, it exists purely due to cash flow mismanagement and could have been avoided entirely with no loss of value to Ryan. Framed as directly connecting his other wasteful spending to the real consequence he experienced (hitting $0 unexpectedly).

---

**Prompt 4:**
"Perfect. One of the requirements is to create this as a repeatable solution. Let's create a financial personal spending dashboard to get a clear view of where Ryan's spending is going towards. Let's start this way. Write a Python function that classifies each transaction using the categories we defined. The function should be reusable on any future month of TD chequing data. Flag any transaction it can't confidently classify for manual review."

**Response 4:**
Delivered `classify_transaction()` and `classify_dataframe()` functions using keyword-matching logic across defined category lists (WASTE_KEYWORDS, ESSENTIAL_SUB_KEYWORDS, GROCERY_KEYWORDS, ESSENTIAL_KEYWORDS, INCOME_KEYWORDS). Added a "needs_review" fallback category instead of defaulting unmatched transactions to "discretionary," plus a `get_review_flags()` helper to surface anything requiring manual review — built for reuse on future months' statements.

---

**Prompt 5:**
"Review your own transaction classifications. Are there any transactions that could reasonably be interpreted differently? Are there recurring charges you might have missed or miscategorized? Point out your own uncertainty rather than being overconfident."

**Response 5:**
Flagged genuine ambiguities: Uber Trip vs Uber Eats (commute vs leisure unclear), LCBO and one-off travel costs (judgment call on essential vs discretionary), and a real code gap — Rogers Wireless was never added to ESSENTIAL_KEYWORDS despite being described as essential, meaning it would have incorrectly fallen into "needs_review." Acknowledged classification confidence is only as strong as the keyword list and recommended manually checking `get_review_flags(df)` output before trusting totals.

---

**Prompt 6:**
"For Uber Trips, we can see that Ryan used it a couple times in May. It's safe to assume that it's not his main way to commute, we can keep it in its current bin. LCBO and the trip costs can stay as discretionary because those types of costs are extra funds or non-essential purchases. They can be cut or changed as needed. Rogers wireless must be a pre-authorized payment, keep it as essential."

**Response 6:**
Locked in decisions: Uber Trip and LCBO/travel costs remain discretionary; added "ROGERS WIRELESS" to ESSENTIAL_KEYWORDS to fix the gap identified in the previous review.

---

**Prompt 7:**
"Can you identify all recurring subscription charges including duplicates or renewals I might miss?"

**Response 7:**
Listed all nine recurring subscription-style charges across essential_sub and wasteful categories. Flagged two notable duplicates: Netflix billed twice in one month (base plan + add-on member, totaling $24.98 rather than $16.99), and Crave TV appearing twice ($19.99 on May 13 and again as "Crave TV Renewal" $19.99 on May 31) — recommended manually confirming with Ryan whether this is a genuine double-charge or two separate billing cycles.

---

**Prompt 8:**
"I noticed there are two Netflix charges and a cluster of ATM withdrawals throughout the month for Ryan. Can you explain what's going on with these and whether they should be treated as wasteful spending?"

**Response 8 (incorrect):**
Both Netflix charges should be treated as a duplicate billing error, the same way the Crave TV renewal was flagged — recommend canceling the add-on entirely to recover $7.99/month, since a single Netflix charge should only appear once. For the ATM withdrawals, grouped all five transactions together as a single "$560 unexplained cash spending" line item and treated it as one habit to cut, without noting that the withdrawals occurred at different points across the month.

---

**Correction 9:**
"Ryan's Netflix add-on isn't a mistake — he added a second profile on purpose, so that's not wasteful the way the Crave TV charge was, since he's not actually using Crave TV. Also, the ATM withdrawals aren't all the same thing — look at when they happened during the month. You can't group them together as one habit without more info on what each one was for."

**Response 9 (revised):**
Corrected: the Netflix add-on member charge reflects an intentional second profile Ryan actively uses, so it stays classified separately from Crave TV's genuine duplicate renewal charge, and is not counted toward wasteful spend. Reclassified the ATM withdrawals as several smaller, separately timed transactions rather than one lump sum, noting that without more detail on each withdrawal, the total should be flagged as "unclear cash" for manual review rather than confidently labeled a single wasteful habit.

---

**Prompt 10:**
"Based on the total wasted spend identified and Ryan's $3,000 emergency fund goal, draft a concise, specific recommendation for Ryan: what to cut, how much he'd save per month, and how many months until he hits his goal. Write it like advice from a financial analyst, not a generic budgeting tip list."

**Response 10:**
Drafted a direct, analyst-style recommendation: cancel GoodLife, LinkedIn Premium, Disney Plus, Crave TV, and Amazon Prime for $143.95/month in confirmed savings; avoid the $45 overdraft fee going forward; investigate the $560/month in untracked cash withdrawals. Combined total recoverable amount of $768.94/month gets Ryan to his $3,000 goal in approximately 4.1 months.

---

## What the AI Got Right

- Correctly classified spending into categories aligned with Ryan's stated habits (gym underuse, unused LinkedIn Premium, streaming overlap).
- Justified the overdraft fee's placement in "wasteful" with a clear, defensible principle (cost with no value received, fully avoidable).
- Proactively caught its own code gap (Rogers Wireless missing from essential keywords) when asked to self-review, rather than needing it pointed out first.
- Identified real, easy-to-miss billing duplicates (Netflix add-on, Crave TV renewal) that could materially affect the wasted-spend total.
- Delivered a final recommendation with specific dollar figures and a concrete timeline, not generic budgeting advice.

## What the AI Got Wrong / Had to Be Corrected

- Initially explained KPI card logic based on inference from the brief rather than verified code, before being corrected.
- Left a duplicate bar chart code block in place during an earlier iteration, causing a `StreamlitDuplicateElementKey` error and incorrect chart layout.
- Flagged Ryan's second Netflix charge as a duplicate billing error identical to the Crave TV renewal, before being corrected that it reflects an intentional second profile Ryan actively uses, not a mistake to cancel.

## Final Recommendation to Ryan

Cancel GoodLife Fitness, LinkedIn Premium, Disney Plus, Crave TV, and Amazon Prime — services confirmed unused or redundant — for $143.95/month in immediate savings. Avoid the $45 overdraft fee by tracking balance more closely. Investigate the $560/month in untracked ATM withdrawals. Combined recoverable total: $768.94/month (19.5% of take-home pay), reaching the $3,000 emergency fund goal in approximately 4.1 months, assuming no interest and no other spending changes.