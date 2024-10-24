import pandas as pd
import numpy as np

def csv_to_sql(csv_file_path, table_name):
    """
    Reads a CSV file into a pandas DataFrame, converts it to SQL CREATE and INSERT statements,
    and saves the SQL code to a file.

    Args:
        csv_file_path (str): The path to the CSV file.
        table_name (str): The name of the SQL table.

    Returns:
        str: The path to the generated SQL file.
    """

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Create the SQL CREATE TABLE statement
    create_table_sql = f"""
    CREATE TABLE {table_name} (
    """
    for column in df.columns:
        data_type = "VARCHAR(255)"  # Default data type
        if df[column].dtype == np.int64:
            data_type = "INT"
        elif df[column].dtype == np.float64:
            data_type = "DECIMAL(10,2)"
        create_table_sql += f"    {column} {data_type},"
    create_table_sql = create_table_sql[:-1] + "\n"  # Remove trailing comma and add newline
    create_table_sql += ");"

    # Create the SQL INSERT statements
    insert_statements_sql = ""
    for index, row in df.iterrows():
        values = ", ".join([f"'{str(value)}'" for value in row.values])
        insert_statements_sql += f"INSERT INTO {table_name} VALUES ({values});\n"

    # Combine the CREATE TABLE and INSERT statements
    sql_code = create_table_sql + "\n" + insert_statements_sql

    # Save the SQL code to a file
    sql_file_path = csv_file_path.replace(".csv", ".sql")
    with open(sql_file_path, "w") as f:
        f.write(sql_code)

    return sql_file_path

# %%
# Example usage
csv_file_path = "data/customer.csv"
table_name = "customer"