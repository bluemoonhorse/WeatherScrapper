from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from prettytable import PrettyTable
import logging
from prettytable import MSWORD_FRIENDLY

time_array = []
temperature_array = []
weather_array = []

options = Options()
options.add_argument("--headless")
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)
logging.basicConfig(filename='error.log', level=logging.ERROR)

title = None
location_text = None
today_forecast = None
try:
    driver.get("https://p.ya.ru/minsk")
    title = driver.title
except Exception as e:
    logging.error('Failed to get page: ' + str(e))

try:
    location_text = driver.find_element(By.CLASS_NAME, "temperature-wrapper").text
    location_text = location_text.replace('\n', ' ')
except Exception as e:
    logging.error('Failed to get location data: ' + str(e))


try:
    today_forecast = driver.find_element(By.CLASS_NAME, "today-forecast").text
except Exception as e:
    logging.error('Failed to get forecast data: ' + str(e))

try:
    elements_temperature = driver.find_elements(By.CLASS_NAME, "temp-chart__temp")
    for element in elements_temperature:
        temperature_array.append(element.text)
except Exception as e:
    logging.error('Failed to get temperature data: ' + str(e))

try:
    elements_time = driver.find_elements(By.CLASS_NAME, "temp-chart__hour")
    for element in elements_time:
        time_array.append("".join(filter(str.isdecimal, element.text)))
except Exception as e:
    logging.error('Failed to get hour data: ' + str(e))

try:
    elements_weather = driver.find_elements(By.CLASS_NAME, "icon_size_24")
    for element in elements_weather:
        # there's only rain for now since its winter, will add snow etc later when it shows up on website
        string = element.get_attribute("class")
        string = string.replace("icon icon_size_24", "")
        string = string.replace("icon_", "")
        if string == " rain":
            string = "☔☔☔"
        elif string == "":
            string = "☀️☀️☀️"
        else:
            string += " (ㅠ﹏ㅠ)"
            raise ValueError("Undefined weather")

        weather_array.append(string)
except Exception as e:
    logging.error('Failed to get hour data: ' + str(e))

    table = None
try:
    table = PrettyTable()
    table.set_style(MSWORD_FRIENDLY)
    table.add_column("Time", time_array)
    table.add_column("Temperature", temperature_array)
    table.add_column("Weather", weather_array)
except Exception as e:
    logging.error('Failed to compile table: ' + str(e))

print(title)
print(table)
print(today_forecast)
print(location_text)

# Close the browser
driver.quit()
