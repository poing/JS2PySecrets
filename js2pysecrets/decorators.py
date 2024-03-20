import types

from .wrapper import chain


class JsFunction:
    def __init__(self, func, test=False, list=False):
        self.func = func
        self.test = test
        self.list = list

    def __call__(self, *args, test=False, list=False, **kwargs):
        def wrapped_func(*args, **kwargs):
            if args:
                args_str = ", ".join(repr(arg) for arg in args)
                return f"{self.func.__name__}({args_str})"
            else:
                if self.list or list:
                    return f"{self.func.__name__}()"
                else:
                    return f"{self.func.__name__}()"

        if list or self.list:
            return wrapped_func(*args, **kwargs)
        else:
            data = []
            if test or self.test:
                data.append("setRNG('testRandom')")

            data.append(wrapped_func(*args, **kwargs))

            return get_last_element_or_string(chain(data))

    def __get__(self, instance, owner):
        return (
            self if instance is None else types.MethodType(self, instance)
        )  # pragma: no cover  No idea how to test!


def get_last_element_or_string(result):
    if isinstance(result, list):
        return result[-1]
    else:
        return str(result)


class jsNeedless:
    def __init__(self, func_name):
        self.func_name = func_name

    def __call__(self, *args, **kwargs):
        raise Exception(
            "Calling subsequent JavaScript functions are not supported. -or- "
            "The JavaScript function isn't necessary for the Python version."
        )
