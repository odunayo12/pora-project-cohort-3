# %%
from faker import Faker
import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
from sklearn.model_selection import train_test_split


# %%
nigerian_states = [
  "Abia",
  "Adamawa",
  "Akwa Ibom",
  "Anambra",
  "Bauchi",
  "Bayelsa",
  "Benue",
  "Borno",
  "Cross River",
  "Delta",
  "Ebonyi",
  "Edo",
  "Ekiti",
  "Enugu",
  "FCT - Abuja",
  "Gombe",
  "Imo",
  "Jigawa",
  "Kaduna",
  "Kano",
  "Katsina",
  "Kebbi",
  "Kogi",
  "Kwara",
  "Lagos",
  "Nasarawa",
  "Niger",
  "Ogun",
  "Ondo",
  "Osun",
  "Oyo",
  "Plateau",
  "Rivers",
  "Sokoto",
  "Taraba",
  "Yobe",
  "Zamfara"
]

# %%
len(nigerian_states)

# %%
def save_csv(dataframe, directory, filename):
    """
    Save a pandas DataFrame to a CSV file in a specified directory with a given filename.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame to save.
    directory (str): The directory where the CSV file will be saved.
    filename (str): The name of the CSV file.

    Returns:
    str: The path to the saved CSV file.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, filename)
    dataframe.to_csv(file_path, index=False)
    return file_path


# %%
promotion_data = [
    {'promo_code':'101', 'name':'onboarder', 'rate':1000, 'measure':'amount in Naira', 'target':'sign-on without transacting', 'aim':'conversion of sign-ons'},
    {'promo_code':'1001', 'name':'bulk_buzzer', 'rate':3, 'measure':'percentage', 'target':'bulk buyers', 'aim':'encourage high purchase volumes'},
    {'promo_code':'10001', 'name':'reactivator', 'rate':500, 'measure':'amount in Naira', 'target':'reactivate inactive customers', 'aim':'win back inactive customers'}
]

promotion_df = pd.DataFrame(promotion_data)

# %%

# Define the unit of measurement data
unit_of_measurement_data = [
    {"id": str(uuid.uuid4()), "long_name": "Kilogram", "short_name": "kg", "remarks": "Unit of mass"},
    {"id": str(uuid.uuid4()), "long_name": "Liter", "short_name": "L", "remarks": "Unit of volume"},
    {"id": str(uuid.uuid4()), "long_name": "Unit", "short_name": "unit", "remarks": "Individual item count"},
    {"id": str(uuid.uuid4()), "long_name": "Gram", "short_name": "g", "remarks": "Unit of mass"},
    {"id": str(uuid.uuid4()), "long_name": "Milliliter", "short_name": "mL", "remarks": "Unit of volume"}
]
unit_of_measurement_df = pd.DataFrame(unit_of_measurement_data)


# %%

# Define the category data
category_data = [
    {"id": str(uuid.uuid4()), "name": "Fruits", "long_name": "Fresh Fruits", "remarks": "Includes all types of fresh fruits"},
    {"id": str(uuid.uuid4()), "name": "Vegetables", "long_name": "Fresh Vegetables", "remarks": "Includes all types of fresh vegetables"},
    {"id": str(uuid.uuid4()), "name": "Dairy", "long_name": "Dairy Products", "remarks": "Includes milk, cheese, and other dairy products"},
    {"id": str(uuid.uuid4()), "name": "Bakery", "long_name": "Bakery Items", "remarks": "Includes bread, cakes, and other baked goods"},
    {"id": str(uuid.uuid4()), "name": "Beverages", "long_name": "Beverages", "remarks": "Includes all types of drinks"}
]
category_df = pd.DataFrame(category_data)


# %%

# Define the sub_category data
sub_category_data = [
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[0, 'id'], "name": "Citrus", "long_name": "Citrus Fruits", "remarks": "Includes oranges, lemons, and other citrus fruits"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[0, 'id'], "name": "Berries", "long_name": "Berries", "remarks": "Includes strawberries, blueberries, and other berries"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[1, 'id'], "name": "Leafy Greens", "long_name": "Leafy Green Vegetables", "remarks": "Includes spinach, kale, and other leafy greens"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[1, 'id'], "name": "Root Vegetables", "long_name": "Root Vegetables", "remarks": "Includes carrots, potatoes, and other root vegetables"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[2, 'id'], "name": "Milk", "long_name": "Milk Products", "remarks": "Includes all types of milk"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[2, 'id'], "name": "Cheese", "long_name": "Cheese Products", "remarks": "Includes all types of cheese"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[3, 'id'], "name": "Bread", "long_name": "Bread Items", "remarks": "Includes all types of bread"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[3, 'id'], "name": "Pastries", "long_name": "Pastries", "remarks": "Includes cakes, cookies, and other pastries"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[4, 'id'], "name": "Juices", "long_name": "Fruit Juices", "remarks": "Includes all types of fruit juices"},
    {"id": str(uuid.uuid4()), "category_id": category_df.loc[4, 'id'], "name": "Sodas", "long_name": "Sodas", "remarks": "Includes all types of sodas"}
]
sub_category_df = pd.DataFrame(sub_category_data)


# %%

# Define the product data
product_data = [
    {"id": str(uuid.uuid4()), "name": "Orange", "sub_category_id": sub_category_df.loc[0, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 3.5, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Lemon", "sub_category_id": sub_category_df.loc[0, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 2.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Strawberry", "sub_category_id": sub_category_df.loc[1, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[3, 'id'], "price": 5.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Blueberry", "sub_category_id": sub_category_df.loc[1, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[3, 'id'], "price": 6.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Spinach", "sub_category_id": sub_category_df.loc[2, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 4.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Kale", "sub_category_id": sub_category_df.loc[2, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 4.5, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Carrot", "sub_category_id": sub_category_df.loc[3, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 2.5, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Potato", "sub_category_id": sub_category_df.loc[3, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 1.5, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Whole Milk", "sub_category_id": sub_category_df.loc[4, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[1, 'id'], "price": 1.2, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Cheddar Cheese", "sub_category_id": sub_category_df.loc[5, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 7.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "White Bread", "sub_category_id": sub_category_df.loc[6, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[2, 'id'], "price": 2.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Chocolate Cake", "sub_category_id": sub_category_df.loc[7, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[2, 'id'], "price": 15.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Apple Juice", "sub_category_id": sub_category_df.loc[8, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[1, 'id'], "price": 3.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Cola", "sub_category_id": sub_category_df.loc[9, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[1, 'id'], "price": 1.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Grapefruit", "sub_category_id": sub_category_df.loc[0, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 3.0, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Raspberry", "sub_category_id": sub_category_df.loc[1, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[3, 'id'], "price": 5.5, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Lettuce", "sub_category_id": sub_category_df.loc[2, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 2.8, 'currency':'naira'},
    {"id": str(uuid.uuid4()), "name": "Beetroot", "sub_category_id": sub_category_df.loc[3, 'id'], "unit_of_measurement_id": unit_of_measurement_df.loc[0, 'id'], "price": 6.99, 'currency':'naira'}
]

product_df = pd.DataFrame(product_data)


product_df['price'] = np.where(product_df['unit_of_measurement_id'] == 2, 
                               product_df['price'] * 110, 
                               product_df['price'] * random.choice([815, 1070, 1420]))

# product_df['price'] = product_df['price']*110 if( product_df['unit_of_measurement_id'] == 2) else product_df['price'] * random.choice([815, 1070, 1420])

# %%
fake = Faker('en_GB')  # Use the English (Great Britain) locale
start_date = '2024-01-01'
end_date = '2024-09-30'
date_range = pd.date_range(start_date, end_date)
print(date_range)
# print(trans_interval)
# trans_interval = fake.date_between_dates(date_start=datetime(2024, 1, 1), date_end=datetime(2024, 9, 30))
# Generate customer data
def generate_customer():
    # sign_up_date = None
    is_active = random.random() < 0.7  # 70% chance of being active
    first_name = fake.first_name()
    last_name = fake.last_name()
    street = fake.street_address()
    state = random.choice(nigerian_states)
    country = "Nigeria"
    phone_number = fake.phone_number()
    email = fake.email()
    return {
        "id": str(uuid.uuid4()),
        "first_name": first_name,
        "last_name": last_name,
        "street": street,
        "state": state,
        "country": country,
        "credit_card_number": fake.credit_card_number(),
        # "sign_up_date": sign_up_date,
        "is_active": is_active
    }

customer_data = [generate_customer() for _ in range(53571)]
random_dates = np.random.choice(date_range, size=len(customer_data))
customer_df = pd.DataFrame(customer_data)
customer_df['sign_up_date'] = random_dates


# %%

# Filter active customers
active_customers = customer_df[customer_df['is_active']]

# Ensure 20% of active customers have sign_up_date within two weeks before September 30, 2024
two_weeks_before_end = datetime(2024, 9, 30) - timedelta(weeks=2)
recent_signups = active_customers.sample(frac=0.2)
mod_date_range = pd.date_range(two_weeks_before_end, end_date)
customer_df.loc[recent_signups.index, 'sign_up_date'] = np.random.choice(mod_date_range, size=len(recent_signups))

# Exclude recent sign-ups from active customers for transaction generation
recent_signup_ids = recent_signups['id'].tolist()
active_customers_for_transactions = active_customers[~active_customers['id'].isin(recent_signup_ids)]


# %%
customer_df['sign_up_date'].nunique()

# %%
# Assuming active_customers and product DataFrames are already defined
def generate_transaction(active_customers, product,):
    customer_id = random.choice(active_customers['id'].tolist())
    product_id = random.choice(product['id'].tolist())
    # trans_interval = datetime.now() - timedelta(days=random.randint(1, 90))  # Example transaction interval
    return {
        "transaction_id": str(uuid.uuid4()),
        "tansaction_date": None, #pd.to_datetime(trans_interval),
        "product_id": product_id,
        "quantity": random.randint(1, 1000),
        "customer_id": customer_id,
        "promo_code": None
    }

transaction_data = [generate_transaction(active_customers, product_df) for _ in range(10000000)]
transaction_df = pd.DataFrame(transaction_data)
trans_random_dates = np.random.choice(date_range, size=len(transaction_df))
transaction_df['transaction_date'] = trans_random_dates

# Calculate the average quantity of items purchased in the last month
one_month_ago = datetime(2024, 9, 30) - timedelta(days=30)
last_month_transactions = transaction_df[(transaction_df['transaction_date']) > one_month_ago]
average_quantity_last_month = last_month_transactions['quantity'].mean()

# Ensure at least 33% customers have their most recent transaction quantity greater than the average
total_customers = transaction_df['customer_id'].nunique()
required_count_for_update = int(.33 * total_customers)
recent_transactions = transaction_df.sort_values(by='transaction_date').groupby('customer_id').tail(1)
customers_to_update = recent_transactions[recent_transactions['quantity'] <= average_quantity_last_month].head(required_count_for_update)

for index, row in customers_to_update.iterrows():
    transaction_df.loc[transaction_df['transaction_id'] == row['transaction_id'], 'quantity'] = average_quantity_last_month + 1

# Calculate days of inactivity for each customer as of September 30, 2024
end_date = datetime(2024, 9, 30)
start_date = end_date - timedelta(days=90)
transactions_within_90_days = transaction_df[(transaction_df['transaction_date'] <= end_date) & (transaction_df['transaction_date'] >= start_date)]

# Calculate the average number of days between transactions
transactions_within_90_days['prev_date'] = transactions_within_90_days.groupby('customer_id')['transaction_date'].shift(1)
transactions_within_90_days['days_between'] = (transactions_within_90_days['transaction_date'] - transactions_within_90_days['prev_date']).dt.days
average_days_between = transactions_within_90_days['days_between'].mean()

# Identify customers with days of inactivity greater than the average
inactive_customers = transactions_within_90_days.groupby('customer_id').tail(1)
inactive_customers = inactive_customers[inactive_customers['days_between'] > average_days_between]

# Ensure about 30% of customers meet this inactivity criterion
required_inactive_customers = int(0.3 * total_customers)
inactive_customers_to_update = inactive_customers.head(required_inactive_customers)

# Update the transaction DataFrame as needed
# (This part depends on what specific updates you want to make for these inactive customers)

print(transaction_df.head())


# %%
promo_recipient_list  = list(set(customers_to_update['customer_id'].to_list()+recent_signup_ids+inactive_customers_to_update['customer_id'].to_list()))
non_promo_recipients = transaction_df[~transaction_df['customer_id'].isin(promo_recipient_list)]
required_non_promo_recipients = int(0.5*(non_promo_recipients['customer_id'].nunique()))
required_non_promo_recipients_list = non_promo_recipients['customer_id'].drop_duplicates().to_list()[:required_non_promo_recipients] 
oct_transaction_generator = required_non_promo_recipients_list + promo_recipient_list
oct_transaction_generator = pd.DataFrame({'id':oct_transaction_generator})
oct_date_rage = pd.date_range('2024-10-01', '2024-10-31')
oct_transaction_data = [generate_transaction(oct_transaction_generator,product_df) for _ in range(1300000)]
oct_transaction_data_df = pd.DataFrame(oct_transaction_data)
oct_random_dates = np.random.choice(oct_date_rage, size=len(oct_transaction_data_df))
oct_transaction_data_df['transaction_date'] = oct_random_dates

# %%
transaction_df_final = pd.concat(
    [transaction_df, oct_transaction_data_df], 
    ignore_index = True
)

# %%
dir_ = 'data/csv'
table_attr = {
    'unit_of_measurement.csv':unit_of_measurement_df,
    'category.csv':category_df,
    'sub_category.csv':sub_category_df,
    'product.csv':product_df,
    'transaction.csv':transaction_df_final,
    'promotion.csv':promotion_df ,
    'customer.csv':customer_df  
}

[save_csv(v, dir_, k) for k,v in table_attr.items()]

# # %%
# from sklearn.model_selection import train_test_split

# # Assuming transaction_df_final is already defined

# # Sort the DataFrame by 'transaction_id' to ensure consistent splitting
# transaction_df_final = transaction_df_final.sort_values(by='transaction_id')

# # Split into 40% and 60% 
# smaller_df, larger_df = train_test_split(transaction_df_final, test_size=0.6, random_state=42)
# installment_1 = smaller_df.copy()
# installment_1['paymnet_mode'] = 'card'
# installment_1['payment_date'] = installment_1['transaction_date']
# installment_2, installment_3_4 = train_test_split(larger_df, test_size=0.26, random_state=42)
# installment_2['paymnet_mode'] = np.where(installment_2['quantity'] > 100, 'direct debit', 'cash bank transfer')



# %%)

# Now you have two DataFrames:
# - smaller_df: Contains 40% of the data
# - larger_df: Contains 60% of the data



