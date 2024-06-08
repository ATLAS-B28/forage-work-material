import json
import unittest
from datetime import datetime


with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)

def convertFromFormat1(jsonObject):
    merged_data = {}

    # Merge deviceID and deviceType
    merged_data["deviceID"] = jsonObject.get("deviceID", data1["device"]["id"])
    merged_data["deviceType"] = jsonObject.get("deviceType", data1["device"]["type"])

    # Merge timestamp
    merged_data["timestamp"] = jsonObject.get("timestamp")

    # Merge location information
    location = {
        "country": jsonObject.get("country"),
        "city": jsonObject.get("city"),
        "area": jsonObject.get("area"),
        "factory": jsonObject.get("factory"),
        "section": jsonObject.get("section")
    }
    merged_data["location"] = location

    # Merge data information
    data = {
        "status": jsonObject.get("operationStatus"),
        "temperature": jsonObject.get("temp")
    }
    merged_data["data"] = data

    return merged_data

def convertFromFormat2(jsonObject):
    merged_data = {}

    # Merge deviceID and deviceType
    merged_data["deviceID"] = jsonObject["device"]["id"]
    merged_data["deviceType"] = jsonObject["device"]["type"]

    # Convert timestamp to datetime object
    timestamp_str = jsonObject["timestamp"]
    try:
        timestamp_datetime = datetime.fromisoformat(timestamp_str[:-1])  # Try ISO 8601 format
    except ValueError:
        # If not ISO 8601 format, parse using another format
        timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        timestamp_datetime = datetime.strptime(timestamp_str, timestamp_format)
    
    # Convert datetime object to Unix timestamp (epoch time)
    timestamp_unix = int(timestamp_datetime.timestamp())
    merged_data["timestamp"] = timestamp_unix

    # Merge location information
    location = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }
    merged_data["location"] = location

    # Merge data information
    data = {
        "status": jsonObject["data"]["status"],
        "temperature": jsonObject["data"]["temperature"]
    }
    merged_data["data"] = data

    return merged_data

def main(jsonObject):
    result = {}

    if jsonObject.get('device') is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result

'''jsonData1 = {
    "deviceID": "dh28dslkja",
    "deviceType": "LaserCutter",
    "timestamp": 1624445837783,
    "operationStatus": "healthy",
    "temp": 22
}

jsonData2 = {
    "device": {
        "id": "dh28dslkja",
        "type": "LaserCutter"
    },
    "timestamp": "2021-06-23T10:57:17.783Z",
    "country": "japan",
    "city": "tokyo",
    "area": "keiyō-industrial-zone",
    "factory": "daikibo-factory-meiyo",
    "section": "section-1",
    "data": {
        "status": "healthy",
        "temperature": 22
    }
}

jsonExpectedResult = {
    "deviceID": "dh28dslkja",
    "deviceType": "LaserCutter",
    "timestamp": 1624445837783,
    "location": {
        "country": "japan",
        "city": "tokyo",
        "area": "keiyō-industrial-zone",
        "factory": "daikibo-factory-meiyo",
        "section": "section-1"
    },
    "data": {
        "status": "healthy",
        "temperature": 22
    }
}'''

class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
