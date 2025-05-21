import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Part 1: Web Scraping to create DF1
def scrape_covid_data():
    url = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', id='main_table_countries_today')
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = []

    for tr in table.find_all('tr')[1:31]:  # Get first 30 records
        row = [td.text.strip() for td in tr.find_all('td')]
        rows.append(row)

    df1 = pd.DataFrame(rows, columns=headers)
    # Clean up column names and select relevant columns
    df1 = df1[['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases']]
    df1.columns = ['Country', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases']

    # Convert numeric columns
    numeric_cols = ['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 'TotalRecovered', 'ActiveCases']
    for col in numeric_cols:
        df1[col] = df1[col].str.replace(',', '').str.replace('+', '')
        df1[col] = pd.to_numeric(df1[col], errors='coerce').fillna(0)

    return df1

# Part 2: API Requests to create DF2
def get_covid_api_data(country):
    url = "https://covid-19-data.p.rapidapi.com/country"
    querystring = {"name": country}
    headers = {
        'x-rapidapi-key': "YOUR_API_KEY",  # Replace with your actual API key
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()[0]

        return {
            'API_Confirmed': data.get('confirmed', 0),
            'API_Recovered': data.get('recovered', 0),
            'API_Deaths': data.get('deaths', 0),
            'API_FatalityRate': data.get('fatalityRate', 0),
            'API_LastUpdate': data.get('lastUpdate', '')
        }
    except:
        return {
            'API_Confirmed': 0,
            'API_Recovered': 0,
            'API_Deaths': 0,
            'API_FatalityRate': 0,
            'API_LastUpdate': ''
        }

def create_api_dataframe(countries):
    api_data = []
    for country in countries:
        api_data.append(get_covid_api_data(country))

    df2 = pd.DataFrame(api_data)
    return df2

# Main execution
def main():
    # Create DF1
    df1 = scrape_covid_data()
    print("Scraped Data (DF1):")
    print(df1.head())

    # Create DF2
    countries = df1['Country'].tolist()
    df2 = create_api_dataframe(countries)
    print("\nAPI Data (DF2):")
    print(df2.head())

    # Create DF3 by merging DF1 and DF2
    df3 = pd.concat([df1, df2], axis=1)
    print("\nCombined Data (DF3):")
    print(df3.head())

    # Display statistics
    print("\nDescriptive Statistics:")
    print(df3.describe())

    # Export to CSV
    df3.to_csv('covid_combined_data.csv', index=False)
    print("\nData exported to covid_combined_data.csv")

    # Store in SQLite database
    conn = sqlite3.connect('covid_data.db')
    df3.to_sql('combined_covid_data', conn, if_exists='replace', index=False)
    conn.close()
    print("Data stored in SQLite database 'covid_data.db'")

if __name__ == "__main__":
    main()