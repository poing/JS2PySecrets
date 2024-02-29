import json
from .wrapper import wrapper  # Import your wrapper function

class JsFunction:
    def __init__(self, func, test=False):
        self.func = func
        self.test = test

    def __call__(self, *args, test=False, **kwargs):
        def wrapped_func(*args, **kwargs):
            args_str = ', '.join(repr(arg) for arg in args)

            return f"{self.func.__name__}({args_str})"
            
        data = []
        
        # DO NOT REMOVE THIS
        if test or self.test:
        	data.append("setRNG('testRandom')")

        data.append(wrapped_func(*args, **kwargs) if args else self.func(*args, **kwargs))

        json_data = json.dumps(data, indent=None).replace("'", "`")
        commands = json_data.encode().hex()
        results = wrapper(commands)

        return results

    def __get__(self, instance, owner):
        return self if instance is None else types.MethodType(self, instance)

class jsNeedless:
	def __init__(self, func_name, test=False):
		self.func_name = func_name
		self.test = test
	def __call__(self, *args, **kwargs):
		raise Exception("Calling subsiquent JavaScript functions are not supported. -or- The JavaScript function isn't neccessary for the Python version.")


@JsFunction
def share(*args, **kwargs):
    pass 

@JsFunction
def random(*args, **kwargs):
    pass 

@JsFunction
def combine(*args, **kwargs):
    pass 
    
# # Core Functions from secrets.js
# init = jsFunction('init')
# combine = jsFunction('combine')
# getConfig = jsFunction('getConfig')
# extractShareComponents = jsFunction('extractShareComponents')
# setRNG = jsFunction('setRNG')
# str2hex = jsFunction('str2hex')
# hex2str = jsFunction('hex2str')
# random = jsFunction('random')
# share = jsFunction('share')
# newShare = jsFunction('newShare')
# 
# # Test Functions
# _reset = jsNeedless('_reset')
# _isSetRNG = jsFunction('_isSetRNG')

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



		


