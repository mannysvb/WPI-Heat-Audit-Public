�   ()
    if(machine.reset_cause() != 3): # Reset from anything other than deepsleep
        blink(10)
        deepsleep(40*1000, logger)
    else: # Reset from deepsleep
        logger.log("Normal sleeping for 5000ms")
        time.sleep(5)
        check_deepsleep(logger)

    repeat_blink(3)

    # Connects to WiFi
    connect_to_wifi()
    if (NTP_SYNC):
        sync_time()

    i2c0_sda = Pin(8)
    i2c0_scl = Pin(9)
    i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)
    time.sleep(1)  # TODO check if necessary

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
                logger.log_error("Failed to initialize DHT20 (check wiring)")
        else:
            dht_initialized = True
            print("DHT initialized")

    # TODO figure out how to do this (either this way or another way):
    # the following function, when added to the google sheet (Tools > Script editor) allows the
    # formula uploaded in the "now" variable (see "measure(self)") to calculate a local timestamp
    # from the epoch value loaded in column A of the inserted row
    #
    # function TIMESTAMP_TO_DATE(value) {
    #   return new Date(value * 1000);
    # }
    # see the sheets.py file to set the ValueInputOption to USER_INPUT to avoid now string value being prefixed with a '

    # enable garbage collection
    gc.enable()
    print('garbage collection threshold: ' + str(gc.threshold()))

    # load configuration for a file
    config = Config('main.conf', 'key.json')

    # create an instance of ServiceAccount class
    # which then is going to be used to obtain an OAuth2 token
    # for writing data to a sheet
    sa = ServiceAccount()
    sa.email(config.get('google_service_account_email'))
    sa.scope('https://www.googleapis.com/auth/spreadsheets')
    sa.private_rsa_key(config.private_rsa_key())

    # create an instance of Spreadsheet which is used to write data to a sheet
    spreadsheet = Spreadsheet(logger)
    spreadsheet.set_service_account(sa)
    spreadsheet.set_id(config.get('google_sheet_id'))
    spreadsheet.set_range('TemperatureData!A:A')

    print("")
    # main loop
    while True:
        temperature = dht.measurements['t'] if HAS_DHT_SENSOR else -999
        spreadsheet.append_values([temperature])
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
        blink(3)
        sleep_time = time_to_next_reading()
        print("Sleeping until " +
              str(time.gmtime(time.time() + int(sleep_time/1000))))
        print("Sleeping...")
        deepsleep(sleep_time, logger)


main()
����������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������encoding="utf-8"
            ) as board_name_file:
                return board_name_file.read().strip()
        except FileNotFoundError:
            pass
        return None
