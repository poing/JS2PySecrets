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

random = jsFunction('random')
share = jsFunction('share')
init = jsFunction('init')
getConfig = jsFunction('getConfig')
_reset = jsFunction('_reset')
setRNG = jsFunction('setRNG')
str2hex = jsFunction('str2hex')
hex2str = jsFunction('hex2str')
combine = jsFunction('combine')
