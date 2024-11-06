import sqlite3
import pandas as pd
import os
from datetime import date, timedelta
from twilio.rest import Client

# Your Account SID and Auth Token from twilio.com/console
# Set environment variables for security
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

def execute_sql_and_save_csv(sql_file_path, db_file_path, output_dir='summary'):
    """Executes an SQL query, saves the result as a CSV, and returns the file path."""
    with open(sql_file_path, 'r') as file:
        sql_query = file.read()

    conn = sqlite3.connect(db_file_path)
    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    df['date'] = date.today().strftime('%Y-%m-%d')
    os.makedirs(output_dir, exist_ok=True)
    csv_file_path = os.path.join(output_dir, f"data_{date.today().strftime('%Y-%m-%d')}.csv")
    df.to_csv(csv_file_path, index=False)
    return csv_file_path

def compare_single_row_data(today_csv, yesterday_csv, phone_numbers):
    """Compares single-row data between two CSV files and sends differences."""
    df_today = pd.read_csv(today_csv)
    df_yesterday = pd.read_csv(yesterday_csv)

    # Ensure only comparing single-row dataframes
    if len(df_today) != 1 or len(df_yesterday) != 1:
        print("Error: Input CSV files should contain only one row.")
        return

    differences = []
    for col in df_today.columns:
        if df_today[col].iloc[0] != df_yesterday[col].iloc[0]:
            differences.append(f"- {col}: {df_yesterday[col].iloc[0]} -> {df_today[col].iloc[0]}")

    if differences:
        message = "Data Differences:\n" + "\n".join(differences)
        for number in phone_numbers:
            send_whatsapp_message(message, number)
    else:
        print("No differences found.")

def send_whatsapp_message(message, to_number):
    """Sends a WhatsApp message using Twilio."""
    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Replace with your Twilio WhatsApp number
        to=f'whatsapp:{to_number}'
    )
    print(f"Message sent to {to_number}: {message.sid}")

if __name__ == "__main__":
    sql_file = "your_sql_query.sql" 
    database_file = "your_database.db" 
    whatsapp_numbers = ["+1234567890", "+1987654321"]  # Add recipient numbers

    today_csv = execute_sql_and_save_csv(sql_file, database_file)
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_csv = os.path.join("summary", f"data_{yesterday}.csv")

    if os.path.exists(yesterday_csv):
        compare_single_row_data(today_csv, yesterday_csv, whatsapp_numbers)
    else:
        print("Yesterday's data file not found. Skipping comparison.")
