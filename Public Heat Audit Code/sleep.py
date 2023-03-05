import machine
import time
import logger

# The maximum time the pico will sleep for
# This is necessary because machine.deepsleep has a maximum duration
SLEEP_INCREMENT = 1000*60*60
SLEEP_LEFT_FILENAME = "sleep_left.txt"


def check_deepsleep(logger):
    sleep_left = 0

    with open(SLEEP_LEFT_FILENAME, "r") as f:
        sleep_left = int(f.readline())
        f.close()

    if (sleep_left > 0):
        deepsleep(sleep_left, logger)


def write_sleep_left(sleep_left, logger):
    with open(SLEEP_LEFT_FILENAME, "w") as f:
        f.write(str(sleep_left))
        f.close()


def deepsleep(sleep_ms, logger):

    sleep_for = 0  # the amount of time the machine deep sleeps before waking up

    if (sleep_ms > SLEEP_INCREMENT):  # More than sleep than can be done at once
        sleep_ms -= SLEEP_INCREMENT
        write_sleep_left(sleep_ms, logger)
        sleep_for = SLEEP_INCREMENT
    else:  # Sleep can be done at once
        write_sleep_left(0, logger)
        sleep_for = sleep_ms

    # Subtracts the 5 seconds taken to pause upon startup
    if (sleep_for >= 5000):
        sleep_for -= 5000

    # Disables power to WiFi chip, because for some reason deepsleep doesn't work properly otherwise
    machine.Pin("WL_GPIO1", machine.Pin.OUT).low()
    machine.Pin(23, machine.Pin.OUT).low()
    time.sleep(1)

    # Deep sleeps
    machine.deepsleep(sleep_for)
