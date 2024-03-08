# import json

from .decorators import JsFunction, jsNeedless

# from .wrapper import wrapper  # Import your wrapper function

NAME = "js2pysecrets"


@JsFunction
def share(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def random(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def foobar(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def getConfig(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def combine(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def init(*args, **kwargs):
    pass  # pragma: no cover


@jsNeedless
def _reset(*args, **kwargs):
    pass  # pragma: no cover


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
