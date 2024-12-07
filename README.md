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
1. 

For server.py:
1. To run, type "python server.py".
2. Input the IP address you want your server to connect to.
3. Input the port you want your serve to connect to.

For client.py:
1. To run, type "python client.py".
2. Input the IP of the server you wish to contact.
3. Input the port you want to contact the server through.
4. Input one of the three queries:
   1. What is the average moisture inside my kitchen fridge in the past three hours?
   2. What is the average water consumption per cycle in my smart dishwasher?
   3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?
5. After the server responds, type "y" to continue messaging the server or "n" to
end the program.
