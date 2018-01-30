#!/usr/bin/python
import json,sys
SEARCH_KEY_NAME = "quantity" #name of the field that required to change
JSON_FILE = "data.json"


def decode_dump(dumpFile):
    with open(dumpFile) as json_file:
        return json.load(json_file)

def traverse_dict(dict_obj,value):
	"This function will traverse all items of the JSON object and replace the value of quantity with the passing value"
	for key in dict_obj.keys():
		if isinstance(key, dict):
			traverse_dict(key, value)
		elif isinstance(key, list):
			for item in key:
				if isinstance(item, dict):
					traverse_dict(item, value)
				elif isinstance(item, list):
					for i in item:
						if isinstance(i, dict):
							traverse_dict(i, value)
						elif isinstance(i, str) and i == SEARCH_KEY_NAME:
							dict_obj[i] = value
				elif isinstance(item, str) and item == SEARCH_KEY_NAME:
					dict_obj[key] = value
		elif key == SEARCH_KEY_NAME: #here we can pass other fields which needto change
			dict_obj[key] = value

		key_obj = dict_obj[key]

		if isinstance(key_obj, dict):
			traverse_dict(key_obj,value)
		elif isinstance(key_obj, list):
			for item1 in key_obj:
				if isinstance(item1, dict):
					traverse_dict(item1, value)
				elif isinstance(item1,list):
					for i1 in item1:
						if isinstance(i1, dict):
							traverse_dict(i1,value)
		elif(key_obj == SEARCH_KEY_NAME):
			dict_obj[key_obj] = value

	return None

if __name__ == "__main__":

	value = 23
	try:
		value = int(sys.argv[1])
	except:
		print'No Value passed. So default value %s will be used.'%(value)
		pass
	json_dict = decode_dump(JSON_FILE)
	result = traverse_dict(json_dict['data']['100gm'], value)
	outFileName = 'newData.json'
	outFile = open(outFileName,'w')
	outFile.write(json.dumps(json_dict))
	outFile.close()
	print"JSON file %s created"%(outFileName)