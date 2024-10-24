# %%
from faker import Faker
import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
from sklearn.model_selection import train_test_split
import unittest
from data_generator import generate_customer, generate_transaction, save_csv, nigerian_states

class TestDataGenerator(unittest.TestCase):

    def test_generate_customer(self):
        customer = generate_customer()
        self.assertIsInstance(customer, dict)
        self.assertIn('id', customer)
        self.assertIsInstance(customer['id'], str)
        self.assertIn('first_name', customer)
        self.assertIsInstance(customer['first_name'], str)
        self.assertIn('last_name', customer)
        self.assertIsInstance(customer['last_name'], str)
        self.assertIn('street', customer)
        self.assertIsInstance(customer['street'], str)
        self.assertIn('state', customer)
        self.assertIn(customer['state'], nigerian_states)
        self.assertIn('country', customer)
        self.assertEqual(customer['country'], "Nigeria")
        self.assertIn('credit_card_number', customer)
        self.assertIsInstance(customer['credit_card_number'], str)
        self.assertIn('is_active', customer)
        self.assertIsInstance(customer['is_active'], bool)

    def test_generate_transaction(self):
        # Create sample active customers and product dataframes
        active_customers = pd.DataFrame({'id': [str(uuid.uuid4()) for _ in range(5)]})
        product = pd.DataFrame({'id': [str(uuid.uuid4()) for _ in range(10)]})

        transaction = generate_transaction(active_customers, product)
        self.assertIsInstance(transaction, dict)
        self.assertIn('transaction_id', transaction)
        self.assertIsInstance(transaction['transaction_id'], str)
        self.assertIn('tansaction_date', transaction)
        self.assertIsInstance(transaction['tansaction_date'], type(None))
        self.assertIn('product_id', transaction)
        self.assertIn(transaction['product_id'], product['id'].tolist())
        self.assertIn('quantity', transaction)
        self.assertIsInstance(transaction['quantity'], int)
        self.assertIn('customer_id', transaction)
        self.assertIn(transaction['customer_id'], active_customers['id'].tolist())
        self.assertIn('promo_code', transaction)
        self.assertIsNone(transaction['promo_code'])

    def test_save_csv(self):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        directory = 'test_data'
        filename = 'test.csv'
        file_path = save_csv(df, directory, filename)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)
        os.rmdir(directory)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

