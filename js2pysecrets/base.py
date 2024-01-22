import json
from .wrapper import wrapper  # Import your wrapper function

class jsFunction:
    def __init__(self, func_name, test=False):
        self.func_name = func_name
        self.test = test

    def __call__(self, *args, **kwargs):
        result = {
            'function': self.func_name,
            'args': args
        }

        setup = []  # Keep the setup list
        if self.test:
            setup = [{'function': 'setRNG', 'args': ['testRandom']}]

        main = {'function': self.func_name, 'args': args}
        tasks = {'tasks': [{'setup': setup, 'start': main}]}
        json_data = json.dumps(tasks, indent=None)
        data = wrapper(json_data)
        
        return data


class jsNeedless:
	def __init__(self, func_name, test=False):
		self.func_name = func_name
		self.test = test
	def __call__(self, *args, **kwargs):
		raise Exception("Calling subsiquent JavaScript functions are not supported. -or- The JavaScript function isn't neccessary for the Python version.")


# Core Functions from secrets.js
init = jsFunction('init')
combine = jsFunction('combine')
getConfig = jsFunction('getConfig')
extractShareComponents = jsFunction('extractShareComponents')
setRNG = jsNeedless('setRNG')
str2hex = jsFunction('str2hex')
hex2str = jsFunction('hex2str')
random = jsFunction('random')
share = jsFunction('share')
newShare = jsFunction('newShare')

# Test Functions
_reset = jsNeedless('_reset')
_isSetRNG = jsFunction('_isSetRNG')

#         /* test-code */
#         // export private functions so they can be unit tested directly.
#         _reset: reset,
#         _padLeft: padLeft,
#         _hex2bin: hex2bin,
#         _bin2hex: bin2hex,
#         _hasCryptoGetRandomValues: hasCryptoGetRandomValues,
#         _hasCryptoRandomBytes: hasCryptoRandomBytes,
#         _getRNG: getRNG,
#         _isSetRNG: isSetRNG,
#         _splitNumStringToIntArray: splitNumStringToIntArray,
#         _horner: horner,
#         _lagrange: lagrange,
#         _getShares: getShares,
#         _constructPublicShareString: constructPublicShareString
#         /* end-test-code */



		


