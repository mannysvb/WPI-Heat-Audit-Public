# Software adapted from https://blog.gypsyengineer.com/en/diy-electronics/weather-station-based-on-esp32-and-micropython.html

import time
import network
import machine
from machine import Pin, I2C
import dht20
import gc
from config import Config
from google.auth import ServiceAccount
from google.sheet import Spreadsheet
import ntptime
from logger import Logger
from sleep import check_deepsleep, deepsleep
import sys

### ----- EDIT THESE CONSTANTS ----- ###

# This determines which spreadsheet this sensor will upload data to
# Each sheet made within the Google Spreadsheet is defined as a location, therefore if you add a sheet named "Grasslands" the SENSOR_LOCATION should be "Grasslands"

SENSOR_LOCATION = "" # <----- Edit this 

# Determines what the sensor will do upon encountering an error
# If True: the sensor halts execution
# If False: the sensor sleeps until the next reading time and retries when it awakes 
STOP_UPON_ERROR = False # <----- Should keep this as False

# The number of readings the sensor will take per day, evenly distributed throughout the day
# For example, if 24, it will take a reading every hour, on the hour
# If 12, it will take a reading every odd hour, on the hour
READINGS_PER_DAY = 24

# The maximum number of lines in the log.txt file. If the length exceeds this number,
# the log file will automatically shorten to half this number, deleting older entries first
MAX_LOG_LENGTH = 100

# The WiFi network that this sensor will attempt to connect to
# This should be ["NETWORK_1", "NETWORK_2", "NETWORK_3"]
WIFI_OPTIONS = ["NETWORK_1", "NETWORK_2", "NETWORK_3"]

# A labelled list of all WiFi networks this sensor can connect to. Will attempt to connect
# to whichever entry has the same label written in "WIFI_OPTIONS"
# If the WiFi information changes, make sure to replace the new credentials
WIFI_INFO = {
    "NETWORK_1":    {"ssid": "INSERT SSID HERE", "password": "INSERT PASSWORD HERE"},
    "NETWORK_2":    {"ssid": "INSERT SSID HERE", "password": "INSERT PASSWORD HERE"},
    "NETWORK_3":    {"ssid": "INSERT SSID HERE", "password": "INSERT PASSWORD HERE"}
}

### ----- BE CAREFUL EDITING THESE ----- ###

LOG_EXCEPTIONS = True
HAS_DHT_SENSOR = True
LOG_FILE_PATH = "log.txt"
AUTO_SHORTEN_LOG = True
logger = Logger(LOG_FILE_PATH, MAX_LOG_LENGTH, AUTO_SHORTEN_LOG)

NTP_SYNC = True
RETRY_LIMIT = 50

# Gives the number of ms to wait such that the reading is uploaded at the exact correct time (determined by READINGS_PER_DAY)


def time_to_next_reading():

    # Records current time
    hour_increment = int(24/READINGS_PER_DAY)
    local_time = time.localtime()
    current_hour = local_time[3]
    current_minutes = local_time[4]
    current_seconds = local_time[5]

    current_reading_hour = hour_increment
    next_reading_hour = 24

    # Finds time for next reading
    while (current_reading_hour < 24):
        if (current_reading_hour > current_hour):
            next_reading_hour = current_reading_hour
            break
        current_reading_hour += hour_increment

    # Calculates the amount of time until the next reading should occur
    hour_delta = next_reading_hour - current_hour - 1
    minute_delta = 60 - current_minutes - 1
    seconds_delta = 60 - current_seconds
    seconds_wait = hour_delta * 60 * 60 + minute_delta * 60 + seconds_delta
    return seconds_wait * 1000

# Blinks the onboard LED a given number of times repeatedly. Used in debugging.


def repeat_blink(number):
    while True:
        blink(number)
        time.sleep_ms(300)

# Blinks the onboard LED a given number of times


def blink(number):
    led = Pin("LED", Pin.OUT)
    for i in range(0, number):
        led.on()
        time.sleep_ms(250)
        led.off()
        time.sleep_ms(250)


def get_best_wifi(wlan):
    scan = wlan.scan()
    results = {}
    for wifi in WIFI_OPTIONS:
        for nw in scan:
            if (str(nw[0]) == "b'" + WIFI_INFO[wifi]["ssid"] + "'"):
                # print(WIFI_INFO[wifi]["ssid"] + " RSSI: " + str(nw[-3]))
                if (wifi in results.keys() and nw[-3] > results[wifi] or wifi not in results.keys()):
                    results[wifi] = nw[-3]

    best_wifi = None
    best_RSSI = -9999
    for wifi in results:
        if results[wifi] > best_RSSI:
            best_RSSI = results[wifi]
            best_wifi = wifi
    print(results)
    return best_wifi

