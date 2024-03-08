import json
import types

from .wrapper import wrapper  # Import your wrapper function


class JsFunction:
    def __init__(self, func, test=False):
        self.func = func
        self.test = test

    def __call__(self, *args, test=False, **kwargs):
        def wrapped_func(*args, **kwargs):
            args_str = ", ".join(repr(arg) for arg in args)

            return f"{self.func.__name__}({args_str})"

        data = []

        # DO NOT REMOVE THIS
        if test or self.test:
            data.append("setRNG('testRandom')")

        data.append(
            wrapped_func(*args, **kwargs)
            if args
            else self.func(*args, **kwargs)
        )

        json_data = json.dumps(data, indent=None).replace("'", "`")
        commands = json_data.encode().hex()
        results = wrapper(commands)

        return results

    def __get__(self, instance, owner):
        return (
            self if instance is None else types.MethodType(self, instance)
        )  # pragma: no cover  No idea how to test!


class jsNeedless:
    def __init__(self, func_name, test=False):
        self.func_name = func_name
        self.test = test

    def __call__(self, *args, **kwargs):
        raise Exception(
            "Calling subsequent JavaScript functions are not supported. -or- "
            "The JavaScript function isn't necessary for the Python version."
        )
