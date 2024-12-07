import socket
import time
import re
from pymongo import MongoClient
numberOfBytes = 1024

CONNECTION_STRING = "mongodb+srv://smart-home:ironwill@cluster0.1coyr.mongodb.net/"
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
                                "$lookup": { #connecting the virtual data to the metadata database 
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$match": { #filters location, device name and timestamp
                                    "metaloc.customAttributes.additionalMetadata.location": "kitchen",
                                    "metaloc.customAttributes.name": {"$regex": "Fridge"},
                                    "payload.timestamp": {"$lt": str(time.time()), "$gt": str(time.time() - 10800)}
                                }
                            },
                            {
                                "$project": { #singles out the device's moisture reading as long as it contains the substring "Moisture Meter"
                                    "moisture": {
                                        "$filter": {
                                            "input": {
                                                "$objectToArray": "$payload"
                                            },
                                            "as": "payload_filter",
                                            "cond": {
                                                "$regexMatch": {"input": "$$payload_filter.k", "regex": re.compile(r"^Moisture Meter")}
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "$unwind": {
                                    "path": "$moisture"
                                }
                            },
                            {
                                "$group": { #finds avg moisture
                                    "_id": "$moisture.k",
                                    "avgMoisture": {"$avg": {"$toDouble": "$moisture.v"}}
                                }
                            }
                        ]
                        results = collection_data.aggregate(pipeline) #runs list on collection data

                        for result in results:
                            someData = f"The average moisture inside your kitchen fridge in the past three hours is: {round(result["avgMoisture"], 2)}%."
                    elif myData.decode("utf-8") == "2":
                        print("Query #2 received.")
                        pipeline = [
                            {
                                "$lookup": { #connecting the virtual data to the metadata database 
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$match": { #checks for dishwasher
                                    "metaloc.customAttributes.name": {"$regex": "Dishwasher"}
                                }
                            },
                            {
                                "$project": { # singles out the device's water consumption reading as long as it contains the substring "Water Consumption Sensor"
                                    "water_consumption": {
                                        "$filter": {
                                            "input": {
                                                "$objectToArray": "$payload"
                                            },
                                            "as": "payload_filter",
                                            "cond": {
                                                "$regexMatch": {"input": "$$payload_filter.k",
                                                                "regex": re.compile(r"^Water Consumption Sensor")}
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "$unwind": {
                                    "path": "$water_consumption"
                                }
                            },
                            {
                                "$group": { #avg water consumption
                                    "_id": "$water_consumption.k",
                                    "avgWaterConsumption": {
                                        "$avg": {"$toDouble": "$water_consumption.v"}}
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
                                "$lookup": { #connecting the virtual data to the metadata database 
                                    "from": "smart-table_metadata",
                                    "localField": "payload.parent_asset_uid",
                                    "foreignField": "assetUid",
                                    "as": "metaloc"
                                }
                            },
                            {
                                "$project": { # singles out the device's current reading as long as it contains the substring "Ammeter"
                                    "current": {
                                        "$filter": {
                                            "input": {
                                                "$objectToArray": "$payload"
                                            },
                                            "as": "payload_filter",
                                            "cond": {
                                                "$regexMatch": {"input": "$$payload_filter.k",
                                                                "regex": re.compile(r"^Ammeter")}
                                            }
                                        }
                                    },
                                    "name": "$metaloc.customAttributes.name"
                                }
                            },
                            {
                                "$unwind": {
                                    "path": "$current"
                                }
                            },
                            {
                                "$unwind": { #gives individual names instead of a list
                                    "path": "$name"
                                }
                            },
                            {
                                "$group": { # sums ammeter readings
                                    "_id": "$name",
                                    "totCurrent": {"$sum": {"$toDouble": "$current.v"}}
                                }
                            },
                            {
                                "$sort": { #compares and orders devices based on energy consumption(greatest to least)
                                    "totCurrent": -1
                                }
                            },
                            {
                                "$limit": 1 #give the most 
                            }
                        ]
                        results = collection_data.aggregate(pipeline)

                        for result in results:
                            someData = f"The device that consumed the most electricity was the {result["_id"]}."
                    incomingSocket.send(bytearray(str(someData), encoding='utf-8'))
                except:
                    incomingSocket.close()
                    break
            break
        except socket.error:
            print("ERROR: Unable to connect to server. Please check your IP address and port number and try again.")
    except:
        print("ERROR: Invalid IP address or port number. Please check your IP address and port number and try again.")
