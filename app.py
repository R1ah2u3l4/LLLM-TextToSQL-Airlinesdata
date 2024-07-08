from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Configure Genai Key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print("API Key Loaded")  # Print a confirmation that the API key is loaded
    genai.configure(api_key="AIzaSyDo7B9rv_03XBea9NiByw1yJq0ZjA-luEk")
else:
    raise ValueError("API Key not found in environment variables.")

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Airlines and has the following columns - Passenger ID, First Name,	Last Name, Gender,	Age, Nationality,	
    Airport Name, Airport Country Code,	Country Name, Airport Continent, Continents, Departure Date, Arrival Airport, Pilot Name, Flight Status
     \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM Airlines ;
    \nExample 2 - Find the Number of Flights Departing from Each Country
    the SQL command will be something like this SELECT CountryName, COUNT(*) AS NumberOfFlights FROM PassengerData GROUP BY CountryName;
    \nExample3 - Count the Number of Passengers by Airport Continent
    SELECT AirportContinent, COUNT(*) AS Count FROM PassengerData GROUP BY AirportContinent;
    \nExample4 - List All Pilots and the Number of Flights They Are Operating
    SELECT PilotName, COUNT(*) AS NumberOfFlights FROM PassengerData GROUP BY PilotName;
    \nExample5 - Find the number of flights by Flight Status
    SELECT FlightStatus, COUNT(*) AS Count FROM PassengerData GROUP BY FlightStatus;
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)  # Print the generated SQL query for debugging
    response_data = read_sql_query(response, "Airlines.db")
    st.subheader("The Response is")
    for row in response_data:
        print(row)
        st.write(row)  # Display each row in the Streamlit interface
