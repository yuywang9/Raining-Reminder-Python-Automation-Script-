import requests
import time
import os
import os.path

def Get_Weather(api, city, backoff=2, retries=100): 
    """
    Get the weather data for a given city using the WeatherAPI.com.
    """

    url="http://api.weatherapi.com/v1/forecast.json"

    """Define the parameters(You can also defined the days parameter to get the weather forcast,
    if not mentioned, only today's weather will be provided)"""
    parameters={
        'key': api,
        'q': city,
        'days': 1,
    }

    for attempt in range(retries):
        response = requests.get(url, params=parameters)

        #Here, we check the first issue which is status code
        if response.status_code == 200:
            #Here, we check the second issue which is JSONDecodeError
            try:
                weather_data = response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Unable to decode JSON response.")
                print("Response content:", response.text)
                
            # #Here, we check the third issue if 'current' object has fields
            if 'forecast' in weather_data and weather_data['forecast']:
                return weather_data
        else:
            print(f"Error: {response.status_code}")
            print("Response content:", response.text)
        
        time.sleep(backoff * (attempt + 1))

    print("From Get_Weather: Failed to retrieve valid weather data after attempts.")
    return None

def is_rainning(Weather_Text):
    Weather_Text=Weather_Text.lower()
 
    if 'rain' in Weather_Text or 'shower' in Weather_Text or 'drizzle' in Weather_Text:
        return True

    return False

def send_message(bot_api_key, channel_name, text, last_message_id=None):
    """
    Send a message to the Telegram channel and return the message ID.
    If last_message_id is provided, delete the previous message before sending a new one.
    """
    if last_message_id:#For the first message, this condition will not be triggered
        delete_url = f'https://api.telegram.org/bot{bot_api_key}/deleteMessage'
        delete_response = requests.get(delete_url, params={'chat_id': channel_name, 'message_id': last_message_id})
        if delete_response.status_code != 200:
            print(f"Failed to delete message: {delete_response.status_code}")
    
    send_url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'
    response = requests.get(send_url, params={'chat_id': channel_name, 'text': text})
    
    if response.status_code == 200:
        return response.json().get('result', {}).get('message_id')
    else:
        print(f"Failed to send message: {response.status_code}")
        print(response.text)
        return None

def read_last_message_id(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read().strip()#removes any leading and trailing whitespace, including newlines, from the string, but will keep the space bewteen the characters.
    return None

def write_last_message_id(last_message_file, last_message_id):
    with open(last_message_file, 'w') as file:
        file.write(str(last_message_id))

def main():
    city="Hong Kong"
    api="******************"
    BOT_API_KEY="***********************"
    CHANNEL_NAME="@Freya_Kris"
    last_message_file = 'Last_Message_ID.txt'
    #Last Message ID is stored in this file, or each time the main function run, the Last Message ID is deleted.

    last_message_id = read_last_message_id(last_message_file)

    Weather_Data=Get_Weather(api,city)
    """Weather_Data is a json file"""

    if Weather_Data:
        print("Weather data received")
        # print(Weather_Data)
        #Weather data here is forecast

        hourly_forecast = Weather_Data["forecast"]["forecastday"][0]["hour"]
        raining_periods = []
        raining = False
        start_time = None
        end_time = None

        for hour in hourly_forecast:
            time_str=hour["time"].split(" ")[1]
            if "07:00"<=time_str<="23:00":
                weather_text=hour["condition"]["text"]
                if is_rainning(weather_text):#When it is raining
                    if not raining: #when it is the situation where it is the start of a raining period
                        start_time=time_str
                        raining=True
                    else: #when it is the situation where it is in the period of raining
                        pass
                else: #When it is not raining
                    if raining: #when it is not raining but the end of the raining period
                        end_time=time_str
                        raining=False
                        raining_periods.append(f"{start_time} to {end_time}")
                    else:#When it is not raining and not the end of the period
                        pass

        #Remember, the period is determined when the end of the raining period is met, but what if the weather 
        #keeps raining until 23:00, which is the last hour report, then we have to deal with this situation
        if raining:
            raining_periods.append(f"{start_time} to 00:00")
        
        if raining_periods:
            text = f" \U00002614 It will rain in {city} during the following periods today:\n" + "\n".join(raining_periods) + "\nYou may consider to bring umbrella!"
        else:
            text = f"\U0001F60A It's not raining today in {city}. Enjoy!"

        print(text)
        last_message_id = send_message(BOT_API_KEY, CHANNEL_NAME, text, last_message_id)
        #Even if it is the first time to send messages, we can still get last_message_id
        if last_message_id:
            write_last_message_id(last_message_file, last_message_id)
        
    else:
        print("From main: Failed to retrieve weather data.")

if __name__ == "__main__":
    main()