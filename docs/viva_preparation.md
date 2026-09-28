# Banking Portfolio and Risk Analytics — Viva Preparation

## 2-Minute Project Explanation

“माझा project Banking Portfolio and Risk Analytics हा end-to-end data analytics project आहे. मी actual banking Excel dataset वापरला, ज्यात 3,000 client portfolio records आहेत.

सुरुवातीला Python आणि Pandas वापरून data understanding केले. मी sheets, data types, missing values, duplicates, unique values आणि outliers तपासले. Dataset मध्ये missing values आणि exact duplicate rows नव्हत्या, पण Customer ID fully unique नव्हता. म्हणून मी प्रत्येक record साठी `client_record_id` हा surrogate primary key तयार केला.

नंतर data cleaning आणि transformation केले. Age Group, Income Segment, Loan-to-Income Ratio, Total Account Balance आणि Total Lending Exposure हे derived columns तयार केले.

मी PostgreSQL मध्ये `banking_clients` table तयार करून SQL analysis केले. त्यानंतर Python EDA वापरून customer demographics, lending exposure, loyalty classification, banking relationship आणि Risk Score patterns analyze केले.

Power BI मध्ये Executive Summary, Customer Analysis, Risk Analysis आणि Insights Dashboard असे चार dashboard pages तयार केले. Project मधील मुख्य finding म्हणजे Retail relationship मध्ये सर्वात जास्त lending exposure आहे. Score 4–5 records 16.07% आहेत, पण source dataset मध्ये risk-score direction define नसल्यामुळे मी त्यांना confirmed high-risk किंवा default customers म्हटले नाही; फक्त risk-review records म्हटले आहे.

या project मधून banking portfolio monitoring, risk-review prioritisation आणि future data requirements यासाठी practical recommendations मिळाल्या.” 

## Common Viva Questions and Answers

### 1. Why did you choose the banking domain?

Banking domain मध्ये customer segmentation, loans, deposits, risk management आणि portfolio analysis यांसारखे practical business problems असतात. त्यामुळे Excel, Python, SQL आणि Power BI skills एकाच project मध्ये दाखवता येतात.

### 2. Why is this a Data Analytics project and not a Machine Learning project?

या dataset मध्ये default flag, repayment history, credit score आणि EMI अशी supervised machine-learning target तयार करण्यासाठी आवश्यक fields नाहीत. त्यामुळे ML model बनवणे technically correct नसते. म्हणून मी project ला data analytics वर focused ठेवले.

### 3. What was the biggest data-quality issue?

`Customer ID` fully unique नव्हता. 3,000 records मध्ये फक्त 2,940 unique source Customer IDs होते. काही repeated IDs वेगवेगळ्या customer names सोबत होते. त्यामुळे `Customer ID` primary key म्हणून वापरला नाही आणि `client_record_id` तयार केला.

### 4. Why did you not remove outliers?

Banking मध्ये high loan amount, high deposit किंवा high balance हे genuine high-value customers असू शकतात. त्यामुळे IQR method ने outliers identify केले, पण business validation शिवाय delete किंवा cap केले नाहीत.

### 5. What is the difference between Loan-to-Income Ratio and EMI Ratio?

Loan-to-Income Ratio म्हणजे Loan Amount divided by Estimated Income. EMI Ratio साठी EMI amount आवश्यक असतो. Dataset मध्ये EMI field नसल्यामुळे मी EMI Ratio calculate केला नाही.

### 6. Why did you use PostgreSQL?

PostgreSQL relational database आहे. त्यात structured tables, SQL queries, aggregations, filters आणि data validation करता येते. त्यामुळे Python analysis नंतर SQL-based business analysis दाखवता आला.

### 7. What is the primary key in your project?

`client_record_id` हा primary key आहे. तो cleaning phase मध्ये प्रत्येक record साठी तयार केला आहे. Source `customer_id` duplicate असल्यामुळे तो primary key नाही.

### 8. Why did you not create a complete star schema?

Source मध्ये separate reliable customer, loan, payment, city किंवा transaction tables नव्हत्या. Artificial dimensions तयार केल्यास model misleading झाला असता. म्हणून single analytical table model वापरला आणि Power BI साठी Date dimension तयार केली.

### 9. What are the main KPIs?

Main KPIs आहेत:

- Client Records
- Unique Source Customer IDs
- Total Loan Amount
- Total Deposit Amount
- Total Lending Exposure
- Average Estimated Income
- Average Risk Score
- Score 4–5 Risk Review Records
- Score 4–5 Risk Review Percentage

### 10. What is your most important business insight?

Retail banking relationship मध्ये सर्वात जास्त lending exposure आहे: 2,093,100,933.31. त्यामुळे relationship-level concentration monitoring आवश्यक आहे.

### 11. Why did you use “Risk Review Records” instead of “High-Risk Customers”?

Dataset मध्ये Risk Score 1–5 असला तरी score direction document केलेली नाही. त्यामुळे Score 4–5 ला confirmed high-risk म्हणणे incorrect ठरू शकते. म्हणून accurate आणि safe term म्हणून “Risk Review Records” वापरला.

### 12. What are the limitations of this project?

- Default status नाही.
- Payment history नाही.
- EMI amount नाही.
- Credit score नाही.
- Loan status आणि loan ID नाही.
- City mapping नाही.
- Currency unit defined नाही.
- Customer ID duplicates आहेत.

### 13. What is the future scope?

Future मध्ये default flag, repayment data, EMI, credit score, loan type, city master आणि transaction-level data add करून confirmed credit-risk, default, repayment आणि trend analysis करता येईल.

## Final Project Checklist

### Data and Code

- [ ] Original Excel file remains unchanged.
- [ ] Raw and processed datasets are excluded from GitHub.
- [ ] All four Python scripts run successfully.
- [ ] `transformed_banking_clients.csv` is generated.
- [ ] PostgreSQL table contains 3,000 records.
- [ ] SQL quality and analytics queries run successfully.

### Power BI

- [ ] All four dashboard pages are complete.
- [ ] Slicers update visuals correctly.
- [ ] DAX KPI values match source analysis.
- [ ] No unsupported Default Rate or EMI Ratio is shown.
- [ ] Risk Score 4–5 is labelled as Risk Review.
- [ ] Dashboard file is saved locally.

### Documentation and GitHub

- [ ] README is complete.
- [ ] Data dictionary is complete.
- [ ] Architecture document is complete.
- [ ] Insights document is complete.
- [ ] Viva preparation document is complete.
- [ ] GitHub repository does not contain actual customer data.
- [ ] Latest changes are committed and pushed.

## Final Git Commands

```powershell
git status
git add .
git commit -m "Complete banking portfolio and risk analytics project"
git push
```