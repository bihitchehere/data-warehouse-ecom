from faker import Faker
import pandas as pd

fake = Faker()

def connect():
    # Generate 1000 fake names
    names = [fake.name() for _ in range(10000)]
    emails = [fake.email for _ in range(10000)]
    signup_dates = [fake.date_time_between_dates(datetime_start='-30y', datetime_end='now') for _ in range(10000)]
    # Create a DataFrame
    data = pd.DataFrame({'name': names,'emails': emails , 'signup_dates':signup_dates})

    
    print(data.head())

if __name__ == "__main__":
    connect()
