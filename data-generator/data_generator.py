# %%
from faker import Faker
import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
import algorithm as alg
from tqdm import trange


# %%
nigerian_states = alg.nigerian_states
number_of_customers = 120000
number_of_transactions = 10000000
number_of_transactions_oct = int(.1*number_of_transactions)
start_date = '2024-01-01'
end_date = '2024-09-30'
dim_start_date = '2023-10-01'
dim_end_date = '2024-02-01'
dim_start_date_up = '2024-03-01'
dim_end_date_up = end_date
oct_start_date = '2024-10-01'
oct_end_date = '2024-10-31'



# %%
promotion_data = alg.promotion_data
promotion_df = alg.table_update(promotion_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)
# %%
# Define the unit of measurement data
unit_of_measurement_data = alg.unit_of_measurement_data
unit_of_measurement_df = alg.table_update(unit_of_measurement_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)
# %%
# Define the category data
category_data = alg.category_data
category_df = alg.table_update(category_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)
# %%
# Define the sub_category data
sub_category_data = alg.generate_subcategory(category_df)
sub_category_df = alg.table_update(sub_category_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)

#%%
product_data = alg.generate_product(unit_of_measurement_df, sub_category_df)
product_df = alg.table_update(product_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)
product_df['price'] = np.where(product_df['unit_of_measurement_id'] == 2, 
                               product_df['price'] * 110, 
                               product_df['price'] * random.choice([815, 1070, 1420]))

# %%
customer_data = [alg.generate_customer() for _ in trange(number_of_customers)]
customer_df = alg.table_update(customer_data, start_date, end_date, dim_start_date_up, end_date)

# %%
installment_data = alg.instalment_data
installment_df = alg.table_update(installment_data, dim_start_date, dim_end_date, dim_start_date_up, dim_end_date_up)
# %%

# Filter active customers
in_force_customers = customer_df[customer_df['is_in_force'] == True]
# inforce Fasle means they might have been barred for default on the pay-small-small scheme
# Ensure 20% of active customers have created_on within two weeks before September 30, 2024
two_weeks_before_end = datetime(2024, 9, 30) - timedelta(weeks=2)
recent_signups = in_force_customers.sample(frac=0.2)
mod_date_range = pd.date_range(start_date, two_weeks_before_end)
customer_df.loc[recent_signups.index, 'created_on'] = np.random.choice(mod_date_range, size=len(recent_signups))

# Exclude recent sign-ups from active customers for transaction generation
recent_signup_ids = recent_signups['id'].tolist()
active_customers_for_transactions = in_force_customers[~in_force_customers['id'].isin(recent_signup_ids)]
# %%
transaction_data = [alg.generate_transaction(active_customers_for_transactions, product_df) for _ in trange(number_of_transactions)]
transaction_df = alg.table_update(transaction_data, start_date, end_date, dim_start_date_up, oct_end_date)

#%%
# Filter transactions for September 2024
september_transactions = transaction_df[transaction_df['created_on'].dt.month == 9]

# Calculate average quantity purchased by each customer in September
september_avg_quantity = september_transactions.groupby('customer_id')['quantity'].mean()

# Filter transactions for August 2024
august_transactions = transaction_df[transaction_df['created_on'].dt.month == 8]

# Calculate average quantity purchased by each customer in August
august_avg_quantity = august_transactions.groupby('customer_id')['quantity'].mean()

# Combine the average quantities for September and August
combined_avg_quantity = pd.merge(september_avg_quantity, august_avg_quantity, on='customer_id', how='left', suffixes=('_sept', '_aug'))

# Identify customers whose September average is greater than their August average
customers_with_higher_sept_avg = combined_avg_quantity[combined_avg_quantity['quantity_sept'] > combined_avg_quantity['quantity_aug']]

# Get the list of customer IDs
customers_with_avg_qty_over_avg = customers_with_higher_sept_avg.reset_index()['customer_id'].tolist()


# %%
# Ensure that randomly selected 20% of customers to have their transaction dates replaced with dates between March and May, instead of adding new transactions for them.
# Select 20% of unique customers for March-May transactions
june_july_customers = random.sample(transaction_df['customer_id'].unique().tolist(), 
                                    k=int(0.3 * transaction_df['customer_id'].nunique()))

# Generate random dates between March 1st and May 31st
june_july_date_range = pd.date_range('2024-06-01', '2024-07-31')

# Replace transaction dates for the selected customers
transaction_df.loc[
    transaction_df['customer_id'].isin(june_july_customers), 'created_on'] = np.random.choice(june_july_date_range, size=len(transaction_df[transaction_df['customer_id'].isin(june_july_customers)]))
