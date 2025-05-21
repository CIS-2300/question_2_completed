Question 2


This Python script is designed to collect, merge, analyze, and store COVID-19 data using two sources: a web page and an API. The overall goal is to compile a dataset that includes both scraped and API-based information for the top 30 countries affected by COVID-19 and then store that data for further use.

The script begins by scraping data from the Worldometers website using the scrape_covid_data() function. It sends an HTTP request to the URL https://www.worldometers.info/coronavirus/, parses the HTML using BeautifulSoup, and extracts the relevant table that contains COVID-19 statistics by country. It selects the first 30 countries listed in the table and focuses on specific columns such as Country, Total Cases, New Cases, Total Deaths, New Deaths, Total Recovered, and Active Cases. The data is then cleaned by removing commas and plus signs and converted to numeric types.

Next, the script retrieves additional data from the RapidAPI COVID-19 API using the get_covid_api_data() function. This function sends a request for each country using the API endpoint and collects information including the total number of confirmed cases, recovered cases, deaths, the fatality rate, and the last update date. If the API call fails for any reason, the function returns default values (zero or empty strings) to ensure the process continues without interruption. The function create_api_dataframe() then compiles these API responses into a second DataFrame.

After both data sources are prepared, the script merges them using the pd.concat() function along the columns, creating a combined DataFrame named df3. It then prints a preview of the combined data and displays descriptive statistics using the describe() method, which provides summary metrics such as the mean, standard deviation, and percentiles for the numerical data.

The script concludes by saving the combined data to a CSV file named covid_combined_data.csv and storing it in a SQLite database file named covid_data.db under the table name combined_covid_data. These actions make the dataset easy to access later for analysis, reporting, or visualization.

To execute all of these steps, the main() function orchestrates the workflow: it calls the scraping function, gathers API data, merges the datasets, displays summaries, and then saves the data. This function is run when the script is executed directly.

Before running the script, the user must replace "YOUR_API_KEY" in the header of the API request with a valid RapidAPI key.

This script is useful for researchers, analysts, or developers who want to automate the collection and integration of COVID-19 data from multiple sources into a clean and structured format.


