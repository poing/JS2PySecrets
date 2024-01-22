# js2pysecrets

[![codecov](https://codecov.io/gh/poing/JS2PySecrets/branch/main/graph/badge.svg?token=JS2PySecrets_token_here)](https://codecov.io/gh/poing/JS2PySecrets)
[![CI](https://github.com/poing/JS2PySecrets/actions/workflows/main.yml/badge.svg)](https://github.com/poing/JS2PySecrets/actions/workflows/main.yml)


This is a `Python` implementation of [Shamir's threshold secret sharing scheme](http://en.wikipedia.org/wiki/Shamir's_Secret_Sharing), based **and compatible with** the `JavaScript` fork of `secrets.js` [*maintained by `grempe`*](https://github.com/grempe/secrets.js).  Which is orginally based on the code created by `amper5and` on Github. The [original secrets.js can be found there](https://github.com/amper5and/secrets.js/).

## Status

The project is intended to create a `Python` version that is compatible with `secrets.js`.  It's currently in the **DEVELOPMENT** stage and the framework is being built to *effectively* test and run the `JavaScript` from within the `Python` environment.

All of the `JavaScript` functions can be called from *within* the `Python` environment.  However, **there are limitations**!  Most notably, you can **ONLY** call a single function, so some of the utility provided by the `JavaScript` version is not available.  *In many cases, isn't even necessary*.

Combing of shares is not working *yet*...

### Requirements

**`Node`** is **required**.  

To use this project in it's current state **and for testing**, `Node` is required on the system.  `Node` is always required for testing.  It's used to run the `JavaScript` in the local environment.

## JavaScript Wrapper

The `JavaScript` wrapper **is not** intended to allow subsequent commands.  It spawns an *indvidual* `subprocess` of `Node` for each function called.

```python
import js2pysecrets

js2pysecrets.setRNG('testRandom')
js2pysecrets.share('FFFF', 6, 3) # This will NOT use 'testRandom'
```

While the `Javascript` *does* have code to allow subsequent commands, the only **INTENDED** use is to force the use of `testRandom` for testing purposes.  This can be accomplished by over-riding the function with the kew-word argument `test=True`.

```python
from js2pysecrets import jsFunction

random = jsFunction('random', test=True)
random(32) # Output '075bcd15'
random(32) # Output '075bcd15'
random(32) # Output '075bcd15'
```



## Examples

Divide a 512-bit key, expressed in hexadecimal form, into 10 shares, requiring that any 5 of them are necessary to reconstruct the original key:

**Not everything is working yet...**

```python
import json
import js2pysecrets

# generate a 512-bit key
# key = js2pysecrets.random(512) // => key is a hex string
key = js2pysecrets.random(512)
print(key)

# split into 10 shares with a threshold of 5
# shares = js2pysecrets.share(key, 10, 5)
#  => shares = ['801xxx...xxx','802xxx...xxx','803xxx...xxx','804xxx...xxx','805xxx...xxx']
shares = js2pysecrets.share(key, 10, 5)
print(shares)

# // combine 4 shares
# var comb = secrets.combine(shares.slice(0, 4))
# console.log(comb === key) // => false
#
# // combine 5 shares
# comb = secrets.combine(shares.slice(4, 9))
# console.log(comb === key) // => true
# 
# // combine ALL shares
# comb = secrets.combine(shares)
# console.log(comb === key) // => true
# 
# // create another share with id 8
# var newShare = secrets.newShare(8, shares) // => newShare = '808xxx...xxx'
# 
# // reconstruct using 4 original shares and the new share:
# comb = secrets.combine(shares.slice(1, 5).concat(newShare))
# console.log(comb === key) // => true
```

Divide a password containing a mix of numbers, letters, and other characters, requiring that any 3 shares must be present to reconstruct the original password:

**Things really start to break here...**  
*Big and reversed endianness for the `JS` str2hex*   

```python
import json
import js2pysecrets

# var pw = "<<PassWord123>>"
pw = "<<PassWord123>>"
 
# convert the text into a hex string
# jsHex = secrets.str2hex(pw) // => hex string
jsHex = js2pysecrets.str2hex(pw)
print(jsHex)

# Notice how the JS uses an unconventional str2hex method
pyHex = pw.encode('utf-16').hex().lstrip('fe') # Stripped off the BOM
print(pyHex)

# // split into 5 shares, with a threshold of 3
# var shares = secrets.share(pwHex, 5, 3)
# 
# // combine 2 shares:
# var comb = secrets.combine(shares.slice(1, 3))
# 
# //convert back to UTF string:
# comb = secrets.hex2str(comb)
# console.log(comb === pw) // => false
# 
# // combine 3 shares:
# comb = secrets.combine([shares[1], shares[3], shares[4]])
# 
# //convert back to UTF string:
# comb = secrets.hex2str(comb)
# console.log(comb === pw) // => true
```

## Install it from PyPI

```bash
pip install js2pysecrets
```

## Usage

```py
from js2pysecrets import BaseClass
from js2pysecrets import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m js2pysecrets
#or
$ js2pysecrets
```

## Development and Testing

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.


<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->
----
# Python Project Template

A low dependency and really simple to start project template for Python Projects.

See also 
- [Flask-Project-Template](https://github.com/rochacbruno/flask-project-template/) for a full feature Flask project including database, API, admin interface, etc.
- [FastAPI-Project-Template](https://github.com/rochacbruno/fastapi-project-template/) The base to start an openapi project featuring: SQLModel, Typer, FastAPI, JWT Token Auth, Interactive Shell, Management Commands.

### HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/rochacbruno/python-project-template/generate)** feature.

1. Click on **[Use this template](https://github.com/rochacbruno/python-project-template/generate)**
3. Give a name to your project  
   (e.g. `my_awesome_project` recommendation is to use all lowercase and underscores separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. If you want [codecov](https://about.codecov.io/sign-up/) Reports and Automatic Release to [PyPI](https://pypi.org)  
  On the new repository `settings->secrets` add your `PYPI_API_TOKEN` and `CODECOV_TOKEN` (get the tokens on respective websites)
4. Read the file [CONTRIBUTING.md](CONTRIBUTING.md)
5. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🖼️ Templates for starting multiple application types:
  * **Basic low dependency** Python program (default) [use this template](https://github.com/rochacbruno/python-project-template/generate)
  * **Flask** with database, admin interface, restapi and authentication [use this template](https://github.com/rochacbruno/flask-project-template/generate).
  **or Run `make init` after cloning to generate a new project based on a template.**
- 📦 A basic [setup.py](setup.py) file to provide installation, packaging and distribution for your project.  
  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.
- 🤖 A [Makefile](Makefile) with the most useful commands to install, test, lint, format and release your project.
- 📃 Documentation structure using [mkdocs](http://www.mkdocs.org)
- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.
- 🐋 A simple [Containerfile](Containerfile) to build a container image for your project.  
  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.
- 🧪 Testing structure using [pytest](https://docs.pytest.org/en/latest/)
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- 📊 Code coverage reports using [codecov](https://about.codecov.io/sign-up/)
- 🛳️ Automatic release to [PyPI](https://pypi.org) using [twine](https://twine.readthedocs.io/en/latest/) and github actions.
- 🎯 Entry points to execute your program using `python -m <js2pysecrets>` or `$ js2pysecrets` with basic CLI argument parsing.
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to lint, test and release your project on Linux, Mac and Windows environments.

> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md](ABOUT_THIS_TEMPLATE.md)  
> If you want to contribute to this template please open an [issue](https://github.com/rochacbruno/python-project-template/issues) or fork and send a PULL REQUEST.

[❤️ Sponsor this project](https://github.com/sponsors/rochacbruno/)

