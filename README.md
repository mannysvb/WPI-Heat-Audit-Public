# Creating A Network of Heat Sensors Using Google Sheets

A subgoal of this Interactive Qualifying Project (A partial fulfillment of a Bachelors of Science Degree from Worcester Polytechnic Institute) was to create and implement a method of automated heat tracking for Banksia Gardens Community Services. The final sensor design is centered around utilizing the WiFi-connected Raspberry Pi Pico W micro-controller, with an Adafruit DHT20 Temperature sensor module for temperature readings, and two rechargeable D batteries (recharged and replaced by volunteers every five weeks) to power it all. 

*It is worth mentioning that if the sensors were outside of the WiFi range, the use of radio transmission is a viable alternative. Transmitters would send data from the sensors to one central “Gateway”, which consisted of a radio receiver and a WiFi-connected Pico W board, that would then upload the data to our database using WiFi available in the main building. This idea was abonded as we realized a WiFi approach would meet the needs of our client just as well.*

For an extensive guide of creating and installing these devices, please refer to the instruction manual on our website: xxxxxxxxxxx.

Developed by Worcester Polytechnic Institute Students: 
Stephen Fanning (https://www.linkedin.com/in/stephen-fanning/) &
Emmanuel Vargas (http://linkedin.com/in/esvargas/)

# Requirements 

This repository relies on the use and creation of a Google Service Account for authentication. It is necessary to create a private key from the service account, and enable Google Sheets API as well as the Google Drive API. 

# Establishing a Private Key

Please note that this service key is sensitive information and should be kept private.

1. Go to https://console.cloud.google.com/projectselector2/iam-admin/settings 

2. Select Create Projects
<img width="1440" alt="Screenshot 2023-02-23 at 10 42 04 PM" src="https://user-images.githubusercontent.com/124530176/220896433-d7475506-ed2d-4886-89f8-58b4df13068c.png">
