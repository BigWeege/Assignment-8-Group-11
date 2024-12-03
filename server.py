import socket
import time
from pymongo import MongoClient
numberOfBytes = 1024

CONNECTION_STRING = "mongodb+srv://smart-home:ironwill@cluster0.1coyr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cluster = MongoClient(CONNECTION_STRING)
db = cluster['test']
collection_meta = db['smart-table_metadata']
collection_data = db['smart-table_virtual']

while True:
    try:
        serverIP = input("Insert the server's IP address: ")
        serverPort = int(input("Insert the port you wish to connect to: "))
        try:
            myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            myTCPSocket.bind((serverIP, serverPort))
            myTCPSocket.listen(5)
            incomingSocket, incomingAddress = myTCPSocket.accept()
            while True:
                try:
                    myData = incomingSocket.recv(numberOfBytes)
                    if not myData:
                        break
                    if myData.decode("utf-8") == "1":
                        print("Query #1 received.")
                        pipeline = [
                            {
                                "$lookup": {
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$match": {
                                    "metaloc.customAttributes.additionalMetadata.location": "kitchen",
                                    "metaloc.customAttributes.name": {"$regex": "Fridge"},
                                    "payload.timestamp": {"$lt": str(time.time()), "$gt": str(time.time() - 10800)}
                                }
                            },
                            {
                                "$group": {
                                    "_id": "$payload.parent_asset_uid",
                                    "avgMoisture": {"$avg": {"$toDouble": "$payload.Moisture Meter - Mike"}}
                                }
                            }
                        ]
                        results = collection_data.aggregate(pipeline)

                        for result in results:
                            someData = f"The average moisture inside your kitchen fridge in the past three hours is: {round(result["avgMoisture"], 2)}%."
                    elif myData.decode("utf-8") == "2":
                        print("Query #2 received.")
                        pipeline = [
                            {
                                "$lookup": {
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$match": {
                                    "metaloc.customAttributes.name": {"$regex": "Dishwasher"}
                                }
                            },
                            {
                                "$group": {
                                    "_id": "$payload.parent_asset_uid",
                                    "avgWaterConsumption": {
                                        "$avg": {"$toDouble": "$payload.Water Consumption Sensor - Walter"}}
                                }
                            }
                        ]
                        results = collection_data.aggregate(pipeline)

                        for result in results:
                            someData = f"The average water consumption per cycle in your smart dishwasher is: {round(result["avgWaterConsumption"], 2)} gallons."
                    elif myData.decode("utf-8") == "3":
                        print("Query #3 received.")
                        pipeline = [
                            {
                                "$lookup": {
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$addFields": {
                                    "name": "$metaloc.customAttributes.name"
                                }
                            },
                            {
                                "$unwind": {
                                    "path": "$name"
                                }
                            },
                            {
                                "$group": {
                                    "_id": "$name",
                                    "totNRG1": {"$sum": {"$toDouble": "$payload.Ammeter - Arnold"}},
                                    "totNRG2": {"$sum": {"$toDouble": "$payload.sensor 2 fb26ed6e-2bc2-4a83-8e7d-d4889f9b4d4e"}},
                                    "totNRG3": {"$sum": {"$toDouble": "$payload.Ammeter - Annie"}}
                                }
                            },
                            {
                                "$addFields": {
                                    "totNRG": {"$add": [{"$toDouble": "$totNRG1"}, {"$toDouble": "$totNRG2"}, {"$toDouble": "$totNRG3"}]}
                                }
                            },
                            {
                                "$sort": {
                                    "totNRG": -1
                                }
                            },
                            {
                                "$limit": 1
                            }
                        ]
                        results = collection_data.aggregate(pipeline)

                        for result in results:
                            someData = f"The device that consumed the most electricity was the {result["_id"]}."
                        
                        someData = myData.decode('utf-8')
                    incomingSocket.send(bytearray(str(someData), encoding='utf-8'))
                except:
                    incomingSocket.close()
                    break
            break
        except socket.error:
            print("ERROR: Unable to connect to server. Please check your IP address and port number and try again.")
    except:
        print("ERROR: Invalid IP address or port number. Please check your IP address and port number and try again.")