#%%
# The aim here is to get the 3 types of promo-qualified customers. We desire to use 73.5% of them for generating the data in october transactions
required_for_promo_in_september_df = customers_with_avg_qty_over_avg
required_for_promo_in_june_july = june_july_customers
required_for_promo_in_signups = recent_signup_ids
manipulated_customer_ids = set(required_for_promo_in_june_july + required_for_promo_in_signups + required_for_promo_in_september_df)
random_promo_customers_portion = 0.735 * len(manipulated_customer_ids)
promo_customer_ids = random.sample(list(manipulated_customer_ids), k=int(random_promo_customers_portion))
# check
# set(required_for_promo_in_signups) & set(required_for_promo_in_june_july) == set() -> True
# set(required_for_promo_in_signups) & set(required_for_promo_in_september_df) == set() -> True
# must be true in both cases

# %%
# Here, we desire to identify customer that did not appear in the promo list and use about 80% in generating transactions for october.
customers_in_transaction_df = set(transaction_df['customer_id'].unique().tolist())
customers_in_transaction_but_not_manipulated_ids = customers_in_transaction_df - manipulated_customer_ids
random_non_promo_customers_portion = 0.80 * len(customers_in_transaction_but_not_manipulated_ids)
non_promo_customer_ids = random.sample(list(customers_in_transaction_but_not_manipulated_ids), k=int(random_non_promo_customers_portion))
# check
# set(non_promo_customer_ids) & set(promo_customer_ids) == set() -> True
# %%
oct_transaction_generator_ids = promo_customer_ids + non_promo_customer_ids
oct_transaction_generator = pd.DataFrame({'id':oct_transaction_generator_ids})
oct_transaction_data = [alg.generate_transaction(oct_transaction_generator, product_df) for _ in trange(number_of_transactions_oct)]
oct_transaction_df = alg.table_update(oct_transaction_data, oct_start_date, oct_end_date, oct_start_date, oct_end_date)
transaction_data_final = pd.concat([transaction_df, oct_transaction_df], ignore_index=True)
#
# %%
##### Parent Invoice
#transactions on the same day by the same customer to have the same parent_invoice_id (UUID).
transaction_data_final['parent_invoice_id'] = transaction_data_final.groupby(['created_on', 'customer_id'])['created_on'].transform(lambda _: str(uuid.uuid4()))
invoice_counts = transaction_data_final.groupby(['created_on', 'customer_id'])['id'].nunique()
transaction_data_final = transaction_data_final.sort_values(by=['created_on', 'customer_id'])
transaction_data_final
# %%
# Extract parent_invoice_data
# 1. Merge the DataFrames
# p_df = product_df.copy()
# p_df = p_df.drop(['created_on', 'updated_on'], axis=1).rename(columns={'id':'product_id'})
merged_df = pd.merge(transaction_data_final, product_df, left_on='product_id', right_on='id', how='left')
# 2. Calculate the price per transaction line
merged_df['line_total'] = merged_df['price'] * merged_df['quantity']
# 3. Group by created_on and parent_invoice_id and sum the line totals
invoice_data = merged_df.groupby(['created_on_x', 'customer_id',  'parent_invoice_id'])['line_total'].sum().reset_index(name='invoice_amount').rename(columns={'created_on_x':'created_on'})
# %%
print(invoice_data.shape)
print(invoice_data.head())
# %%
invoice_data['promo_code'] = None
desired_period_filter = invoice_data['created_on'].dt.month == 10
invoice_data.loc[(invoice_data['customer_id'].isin(required_for_promo_in_september_df)) & (desired_period_filter), 'promo_code'] = '1001'
invoice_data.loc[(invoice_data['customer_id'].isin(required_for_promo_in_june_july)) & (desired_period_filter), 'promo_code'] = '10001'
invoice_data.loc[(invoice_data['customer_id'].isin(required_for_promo_in_signups)) & (desired_period_filter), 'promo_code'] = '101'
# invoice_data.tail()
# check
# invoice_data[invoice_data['promo_code']=='1001']

# %%
# intorduce installmental payments/distribution {1:'60%, 2:'23%', 3:'17%'}
# Define the probabilities for each number of installments
installment_probabilities = [0.60, 0.23, 0.17]  # Must add up to 1

# Generate random installment numbers based on probabilities
installment_choices = np.random.choice([1, 2, 3], size=len(invoice_data), p=installment_probabilities)

# Assign the generated installment numbers to the 'no_of_installments' column
invoice_data['no_of_installments'] = installment_choices
#%%
invoice_data['interest_on_installment'] = (invoice_data['no_of_installments'] - 1) /100
invoice_data['promo_rate'] = invoice_data.apply(alg.apply_promo_rate, axis=1)

#%%
invoice_data['amount_due'] = (invoice_data['invoice_amount'] * (1 - invoice_data['promo_rate'])) * (1 + invoice_data['interest_on_installment']) 

