import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Function to fetch F1 fixtures for the current year
def get_f1_fixtures():
    url = "https://ergast.com/api/f1/current.json"
    response = requests.get(url)
    data = response.json()

    races = []
    for race in data['MRData']['RaceTable']['Races']:
        race_info = {
            'Race Name': race['raceName'],
            'Circuit': race['Circuit']['circuitName'],
            'Date': race['date'],
            'Location': race['Circuit']['Location']['locality']
        }
        races.append(race_info)

    return pd.DataFrame(races)

# Function to fetch Cricket fixtures for the current year
def get_cricket_fixtures():
    url = 'https://api.cricapi.com/v1/series?apikey=' # Add your API KEY
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        series = []
        if 'data' in data:
            for series_info in data['data']:
                
                try:
                    series_start_date = datetime.strptime(series_info['startDate'], "%Y-%m-%d").date()
                    series_end_date = datetime.strptime(series_info['endDate'], "%Y-%m-%d").date()
                except ValueError:
                    series_start_date = None
                    series_end_date = None

                # Determine the series status based on the current date
                current_date = datetime.now().date()

                if series_start_date and series_end_date:
                    if current_date < series_start_date:
                        status = "Scheduled"
                    elif series_start_date <= current_date <= series_end_date:
                        status = "Ongoing"
                    else:
                        status = "Finished"
                else:
                    status = " "

                series_info_dict = {
                    'Series Name': series_info['name'],
                    'Start Date': series_info['startDate'],
                    'End Date': series_info['endDate'],
                    'ODIs': series_info['odi'],
                    'T20s': series_info['t20'],
                    'Tests': series_info['test'],
                    'Matches Loaded': series_info['matches'],
                    'Status': status  
                }
                series.append(series_info_dict)

            return pd.DataFrame(series)
        else:
            return pd.DataFrame()  
    else:
        return pd.DataFrame()  

# Function to fetch Football fixtures for the current year
def get_football_fixtures():
    api_token = ""  # Add your API KEY
    headers = {"X-Auth-Token": api_token}

    competitions = {
        "PL": "Premier League",
        "PD": "La Liga"
    }

    all_fixtures = []

    for code, name in competitions.items():
        url = f"https://api.football-data.org/v4/competitions/{code}/matches?season=2024"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for match in data.get('matches', []):
                fixture = {
                    'Competition': name,
                    'Matchday': match.get('matchday'),
                    'Date': match.get('utcDate'),
                    'Home Team': match['homeTeam']['name'],
                    'Away Team': match['awayTeam']['name'],
                    'Status': match['status']
                }
                all_fixtures.append(fixture)
        else:
            print(f"Failed to fetch {name} fixtures: Status code {response.status_code} - {response.text}")

    return pd.DataFrame(all_fixtures)

# Main function for Streamlit UI
def main():
    st.title("Sports Fixtures")

    current_year = datetime.now().year

    sport = st.selectbox("Select sport", ["Football", "F1", "Cricket"])

    # F1 fixtures
    if sport == "F1":
        f1_fixtures = get_f1_fixtures()
        st.write(f1_fixtures)

    # Cricket fixtures
    elif sport == "Cricket":
        cricket_fixtures = get_cricket_fixtures()
        st.write(cricket_fixtures)

    # Football fixtures
    elif sport == "Football":
        football_fixtures = get_football_fixtures()
        st.write(football_fixtures)

# Call the main function to run the app
if __name__ == "__main__":
    main()
