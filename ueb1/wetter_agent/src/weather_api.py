import requests


class WeatherAPI:
    api_key = ""
    base_request_url = "https://api.weatherbit.io/v2.0"
    
    def get_current_forecast(self, city_name):   
        full_request_url = self.base_request_url + "/current"

        params = dict(
            key=self.api_key,
            city=city_name
        )
        
        response = requests.get(url=full_request_url, params=params)
        
        if response is None:
            raise NoResponseException
        
        try:
            response.json()
        except:
            raise ResponseReadError
        
        if not len(response.json().get("data")) >= 1:
            raise NoDataInResponseException            
        
        forecast_data = response.json().get("data")[0]
        
        return forecast_data

    def get_forecast_attribute_by_name(self, forecast_data, attribute_name):
        if attribute_name not in forecast_data:
            raise ForecastAttributeNonExistantException

        return forecast_data.get(attribute_name)


class NoResponseException(Exception):
    pass


class ResponseReadError(Exception):
    pass


class NoDataInResponseException(Exception):
    pass


class ForecastAttributeNonExistantException(Exception):
    pass

