import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1 (jsonObject):
  jsonObject = jsonData1
  location_split = jsonObject["location"].split('/')
  jsonObject["location"] = {"country" : location_split[0], "city" : location_split[1], "area" : location_split [2], "factory" : location_split[3], "section"  : location_split[4]}
  jsonObject["data"] = {"status" : jsonObject["operationStatus"], "temperature" : jsonObject["temp"]}
  jsonObject.pop("operationStatus")
  jsonObject.pop("temp")
  return jsonObject

#the returned jsonObject dictionary items are the same as data-result.json, not sure why it's still returning an assertion error
def convertFromFormat2 (jsonObject):
  jsonObject = jsonData2
  jsonObject["deviceID"] = jsonObject["device"]["id"]
  jsonObject["deviceType"] = jsonObject["device"]["type"]
  import datetime
  time = jsonObject["timestamp"]
  date = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
  timestamp = str((date - datetime.datetime(1970, 1,  1)).total_seconds()*1000)
  jsonObject["timestamp"] = int(timestamp[:-2])
  import itertools
  location_dict = dict(itertools.islice(jsonObject.items(), 3,7))
  jsonObject["location"] = location_dict
  pop_list = ["device", "country", "city", "area", "factory", "section"]
  for i in pop_list:
    jsonObject.pop(i)
  data_dict = jsonObject.pop("data")
  jsonObject["data"] = data_dict
  return jsonObject


def main (jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):

        result = main (jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):

        result = main (jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__':
    unittest.main()
