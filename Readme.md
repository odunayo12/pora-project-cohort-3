# PORA Academy Cohort 3 Capstone Project

## About Jubilee Groceries

The Jubilee Groceries is an e-commerce groceries store with over 120k customers distributed across 36 states of Nigeria plus the FCT. It sells groceries and is embarking on a new promotion drive to maximize the transaction of their existing customer base. This will in turn drive customer loyalty.

## Operations (Marketing)

Jubilee Groceries aims to introduce a promotion campaign to achieve the following objectives.

1. increase bulk/volume purchase,
2. reduce bounce rates. Bouncers are customers those who signed up and have never transacted (that is, in customers, is_deleted is FALSE, but not in invoice),
3. minimize inactivity or churn rates. `inactive customers`are customers who have not transacted the within 60 to 90 days from the project evaluation date (30-09-2024).

### Requirements

1. Evaluate the following KPI’s by time (Month, quarter etc.), category hierarchy, and promotion type
    - Revenue
    - Net Revenue = Revenue - Discount
    - Sales Volume
    - Discounts
    - Conversion – defined as uptakes from the applied promotion
2. Analyze customer inactivity, bulk purchase, and bouncer (customers who sign up but never transact) trends
3. Share insights and recommendations where necessary.

#### Stack

PostgreSQL, dbt, Google Looker

## Finance

Jubilee Groceries operates a buy-now-pay-later scheme. It encourages customers to make instalmental purchases. See the instalment table for details.

### Requirement

1. Evaluate the following KPI’s by time (Month, quarter etc.), and installment payment type, mode of payment.
    - Margin = Net Revenue + interest on instalments.
    - Receivables. What is the Debt obligation of our customers? Hint: use ageing report. Late payments also attracts some levy (see instalment table).
    - Analyze accounts reconciliation. Are there overpayments? Recommend ways to manage such disbursements.


## Resources

+ [Data Generator](data-generator/Readme.md)
+ [doc](https://dbdocs.io/embed/4da9d3f6c8c9a4f46394dae6a353c67a/65ec1da794b44ed38de3d8f03726c436)
