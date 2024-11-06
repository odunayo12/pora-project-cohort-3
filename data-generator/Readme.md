# Doc

This repository simulates a dataset for a fictional **JUBILEE GROCERIES**, an e-commerce grocery store.

Data Generation:

Setup:

Imports necessary libraries like `faker` (for generating fake data), `pandas` (for data manipulation), `uuid` (for unique identifiers), datetime (for handling dates), and `sklearn.model_selection` (for data splitting).
Defines a list of Nigerian states.
Creates a save_csv function to easily save DataFrames to CSV files.
Reference Data:

Creates DataFrames for:

+ `promotion_df`: Stores information about different promotions (e.g., onboarding bonus, bulk discounts).
+ `unit_of_measurement_df`: Defines units for products (kg, L, unit, g, mL).
+ `category_df`: Lists product categories (Fruits, Vegetables, Dairy, etc.).
+ `sub_category_df`: Provides more specific subcategories within each category (Citrus Fruits, Berries, Leafy Greens, etc.).
+ `product_df`: Contains individual product details (name, subcategory, unit of measurement, price).
Customer Data:

generate_customer function: Creates a single customer with random details (name, address, credit card, activity status).
Generates 1000 customer records and stores them in `customer_df`.
Randomly assigns sign-up dates within a specified date range.
Ensures 70% of customers are marked as active.
Manipulates sign-up dates to ensure 20% of active customers signed up within two weeks before September 30, 2024.
Transaction Data:

`generate_transaction` function: Creates a single transaction record with a random customer, product, quantity, and date.
Generates 10,000,000 transaction records and stores them in `transaction_df`.
Calculates the average quantity purchased in the last month.
Ensures at least 33% of customers have their most recent transaction quantity above the average.
Calculates days of inactivity for each customer and ensures about 30% meet a specific inactivity criterion.
October Transaction Data:

Creates a list of customers who should receive promotions in October.
Generates additional transactions for October, ensuring a mix of customers with and without promotions.
Saving Data:

Saves all the generated DataFrames to CSV files in the 'data' directory.
Purpose:

This code creates a realistic (though simulated) dataset for a grocery store, which can be used for various purposes like:

Data Analysis: Analyzing customer behavior, product performance, promotion effectiveness, etc.
Machine Learning: Training models for tasks like customer segmentation, churn prediction, product recommendation, and more.
Testing and Development: Using the dataset to test applications or algorithms that deal with similar data.

## Promotion Criteria

1. Ensure at least 33% customers have their most recent transaction quantity greater than the average quantity purchased in the last 30 days
2. Inactive when number of days from evaluation date is greater than average number of days in between transactions. Bulk_buzzer
3. Ensure 20% of active customers have `sign_up_date` within two weeks before September 30, 2024

## September Data Edit

1. Fetch all September data
2. Include inactive customers
3. Include customers for bulk_buzzer

## Generating October Data

1. Signups 2 weeks before 30-09-2024 and never transacted (i.e. not in the transaction table)
2. Inactive Customers
3. Customers with recent purchase quantity greater than average last month purchase quantity
4. Others in the transaction table
5. Payment-type if
    + 1, purchase-date = payment date, and purchase-amount = payment-amount
    + 2, purchase-date = None, payments are split into at most 2, payable anytime within at most 2 moths from the date of purchase
    + 3, purchase-date = None, payments are split into at most 3, payable anytime within at most 3 moths from the date of purchase

## Invoice Data

This will factor in Pay-small-small and immediate payment approach.

1. Interest-on-installment = [`no_of_installments` – 1] %
2. `amount-due` = [`quantity` * `price` - `promo`] X [1 + `interest_on_installment %`]
3. `no_of_installments` if
    + 1, `instalment_1_payment_date` = `transaction_date`, and `instalment_1_amount_paid` = `amount-due`.
    + 2, `instalment_1_payment_date` = [`transaction_date` + random-days (1-30)], and `instalment_1_amount_paid` = [`amount-due` * `random_days (.25, .33, .72, .67)`], `instalment_2_payment_date` = [`transaction_date` + random-days (31-60)], `instalment_2_amount_paid` = {[`amount-due` - `instalment_1_amount_paid`] * `random_days (.0, 1, .97, .22)`}. Payment ensures that 1st installment is paid within the first 30 days and the 2nd, next 30 days. Also, the least payable amount on the first installment is 25%.
    + 3, `instalment_1_payment_date` = [`transaction_date` + random-days (1-30)], and `instalment_1_amount_paid` = [`amount-due` * random (.5, .53, .79, .66)], `instalment_2_payment_date` = [`transaction_date` + random-days (31-60)], `instalment_2_amount_paid` = {[`instalment_1_amount_paid`] X random (97, .27, .66, .35)}, `instalment_3_payment_date` = [`transaction_date` + random-days (61-90)], `instalment_3_amount_paid` = {[`amount-due`] - [`instalment_1_amount_paid` + `instalment_2_amount_paid`] X random (.0, .5, .27, 1)}. Payment ensures that 1st installment is paid within the first 30 days and the 2nd, next 30 days. Also, the least payable amount on the first installment is 50%.
    + Wherever [(`instalment_2_amount_paid`, `instalment_3_amount_paid`) = 0] update by setting [(`instalment_2_payment_date`, `instalment_3_payment_date`) = `Null`]. This will show defaults. That is if (`amount-due` > `instalment_1_amount_paid`) and `instalment_2_payment_date`=`Null` will imply default; if (`amount-due` > [`instalment_1_amount_paid` + `instalment_2_amount_paid`]) and `instalment_3_payment_date`=`Null` will imply default.