# Connects to WiFi


def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    connected = False
    counter = 0
    while not connected and counter < RETRY_LIMIT:
        best_wifi = None
        while best_wifi == None:
            best_wifi = get_best_wifi(wlan)

        ssid = WIFI_INFO[best_wifi]["ssid"]
        password = WIFI_INFO[best_wifi]["password"]

        print("Connecting to " + ssid + ', ' + password)

        # Attempts to connect
        wlan.connect(ssid, password)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('Waiting for connection...')
            time.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            counter += 1
            if (counter < RETRY_LIMIT):
                print("WiFi connection failed, retrying attempt " +
                      str(counter) + "...\n")
            else:
                print("WiFi failed to connect")
                logger.log_error("WiFi failed to connect")
                handle_error()
        else:
            status = wlan.ifconfig()
            print('Connected to ' + ssid + '. ' + 'Device IP: ' + status[0])
            connected = True

# Syncs time using NTP Server


def sync_time():
    ntpset = False
    counter = 0
    while not ntpset and counter < RETRY_LIMIT:
        try:
            ntptime.settime()
        except:
            counter += 1
            if (counter < RETRY_LIMIT):
                print("NTP failed, retrying attempt " + str(counter) + "...")
                time.sleep(1)
            else:
                print("NTP failed to sync time")
                logger.log_error("NTP failed to sync time")
                handle_error()
        else:
            print("NTP success\n")
            ntpset = True

# Deep Sleeps until next reading should be taken


def sleep_to_next_reading():
    sleep_time = time_to_next_reading()
    print("Sleeping until " +
          str(time.gmtime(time.time() + int(sleep_time/1000))))
    print("Sleeping...")
    deepsleep(sleep_time, logger)


# Responds to an error through sleeping or halting execution
def handle_error():
    if (STOP_UPON_ERROR):
        sys.exit("Error encountered")
    else:
        sleep_to_next_reading()


def main():
    # Enables power to WiFi chip
    machine.Pin(23, machine.Pin.OUT).high()

    # If reset from anything other than deepsleep
    if (machine.reset_cause() != 3):
        blink(10)

    # If reset from deepsleep
    else:
        time.sleep(5)
        check_deepsleep(logger)

    # Connects to WiFi
    connect_to_wifi()
    if (NTP_SYNC):
        sync_time()

    # Initializes I2C
    i2c0_sda = Pin(8)
    i2c0_scl = Pin(9)
    i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

    # Initializes DHT20
    dht_initialized = False
    dht = None
    counter = 0
    print("Initializing DHT20")
    while not dht_initialized and counter < RETRY_LIMIT and HAS_DHT_SENSOR:
        try:
            dht = dht20.DHT20(0x38, i2c0)
        except:
            counter += 1
            if (counter < RETRY_LIMIT):
                print("Failed to initialize DHT20, retrying attempt " +
                      str(counter) + "...")
                time.sleep(2)
            else:
                print("Failed to initialize DHT20 (check wiring)")
                # logger.log_error("Failed to initialize DHT20 (check wiring)")

                # Continues to upload a reading of -999
                # to alert that this specific issue has occured
                # handle_error()
        else:
            dht_initialized = True
            print("DHT initialized")

    # Enable garbage collection
    gc.enable()
    print('garbage collection threshold: ' + str(gc.threshold()))

    # Load configuration for a file
    config = Config('main.conf', 'key.json')

    # Create an instance of ServiceAccount class
    # Which then is going to be used to obtain an OAuth2 token
    # For writing data to a sheet
    sa = ServiceAccount()
    sa.email(config.get('google_service_account_email'))
    sa.scope('https://www.googleapis.com/auth/spreadsheets')
    sa.private_rsa_key(config.private_rsa_key())

    # Create an instance of Spreadsheet which is used to write data to a sheet
    spreadsheet = Spreadsheet(logger, RETRY_LIMIT)
    spreadsheet.set_service_account(sa)
    spreadsheet.set_id(config.get('google_sheet_id'))
    spreadsheet.set_range(SENSOR_LOCATION + '!A:A')

    # Main loop
    print("")
    while True:

        # Takes temperature reading
        temperature = dht.measurements['t'] if dht_initialized else "DHT Disconnected"

        # Sends reading to spreadsheet
        spreadsheet.append_values([temperature])

        # Disconnects from WiFi
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)

        # Deep Sleeps
        sleep_to_next_reading()


try:
    main()
# Handles exceptions
except Exception as e:
    if (LOG_EXCEPTIONS):
        logger.log("Software error encountered. Traceback below:")
        with open(LOG_FILE_PATH, "a") as f:
            sys.print_exception(e, f)  # Writes to log file
            f.close()

    sys.print_exception(e)
    handle_error()
