from faker import Faker
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

# --- CONFIGURATION ---
# The number of fake data records to generate
NUMBER_OF_RECORDS = 2000

# The name of the output CSV file
OUTPUT_FILE = Path("synthetic_customer_data.csv")
# ---------------------

def generate_customer_data(count: int) -> List[Dict[str, Any]]:
    """
    Generates a list of synthetic customer data using the Faker library.
    """
    # Initialize Faker. You can specify a locale, e.g., 'en_US'.
    fake = Faker()
    customers = []
    
    print(f"Generating {count} records of customer data...")
    
    for _ in range(count):
        customers.append({
            "customer_id": fake.uuid4(),
            "full_name": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "address": fake.address().replace('\n', ', '),
            "country": fake.country(),
            "signup_date": fake.date_this_decade(),
            "last_login_ip": fake.ipv4(),
            "total_spent": round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
        })
    return customers

def main():
    """
    Main function to generate data and save it to a CSV file.
    """
    try:
        customer_data = generate_customer_data(NUMBER_OF_RECORDS)
        
        # Convert the list of dictionaries to a Pandas DataFrame
        # This is a highly efficient way to handle tabular data
        df = pd.DataFrame(customer_data)
        
        # Save the DataFrame to a CSV file without the default Pandas index
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        
        print(f"\n✅ Successfully generated {NUMBER_OF_RECORDS} records in '{OUTPUT_FILE}'")
        print("Here are the first 5 rows:")
        print(df.head())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
