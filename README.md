# Assignment-8-Group-11

For MongoDB:
1. Create a free M0 Shared cluster with Google Cloud as your provider.
2. On the left panel in your dashboard, select Database Access under the Security tab.
   1. Create a new Database User.
   2. Select the Password authentication method and create a password.
   3. Click "Add Built In Role" under Database User Privileges and select "Atlas admin".
   4. Click "Add User"
3. On the left panel in your dashboard, select Network Access under the Security tab.
   1. Press "Add IP Address".
   2. Add the IP 0.0.0.0/0.
4. On the left panel in your dashboard, select Clusters under the Database tab.
   1. Select "Connect" on your database.
   2. Select "Connect your application".
   3. Select Python for your driver and choose version 3.6 or later.
   4. Copy the URL it gives you
   5. Change the <username> and <password> fields in the URL to be the username and password you created earlier.

For Dataniz:
1. On the left panel in your dashboard, select Profile & Settings.
   1. Click "Generate New MQTT Key".
   2. Copy the generated key.
2. Create a Source.
   1. Create a name for the source.
   2. Select the Dataniz Source URL source type.
   3. Paste your generated MQTT Key as the MQTT Key.
3. Create a Destination.
   1. Create a name for the database.
   2. Select MongoDB as the Database Type.
   3. Paste the Connection URL you got from creating your MongoDB database.
   4. Name the table "smart-table".
4. Create a Link.
   1. Create a name for the link.
   2. Select the source you created.
   3. Select the destination you created.
   4. Create a name for the connection topic.
5. Create your first device (Kitchen Fridge).
   1. Name the device "Kitchen Fridge".
   2. Choose an Arduino Pro Mini as the board.
   3. Create a Moisture Meter.
      1. Name the sensor whatever you want, as long as it contains the substring "Moisture Meter".
      2. Make the desired range between 30 and 50% relative humidity.
   4. Create a custom sensor called an "Ammeter".
      1. Select the Current Sensor sensor use.
      2. Name the sensor whatever you want, as long as it contains the substring "Ammeter".
      3. Make the sensor range between 0 and 20 amps.
      4. Make the desired range between 10 and 12.5 amps.
   5. Create a custom sensor called an "Thermistor".
      1. Select the Temperature Sensor sensor use.
      2. Name the sensor whatever you want, as long as it contains the substring "Thermistor".
      3. Make the sensor range between -100 and 100 degrees Celsius.
      4. Make the desired range between -10 and 4 degreees Celsius.
   6. Create metadata.
      1. Give the device a latitude and longitude of your choice.
      2. Create custom metadata with the key name "location" and the value name "kitchen".
6. Create your second device (Bedroom Fridge).
   1. Duplicate the Kitchen Fridge device.
   2. Rename the device to "Bedroom Fridge".
   3. Rename the Moisture Meter to something that contains the substring "Moisture Meter".
   4. Rename the Ammeter to something that contains the substring "Ammeter".
   5. Rename the Thermistor to something that contains the substring "Thermistor".
   6. Create metadata.
      1. Give the device a latitude and longitude of your choice.
      2. Create custom metadata with the key name "location" and the value name "bedroom".
7. Create your third device (Dishwasher).
   1. Name the device "Dishwasher".
   2. Choose an Arduino Pro Mini as the board.
   3. Create a custom sensor called a "Water Consumption Sensor".
      1. Select the Water Flow Sensor sensor use.
      2. Name the sensor whatever you want, as long as it contains the substring "Water Consumption Sensor".
      3. Make the sensor range between 0 and 99 gallons per cycle.
      4. Make the desired range between 10 and 12.5 amps.
   4. Create a custom sensor called an "Ammeter".
      1. Select the Current Sensor sensor use.
      2. Name the sensor whatever you want, as long as it contains the substring "Ammeter".
      3. Make the sensor range between 0 and 20 amps.
      4. Make the desired range between 10 and 12.5 amps. 
   5. Create metadata.
      1. Give the device a latitude and longitude of your choice.
      2. Create custom metadata with the key name "location" and the value name "kitchen".
8. Generate data.
   1. Click "Generate & View".
   2. Turn each device on.
   3. Each device's sensors should generate data every minute.

For server.py:
1. To run, type "python server.py".
2. Input the IP address you want your server to connect to.
3. Input the port you want your serve to connect to.

For client.py:
1. In the python code, replace the variable named "CONNECTION STRING" to the Connection URL you got from creating your MongoDB database.
2. To run, type "python client.py".
3. Input the IP of the server you wish to contact.
4. Input the port you want to contact the server through.
5. Input one of the three queries:
   1. What is the average moisture inside my kitchen fridge in the past three hours?
   2. What is the average water consumption per cycle in my smart dishwasher?
   3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
6. After the server responds, type "y" to continue messaging the server or "n" to
end the program.
