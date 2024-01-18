import json
from .wrapper import wrapper

def init(bits=None, rngType=None):
	setup = [{'function': 'init', 'args': [bits]}]
	main = {'function': None, 'args': []}
	tasks = {'tasks': [{'start': main}]}
	json_data = json.dumps(tasks, indent=None)
	data = wrapper(json_data)
	return data

def getConfig():
	setup = []
	main = {'function': 'getConfig', 'args': []}
	tasks = {'tasks': [{'setup': setup, 'start': main}]}
	json_data = json.dumps(tasks, indent=None)
	data = wrapper(json_data)
	return data

def share(secret, numShares, threshold, padLength=128):
	setup = [
		{'function': 'setRNG', 'args': ['testRandom']},
		{'function': 'init', 'args': []},
	]
	main = {'function': 'share', 'args': [secret, numShares, threshold, padLength]}
	tasks = {'tasks': [{'setup': setup, 'start': main}]}
	json_data = json.dumps(tasks, indent=None)
	data = wrapper(json_data)
	return data


	