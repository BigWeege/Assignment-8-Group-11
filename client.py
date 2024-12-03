import socket
maxBytesToReceive = 1024
#lines 5-11 and 26-40 taken from assigment 5
while True:
    try:
        serverIP = input("Insert the IP you wish to contact: ")
        serverPort = int(input("Insert the port you wish to connect to: "))
        try:
            myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            myTCPSocket.connect((serverIP, serverPort))
            
            while True:
                while True:
                    query = input("Your message here: ") #question being asked 
                    if query.upper() == "WHAT IS THE AVERAGE MOISTURE INSIDE MY KITCHEN FRIDGE IN THE PAST THREE HOURS?": #question bieng aksed doesnt have to be case sensitive for all queries
                        message = "1" #send 1 to the client
                        print("Query #1 recieved.")
                        break
                    elif query.upper() == "WHAT IS THE AVERAGE WATER CONSUMPTION PER CYCLE IN MY SMART DISHWASHER?":
                        message = "2" #send 2 to the client
                        print("Query #2 recieved.")
                        break
                    elif query.upper() == "WHICH DEVICE CONSUMED MORE ELECTRICITY AMONG MY THREE IOT DEVICES (TWO REFRIGERATORS AND A DISHWASHER)?":
                        message = "3" #send 2 to the client
                        print("Query #3 recieved.")
                        break
                    else:
                        #query did not match any of the questions and gives list of valid inputs
                        print("Sorry, this query cannot be processed. Please try one of the following:\n1. \"What is the average moisture inside my kitchen fridge in the past three hours?\"\n2. \"What is the average water consumption per cycle in my smart dishwasher?\"\n3. \"Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\"")
                myTCPSocket.send(bytearray(str(message), encoding='utf-8'))
                serverResponse = myTCPSocket.recv(maxBytesToReceive)
                print(f"The server responded: \"{serverResponse.decode('utf-8')}\"")
                wantsMore = input("Do you wish to continue? (y/n): ")
                if wantsMore == 'n':
                    break
                elif wantsMore != 'y':
                    print("I'll take that as a \"no\"!")
                    break
            myTCPSocket.close()
            break
        except socket.error:
            print("ERROR: Unable to connect to server. Please check your IP address and port number and try again.")
    except:
        print("ERROR: Invalid IP address or port number. Please check your IP address and port number and try again.")
