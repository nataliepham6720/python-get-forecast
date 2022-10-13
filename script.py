from pathlib import Path
from geopy.geocoders import Nominatim
import requests
import pandas as pd


def get_forecast( city='Pittsburgh' ):
    '''
    Returns the nightly's forecast for a given city.
    Inputs:
    city (string): A valid string
    Output:
    period (dictionary/JSON): a dictionary containing at least, the forecast keys startTime, endTime and detailedForecast.
    Throws:
    CityNotFoundError if geopy returns empty list or if the latitude longitude fields are empty.
    ForecastUnavailable if the period is empty or the API throws any status code that is not 200
    Hint:
    * Return the period that is labeled as "Tonight"
    '''
    geolocator = Nominatim(user_agent='ModernProgramming')
    location = geolocator.geocode('Pittsburgh',language='en')
    latitude = location.latitude
    longitude = location.longitude
    if not(bool(latitude) and bool(longitude)):
        warnings.warn('CityNotFoundError')
        return None
    else:
        URL = f'https://api.weather.gov/points/{latitude},{longitude}'
        response = requests.get(URL)
        if response.status_code != 200:
            warnings.warn('CityNotFoundError')
            return None
        else:
            forecast_link = response.json().get('properties').get('forecast')
            resp = requests.get(forecast_link)
            if resp.status_code != 200:
                warnings.warn('ForecastUnavailable')
                return None
            else:
                period = pd.DataFrame(resp.json().get('properties').get('periods'),copy=True)
                if period.shape[0] == 0:
                    warnings.warn('ForecastUnavailable')
                    return None
                else:
                    forecast = period[period['name']=='Tonight']
                    return(forecast['startTime'],forecast['endTime'], forecast.iloc[0,12])
            
    return response

    raise NotImplementedError()
    raise NotImplementedError()
    

def main():
    period = get_forecast()

    file = 'weather.pkl'

    if Path(file).exists():
        df = pd.read_pickle( file )
    else:
        df = pd.DataFrame(columns=['Start Date', 'End Date', 'Forecast'])

    df = df.append({'Start Date': period['startTime'], 'End Date': period['endTime'], 'Forecast': period['detailedForecast']}, ignore_index=True)
    df = df.drop_duplicates()
    df.to_pickle(file)

    #sort repositories
    file = open("README.md", "w")
    file.write('![Status](https://github.com/nataliepham6720/python-get-forecast/actions/workflows/build.yml/badge.svg)\n')
    file.write('![Status](https://github.com/nataliepham6720/python-get-forecast/actions/workflows/pretty.yml/badge.svg)\n')
    file.write('# Pittsburgh Nightly Forecast\n\n')
    
    file.write(df.to_markdown(tablefmt='github'))
    file.write('\n\n---\nCopyright © 2022 Pittsburgh Supercomputing Center. All Rights Reserved.')
    file.close()

if __name__ == "__main__":
    main()