#%%
#This code effectively adds the 'mode_of_payment' column to your invoice_data DataFrame and populates it with randomly distributed payment methods for single-installment invoices while using a default value for multi-installment invoices.
# Define the payment methods and their probabilities
payment_methods = ['bank_transfer', 'card']
payment_probabilities = [0.215, 0.785]  # Must add up to 1

# Identify invoices with only one installment
single_installment_mask = invoice_data['no_of_installments'] == 1

# Generate random payment methods for single installment invoices
invoice_data.loc[single_installment_mask, 'mode_of_payment'] = np.random.choice(
    payment_methods, 
    size=sum(single_installment_mask), 
    p=payment_probabilities
)

# For invoices with more than one installment, assume a default payment mode (e.g., 'installment_plan')
invoice_data.loc[~single_installment_mask, 'mode_of_payment'] = 'installment_plan' 

#%%
# wehre mode_of_payment = card and no_of_installments =1, let a new column called instalment_1_amount_paid be equal to amount_due. But where mode_of_payment = bank_transfer and no_of_installments =1, let instalment_1_amount_paid be randomly distributed as 100%, 76% or 88% of amount_due.

# Define conditions for payment types and installments
card_single_installment = (invoice_data['mode_of_payment'] == 'card') & (invoice_data['no_of_installments'] == 1)
bank_transfer_single_installment = (invoice_data['mode_of_payment'] == 'bank_transfer') & (invoice_data['no_of_installments'] == 1)

# Calculate 'instalment_1_amount_paid' based on conditions
invoice_data['instalment_1_amount_paid'] = 0  # Initialize the column

# For card payments with 1 installment, amount paid equals amount due
invoice_data.loc[card_single_installment, 'instalment_1_amount_paid'] = invoice_data.loc[card_single_installment, 'amount_due']

# For bank transfers with 1 installment, randomly choose a percentage of amount due
percentages = np.random.choice([1.00, 0.76, 0.88], size=sum(bank_transfer_single_installment))
invoice_data.loc[bank_transfer_single_installment, 'instalment_1_amount_paid'] = (
    invoice_data.loc[bank_transfer_single_installment, 'amount_due'] * percentages
)

#%%
# Assuming 'created_on' is an existing column in your DataFrame

# Select rows where no_of_installments is 1
single_installment_mask = invoice_data['no_of_installments'] == 1

# Set 'instlment_1_payment_date' to 'created_on' for those rows
invoice_data.loc[single_installment_mask, 'instalment_1_payment_date'] = invoice_data.loc[single_installment_mask, 'created_on'] 
#%%
# Condition for 2 installments
two_installments_mask = invoice_data['no_of_installments'] == 2

# Calculate payment dates for 2 installments
invoice_data.loc[two_installments_mask, 'instalment_1_payment_date'] = (
    invoice_data.loc[two_installments_mask, 'created_on'] + 
    pd.to_timedelta(np.random.randint(2, 31, size=sum(two_installments_mask)), unit='D')
)
invoice_data.loc[two_installments_mask, 'instalment_2_payment_date'] = (
    invoice_data.loc[two_installments_mask, 'created_on'] + 
    pd.to_timedelta(np.random.randint(31, 61, size=sum(two_installments_mask)), unit='D')
)

# Condition for 3 installments
three_installments_mask = invoice_data['no_of_installments'] == 3

# Calculate payment dates for 3 installments
invoice_data.loc[three_installments_mask, 'instalment_1_payment_date'] = (
    invoice_data.loc[three_installments_mask, 'created_on'] + 
    pd.to_timedelta(np.random.randint(2, 31, size=sum(three_installments_mask)), unit='D')
)
invoice_data.loc[three_installments_mask, 'instalment_2_payment_date'] = (
    invoice_data.loc[three_installments_mask, 'created_on'] + 
    pd.to_timedelta(np.random.randint(31, 61, size=sum(three_installments_mask)), unit='D')
)
invoice_data.loc[three_installments_mask, 'instalment_3_payment_date'] = (
    invoice_data.loc[three_installments_mask, 'created_on'] + 
    pd.to_timedelta(np.random.randint(61, 91, size=sum(three_installments_mask)), unit='D')
)
#%%
# Define probabilities for installment_2_amount_paid
installment_2_percentages = [0.0, 1, 0.97, 0.22, 0.88, 0.725, 1.38, 1.83]
installment_2_probabilities = [0.1, 0.4, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]  # Higher probability for 1.0 (full payment)

# Calculate installment amounts for 2 installments
two_installments_mask = invoice_data['no_of_installments'] == 2

invoice_data.loc[two_installments_mask, 'instalment_1_amount_paid'] = (
    invoice_data.loc[two_installments_mask, 'amount_due'] * 
    np.random.choice([0.25, 0.33, 0.72, 0.67], size=sum(two_installments_mask))
)

