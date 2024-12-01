from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://smart-home:ironwill@cluster0.1coyr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
cluster = MongoClient(CONNECTION_STRING)
db = cluster['test']
collection_meta = db['smart-table_metadata']
collection_data = db['smart-table_virtual']

pipeline = [
    {
        "$group": {
            "_id": "$payload.parent_asset_uid",
            "totNRG1": {"$sum": {"$toDouble": "$payload.Ammeter - Arnold"}},
            "totNRG2": {"$sum": {"$toDouble": "$payload.sensor 2 fb26ed6e-2bc2-4a83-8e7d-d4889f9b4d4e"}},
            "totNRG3": {"$sum": {"$toDouble": "$payload.Ammeter - Annie"}}
        }
    }
]

results = collection_data.aggregate(pipeline)

for result in results:
    print(result)