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

*This one time process must be completed on a Windows computer, please see the following video for step by step instructions.*

[![Watch the video](<iframe width="966" height="543" src="https://www.youtube.com/embed/2WAjVtjPpWE" title="Key Tutorial" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>)