invoice_data.loc[two_installments_mask, 'instalment_2_amount_paid'] = (
    (invoice_data.loc[two_installments_mask, 'amount_due'] - 
     invoice_data.loc[two_installments_mask, 'instalment_1_amount_paid']) *
    np.random.choice(installment_2_percentages, size=sum(two_installments_mask), p=installment_2_probabilities)
)

# %%

# Define probabilities for instalment_3_amount_paid
installment_3_percentages = [0.0, 0.5, 0.27, 1, 1.113]
installment_3_probabilities = [0.05, 0.2, 0.2, 0.5, 0.05]  # Higher probability for 1.0 (full payment)

# Calculate installment amounts for 3 installments
three_installments_mask = invoice_data['no_of_installments'] == 3

invoice_data.loc[three_installments_mask, 'instalment_1_amount_paid'] = (
    invoice_data.loc[three_installments_mask, 'amount_due'] * 
    np.random.choice([0.5, 0.53, 0.79, 0.66], size=sum(three_installments_mask))
)

invoice_data.loc[three_installments_mask, 'instalment_2_amount_paid'] = (
    invoice_data.loc[three_installments_mask, 'instalment_1_amount_paid'] * 
    np.random.choice([0.97, 0.27, 0.66, 0.35], size=sum(three_installments_mask))
)

invoice_data.loc[three_installments_mask, 'instalment_3_amount_paid'] = (
    (invoice_data.loc[three_installments_mask, 'amount_due'] - 
     invoice_data.loc[three_installments_mask, 'instalment_1_amount_paid'] -
     invoice_data.loc[three_installments_mask, 'instalment_2_amount_paid']) *
    np.random.choice(installment_3_percentages, size=sum(three_installments_mask), p=installment_3_probabilities)
)

# %%
# Define payment methods for multi-installment invoices
multi_installment_payment_methods = ['card', 'bank_transfer', 'direct_debit']

# Select rows with 2 or 3 installments
multi_installment_mask = invoice_data['no_of_installments'].isin([2, 3])

# Randomly assign payment methods to multi-installment invoices
invoice_data.loc[multi_installment_mask, 'mode_of_payment'] = np.random.choice(
    multi_installment_payment_methods,
    size=sum(multi_installment_mask)
)


#%%
# test_ = [alg.generate_transaction(active_customers_for_transactions, product_df) for _ in trange(10000000)]

#%%
invoice_data_final= invoice_data[
    [
        'customer_id', 'parent_invoice_id', 
        'invoice_amount', 'created_on', 
        'no_of_installments','promo_code', 'mode_of_payment', 
        'instalment_1_payment_date', 'instalment_1_amount_paid',
        'instalment_2_payment_date', 'instalment_2_amount_paid',
        'instalment_3_payment_date', 'instalment_3_amount_paid'
    ]
].rename(columns={'parent_invoice_id':'id', 'no_of_installments':'instalment_id'})

# %%

dir_ = 'data/csv/dimension_tables'
dim_table_attr = {
    'unit_of_measurement.csv':unit_of_measurement_df,
    'category.csv':category_df,
    'sub_category.csv':sub_category_df,
    'product.csv':product_df,
    'installment.csv':installment_df,
    'promotion.csv':promotion_df ,
    'customer.csv':customer_df  
}

[alg.save_csv(v, dir_, k) for k,v in dim_table_attr.items()]

fact_table_attr = {
    'parent_invoice.csv':invoice_data_final,
    'invoice.csv':transaction_data_final
}
invoice_data['year_month'] = invoice_data['created_on'].dt.strftime('%Y-%m')
transaction_data_final['year_month'] = transaction_data_final['created_on'].dt.strftime('%Y-%m')
# Group by year and month
grouped_invoices = invoice_data.groupby('year_month')
grouped_transactions = transaction_data_final.groupby('year_month')

# %%
# Iterate through groups and save each group to a separate CSV file
dir_fact = 'data/csv/fact_tables'
for name, group in grouped_transactions:
    file_dir = os.path.join(dir_fact, 'invoice')
    os.makedirs(file_dir, exist_ok=True)
    file_name = f'{file_dir}/invoice__{name}.csv'
    group.drop('year_month', axis=1).to_csv(file_name, index=False)

#%%
invoice_data.promo_code = None
# %%
for name, group in grouped_invoices:
    file_dir = os.path.join(dir_fact, 'parent_invoice')
    os.makedirs(file_dir, exist_ok=True)
    file_name = f'{file_dir}/parent_invoice__{name}.csv'
    group.drop('year_month', axis=1).to_csv(file_name, index=False)
# TODO: remove the not so needed columns from invoice data
# TODO: save to folder as mysql-syntax compactible sql files
# TODO: compress as csv for github
# %%
