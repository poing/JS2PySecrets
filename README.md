[![CI](https://github.com/poing/JS2PySecrets/actions/workflows/main.yml/badge.svg)](https://github.com/poing/JS2PySecrets/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/poing/JS2PySecrets/branch/main/graph/badge.svg?token=JS2PySecrets_token_here)](https://codecov.io/gh/poing/JS2PySecrets)
[![PyPI version](https://badge.fury.io/py/js2pysecrets.svg)](https://badge.fury.io/py/js2pysecrets)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![JS2PySecrets Documentation](https://img.shields.io/badge/Documentation-white?labelColor=3F00FF&logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c3ZnIGlkPSJiIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNDEuNTUgMTUwLjUiPjxnIGlkPSJjIj48cGF0aCBkPSJNOTEuMy4yNWw1OC4yOC4wOGM2LjQ3LDAsMTEuNzIsNS4yNiwxMS43MiwxMS43M2gwYzAsNS4zLTIuMTEsMTAuMzktNS44NiwxNC4xNGwtMy41LDMuNWMtNi4wMyw2LjAzLTYuNDYsMTUuNjYtMS4wMSwyMi4yMWgwYzgsOS42LDIyLjczLDkuNiwzMC43MywwaDBjNS40Ni02LjU1LDUuMDItMTYuMTgtMS4wMS0yMi4yMWwtMy41LTMuNWMtMy43NS0zLjc1LTUuODYtOC44NC01Ljg2LTE0LjE0aDBjMC02LjQ3LDUuMjQtMTEuNzIsMTEuNzItMTEuNzNsNTguMjgtLjA4YzAsODIuMjktNjcuNzEsMTUwLTE1MCwxNTAtMjYuMzMsMC01Mi4yLTYuOTMtNzUtMjAuMWwyOS4xNy01MC41MmMzLjI0LTUuNiwxLjMyLTEyLjc3LTQuMjktMTZoMGMtNC41OS0yLjY1LTEwLjA1LTMuMzctMTUuMTgtMmwtNC43OCwxLjI4Yy04LjIzLDIuMjEtMTYuNzktMi4yMy0xOS43My0xMC4yM2gwYy00LjMxLTExLjcyLDMuMDYtMjQuNDgsMTUuMzYtMjYuNjFoMGM4LjQtMS40NSwxNi41MiwzLjc0LDE4LjczLDExLjk4bDEuMjgsNC43OGMxLjM3LDUuMTIsNC43Miw5LjQ5LDkuMzIsMTIuMTRoMGM1LjYsMy4yNCwxMi43NywxLjMyLDE2LTQuMjlMOTEuMy4yNVoiIHN0eWxlPSJmaWxsOiNmZmZmZmY7ICIvPjwvZz48L3N2Zz4=)](https://poing.github.io/JS2PySecrets/)

# About

`js2pysecrets` is a port of the [`secrets.js-grempe`](https://github.com/grempe/secrets.js) JavaScript package to Python. 

This package allows for cross-platform compatible shares, *generated using [Shamir's Secret Sharing](http://en.wikipedia.org/wiki/Shamir's_Secret_Sharing)*, to seamlessly interoperate between JavaScript and Python.

Function names and arguments used in the JavaScript package have been maintained for consistency and maintainability. 

The functionality is essentially the same as the JavaScript package, with an exception around random number generation.  Python doesn't have to adapt to different environments for random number generation like the JavaScript does.

*For additional details, see the [documentation](https://poing.github.io/JS2PySecrets/).*


## Installation and Usage

Install the PyPI package:

```
pip install js2pysecrets
```

Import the library:

```
import js2pysecrets as secrets
```

### Examples

Divide a 512-bit key, expressed in hexadecimal form, into 10 shares, requiring that any 5 of them are necessary to reconstruct the original key:

```python
import js2pysecrets as secrets

# generate a 512-bit key
key = secrets.random(512) 
print(key) # => key is a hex string

# split into 10 shares with a threshold of 5
shares = secrets.share(key, 10, 5)
print(shares) # => ['801xxx...xxx','802xxx...xxx', ... ,'809xxx...xxx','80axxx...xxx']

# combine 4 shares
comb = secrets.combine(shares[:4])
print(comb == key) # => False

# combine 5 shares
comb = secrets.combine(shares[:5])
print(comb == key) # => True

# combine ALL shares
comb = secrets.combine(shares)
print(comb == key) # => True

# create another share with id 8
new_share = secrets.newShare(8, shares)
print(new_share) # => '808xxx...xxx'

# reconstruct using 4 original shares and the new share:
comb = secrets.combine(shares[:4] + [new_share])
print(comb == key) # => True
```

Divide a password containing a mix of numbers, letters, and other characters, requiring that any 3 shares must be present to reconstruct the original password:

```python
import js2pysecrets as secrets

pw = "<<PassWord123>>"

# convert the text into a hex string
pwHex = secrets.str2hex(pw)
print(pwHex) # => hex string

# split into 5 shares, with a threshold of 3
shares = secrets.share(pwHex, 5, 3)
print(shares) # => ['801xxx...xxx','802xxx...xxx', ... ,'804xxx...xxx','805xxx...xxx']

# combine 2 shares:
comb = secrets.combine(shares[:2])

# convert back to UTF string:
comb = secrets.hex2str(comb)
print(comb == pw) # => False

# combine 3 shares:
comb = secrets.combine([shares[1], shares[3], shares[4]])

# convert back to UTF string:
comb = secrets.hex2str(comb)
print(comb == pw) # => True
```

## License

`js2pysecrets` is released under the MIT License. See the `LICENSE` file.

## Development and Testing

Read the [CONTRIBUTING.md](https://github.com/poing/JS2PySecrets/blob/main/CONTRIBUTING.md) file.

## To Do

- Restructure and split into separate modules
    - Move the backend functions outside the main module 
- Restructure and clean-up the tests

## Changelog

- 0.0.x

  - Documentation, documentation, documentation...
  - Configured automatic release to PyPI 
  - Converted `secrets.js`[^1] to Python
  - Disabled the `tests_win` GitHub action, #24
  - Moved docs to use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
  - Converted `secrets.js-grempe` Jasmine tests to `pytest` versions
  - Added package.json as a stub
  - Built Node.js wrapper for testing
  - Enable CodeCov
  - Started with the [Python Project Template](https://github.com/rochacbruno/python-project-template)
  
[^1]: `secrets.js-grempe` and `secrets.js` are basically the same.  The difference is the execution environment, JavaScript or Node.js.