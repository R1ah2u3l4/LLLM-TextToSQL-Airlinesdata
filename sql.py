import sqlite3
import pandas as pd

# Connect to sqlite
connection = sqlite3.connect("Airlines.db")

# Create a cursor object to insert records, create table, retrieve
cursor = connection.cursor()

# Create table info
table_info = """
CREATE TABLE PassengerData (
    PassengerID INT PRIMARY KEY,
    FirstName VARCHAR(25),
    LastName VARCHAR(25),
    Gender VARCHAR(10),
    Age INT,
    Nationality VARCHAR(35),
    AirportName VARCHAR(30),
    AirportCountryCode VARCHAR(25),
    CountryName VARCHAR(35),
    AirportContinent VARCHAR(35),
    Continents VARCHAR(30),
    DepartureDate DATE,
    ArrivalAirport VARCHAR(35),
    PilotName VARCHAR(35),
    FlightStatus VARCHAR(20)
);

"""

# Execute the table creation statement
cursor.execute(table_info)

## Read the data from Csv file

df = pd.read_csv(r'C:\Users\hp\Downloads\archive (6)\Airline Dataset Updated - v2.csv')
df

# Insert data into SQLlite table
df.to_sql('Airlines', connection, if_exists='replace', index=False)

## Display all records
print("Inserted Records are :")

data = cursor.execute("Select * from Airlines")

for row in data:
    print(row)


# Commit the changes in database

connection.commit()
connection.close()