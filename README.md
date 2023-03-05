# Creating A Network of Heat Sensors Using Google Sheets

A subgoal of this Interactive Qualifying Project (A partial fulfillment of a Bachelors of Science Degree from Worcester Polytechnic Institute) was to create and implement a method of automated heat tracking for Banksia Gardens Community Services. The final sensor design is centered around utilizing the WiFi-connected Raspberry Pi Pico W micro-controller, with an Adafruit DHT20 Temperature sensor module for temperature readings, and two rechargeable D batteries (recharged and replaced by volunteers every five weeks) to power it all. 

*It is worth mentioning that if the sensors were outside of the WiFi range, the use of radio transmission is a viable alternative. Transmitters would send data from the sensors to one central “Gateway”, which consisted of a radio receiver and a WiFi-connected Pico W board, that would then upload the data to our database using WiFi available in the main building. This idea was abonded as we realized a WiFi approach would meet the needs of our client just as well.*

For an extensive guide of creating and installing these devices, please refer to the instruction manual on our website: xxxxxxxxxxx. If you have any questions feel free to reach out at esvargas@wpi.edu or sefanning@wpi.edu.

Developed by Worcester Polytechnic Institute Students: 
[Stephen Fanning](https://www.linkedin.com/in/stephen-fanning/) &
[Emmanuel Vargas](http://linkedin.com/in/esvargas/)

# Requirements 

This repository relies on the use and creation of a Google Service Account for authentication. It is necessary to create a private key from the service account, and enable Google Sheets API as well as the Google Drive API. 

# Establishing a Private Key

Please note that this service key is sensitive information and should be kept private.

1. Go to [Google Cloud Console](https://console.cloud.google.com/projectselector2/iam-admin/settings)

2. Select Create Projects
<img width="1440" alt="Screenshot 2023-02-23 at 10 42 04 PM" src="https://user-images.githubusercontent.com/124530176/220896433-d7475506-ed2d-4886-89f8-58b4df13068c.png">

3. Create a Project Name
<img width="1439" alt="Screenshot 2023-02-23 at 10 47 48 PM" src="https://user-images.githubusercontent.com/124530176/220898128-c9b0dff0-70df-4769-9c93-2c0112f02a96.png">

4. Navigate to Service Accounts and Create Service Account
<img width="1440" alt="Screenshot 2023-02-23 at 10 54 21 PM" src="https://user-images.githubusercontent.com/124530176/220898993-c3227220-3bcd-41e1-8320-f4df4726001b.png">

5. Fill in the Service Account Name, the ID will automatically be filled in.
<img width="582" alt="Screenshot 2023-02-23 at 11 07 05 PM" src="https://user-images.githubusercontent.com/124530176/220903297-9b188294-4b68-4a1d-a0b1-83998a8a5441.png">

6. Select the "Owner" role and click Done
<img width="599" alt="Screenshot 2023-02-23 at 11 18 39 PM" src="https://user-images.githubusercontent.com/124530176/220903978-4996608d-aa69-4f55-bb97-1556499f6c30.png">

7. Select the Service Account
<img width="1439" alt="Screenshot 2023-02-24 at 2 47 30 PM" src="https://user-images.githubusercontent.com/124530176/221087331-a4f45b9f-0ffd-4e60-be65-29c75506bc5f.png">

8. Navigate to the Keys tab, and Create a New Key
<img width="1437" alt="Screenshot 2023-02-24 at 2 49 14 PM" src="https://user-images.githubusercontent.com/124530176/221087561-d0df916e-f568-4f17-8e17-2e984a9dc08a.png">

9. Create a "JSON" Private Key
<img width="1439" alt="Screenshot 2023-02-24 at 2 51 27 PM" src="https://user-images.githubusercontent.com/124530176/221088279-bd6b390f-c341-4ada-b9a6-8c6ecbb5eb4d.png">

10. This key will be saved to your downloads folder
<img width="1440" alt="Screenshot 2023-02-24 at 2 57 04 PM" src="https://user-images.githubusercontent.com/124530176/221088686-8e0670ff-a2e6-4927-bb2d-7edcdd031d0f.png">

# Converting Your Private Key

*This one time process must be completed on a Windows computer, please see the following video for step by step instructions. The description includes links to download the various programs.*

[![IMAGE ALT TEXT](http://img.youtube.com/vi/2WAjVtjPpWE/0.jpg)](http://www.youtube.com/watch?v=2WAjVtjPpWE "Key Tutorial")

Make sure to drop the key.json file into the "Public Heat Audit Code" folder

# Heat Audit Tutorial
*This guide is specifically tailored to Banksia Gardens Community Services, but all steps can still be followed by other organizations.*

[![IMAGE ALT TEXT](http://img.youtube.com/vi/NXjj1oKcEbQ/0.jpg)](http://www.youtube.com/watch?v=NXjj1oKcEbQ "Heat Audit Tutorial")

# Databases
*There are two databases, the first collects all recordings from the seven sensors, and the second pulls filtered data points to create an organized chart.

<u>The following is a picture of the first database: Raw Heat Sensor Temperature Data</u>

<img width="1440" alt="Screenshot 2023-03-05 at 10 23 18 AM" src="https://user-images.githubusercontent.com/124530176/222983928-506da472-32dc-480f-8454-1151f85dcaad.png">

Cell A1 & A2 are user inputed headers

Column D runs on a script that formats Column A when any edits are made in the sheet

Cell G1 is a user inputed header

Cell G2 filters Column D with the following command: =FILTER(A:B, REGEXMATCH(D:D,":00:|:01:|:02:|:03:|:04:"))

Column J & K runs on a script that removes duplicates

*Please see the folder Google Apps Script for the code to copy on your own Raw Heat Sensor Temperatre Data Google Sheet*

<u>The following is a picture of the second database: Biodiversity and Temperature Database</u>

<img width="1437" alt="Screenshot 2023-03-05 at 10 25 42 AM" src="https://user-images.githubusercontent.com/124530176/222984041-6b013e83-dca4-4ed5-87fe-b170e1c458f3.png">

Cells A1:H1 are user inputed headers

Cells A2:A runs on a script that adds the hour every hour

Cells B2:H2 uses the =IMPORTRANGE formula by inputting the link and defined range.

  *Please see the folder Google Apps Script for the code to copy on your own Biodiversity and Temperature Database Google Sheet. It is worth noting that this formula only consistently works when using defined ranges as shown in the following picture*
  
<img width="1439" alt="Screenshot 2023-03-05 at 10 29 32 AM" src="https://user-images.githubusercontent.com/124530176/222984698-942b93d6-3d12-407f-b259-38a7be4db1a4.png">

