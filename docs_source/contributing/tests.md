## Ready for Testing

All of the JavaScript functions of the `secrets.js-grempe` JavaScript package are accessable through the Node.js wrapper.  _more details on this page_

!!! success "Running Tests"

	Simple test of `str2hex()`.  Comparing output of the Python version to the output of the JavaScript version.

	=== " :fontawesome-brands-python: Python"
	


		``` py
		import js2pysecrets.base as secrets # The Python Version
		import js2pysecrets.node as node # JavaScript using the Node.js wrapper
		import pytest

		def test_str2hex_ASCII():
			# Set the test string
			test_string = "foobar"

			# Perform conversion using the str2hex function in Python
			py_hex = secrets.str2hex(test_string)

			# Perform conversion using the str2hex function in JavaScript
			js_hex = node.str2hex(test_string)

			# Confirm the Python and JavaScript outputs match
			assert py_hex == js_hex
		```

# Configuration

All of the settings are stored using a `dataclass`.  Allowing for the default values to be maintained, while allowing settings to modified too.  

## ==Settings()==

=== " :fontawesome-brands-python: Accessing Settings"
	``` py
	from js2pysecrets.settings import Settings
	
	# Initilize Settings
	settings = Settings()
	
	# Accessing bits Variables
	print(settings.bits) # 8
	```
### ==update_defaults()==

=== " :fontawesome-brands-python: Change a Setting"
	``` py
	from js2pysecrets.settings import Settings
	
	# Initilize Settings
	settings = Settings()

	# Accessing bits Variables
	print(settings.bits) # 8

	# Update bits Variables
	settings.update_defaults(bits=16)
	print(settings.bits) # 16	

	# Empty Update - Reverts all settings to default
	settings.update_defaults()
	print(settings.bits) # 8	
	```

### ==reset_defaults()==

=== " :fontawesome-brands-python: Revert to Defaults"
	``` py
	from js2pysecrets.settings import Settings
	
	# Initilize Settings
	settings = Settings()

	# Accessing bits Variables
	print(settings.bits) # 8

	# Update bits Variables
	settings.update_defaults(bits=16)
	print(settings.bits) # 16	

	# Empty Update - Reverts all settings to default
	settings.reset_defaults()
	print(settings.bits) # 8	
	```

### ==get_defaults()==

=== " :fontawesome-brands-python: Get the Default Values"
	``` py
	from js2pysecrets.settings import Settings
	
	# Initilize Settings
	settings = Settings()

	# Accessing bits Variables
	print(settings.bits) # 8

	# Update bits Variables
	settings.update_defaults(bits=16)
	print(settings.bits) # 16	

	# Get the default values
	settings.get_defaults()
	defaults = settings.get_defaults()
	
	# Updated variables ARE NOT changed
	print(settings.bits) # 16

	# New variable contains all the defaults
	print(defaults.bits) # 8	
	```

### ==get_config()==

Returns a subset of the settings.  _Used by `getConfig()`_

=== " :fontawesome-brands-python: get_config()"
	``` py
	from js2pysecrets.settings import Settings
	
	# Initilize Settings
	settings = Settings()
	config = settings.get_config()
	print(config) 
	"""
	Config(
		bits=8, 
		radix=16, 
		maxShares=255, 
		hasCSPRNG=False, 
		typeCSPRNG=None
	)
	"""
	```



## Running the JavaScript Commands

Since the primary goal of this project is to create a Python implementation of Shamir's Secret Sharing that can interoperates with a JavaScript implementation.  This package needs to run the JavaScript commands.

While there are a variety of Python libraries to execute JavaScript, they had limitations.  Some translate JavaScript into Python.  For others, using `require()` was a challange.  In the end, this package uses a wrapper to make function calls directly to Node.js.

## Node.js Wrapper

The Node.js wrapper allows tests to be run against the JavaScript version from Python.

??? danger "Warning - The JavaScript wrapper uses the `eval()` function.	 "
	JavaScript's eval() function is a powerful tool that can execute code stored as a string. However, it also poses a security risk when used improperly. Here are a few reasons why eval() is considered insecure:

	- Code injection: When eval() is passed untrusted data (such as user input), it can be used to inject malicious code into a program. Attackers can exploit this vulnerability to steal sensitive information, compromise data, or take control of the affected system.

	- Scope pollution: eval() has global scope, meaning that any variables or functions declared within the evaluated code are accessible from anywhere in the program. This can lead to naming collisions and unexpected behavior, as well as making it harder to understand and maintain the code.

	- Performance impact: eval() is significantly slower than other JavaScript operations since it requires the JavaScript engine to parse and executes the string of code at runtime. This can result in slower performance and degraded user experience, especially in large or complex applications.

	- Debugging difficulties: When bugs or errors occur within code executed by eval(), they can be difficult to diagnose and fix due to the dynamic nature of the function. This can make it challenging for developers to find and fix problems in their code.




``` { .yaml .no-copy } 
|-- javascript
|   `-- wrapper.js
|-- js2pysecrets
|   |-- decorators.py
|   |-- node.py
|   `-- wrapper.py
|-- package.json
```

!!! example "Using the Node.js wrapper"

	=== " :fontawesome-brands-python: Python"

		``` py
		import js2pysecrets.node as secrets
		
		secrets.share("aabb", 6, 3)
		```

## Complications with the wrapper

There is a drawback to using the wrapper, each call to Node.js invokes a new process.  It easily handles single functions, but another approach is needed to handle subsequent calls. 


!!! warning "The Python Wrapper"

	The Python wrapper __does not__ operate like Javascript, calls are not sequential.
	
	As you can see in Python example, using `setRNG('testRandom')` is not persistant.  
	
	Calling `random()` after `setRNG()` __will not__ use the defined RNG.  
	
	_While in Node.js, `setRNG()` is persistant and all subsequent calls to `random()` uses the RNG defined._

	=== " :fontawesome-brands-python: Python"

		``` py
		import js2pysecrets.node as secrets

		# Enable fixed pattern for simulated random number generation (RNG)
		secrets.setRNG('testRandom') # True

		# Outputs should all be the same, but are not
		secrets.random(8) # 'fc'
		secrets.random(8) # 'c0'
		secrets.random(8) # 'a9'
		secrets.random(8) # '27'
		```

	=== " :fontawesome-brands-node-js: Node.js"

		``` js
		const secrets = require('../node_modules/secrets.js-grempe/secrets.js');

		// Enable fixed pattern for simulated random number generation (RNG)
		secrets.setRNG('testRandom') // True
		
		// Outputs should all be the same
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		```

### Subsequent Commands

The wrapper and calling the JavaScript was built to _either_ execute the command in Node.js __or__ output the command as a string to build a list of commands.

This is accomplished by setting the `list` keyword in the command to `True`

=== " :fontawesome-brands-python: Python"

	``` py
	some_func('aaa', 1, 2, 3) # Executes the command in Node.js
	some_func('aaa', 1, 2, 3, list=True) # String: "some_func('aaa', 1, 2, 3)"
	```



!!! success "Chaining a Series"

	After building a series of commands, run them _in order_ on Node.js by passing the list to `chain()`

	Output for each command can be accessed using the corresponding element returned by `chain()`.
	
	=== " :fontawesome-brands-python: Python"

		``` py
		import js2pysecrets.node as secrets
		from js2pysecrets.wrapper import chain

		# Commands run in sequence need to use chain
		series = []
		
		# Enable fixed pattern for simulated random number generation (RNG)
		series.append(secrets.setRNG('testRandom', list=True)) # results[0]: True

		# Outputs should all be the same
		series.append(secrets.random(8, list=True)) # results[1]: '15'
		series.append(secrets.random(8, list=True)) # results[2]: '15'
		series.append(secrets.random(8, list=True)) # results[3]: '15'
		series.append(secrets.random(8, list=True)) # results[4]: '15'
		
		results = chain(series)
		```

	=== " :fontawesome-brands-node-js: Node.js"

		``` js
		const secrets = require('../node_modules/secrets.js-grempe/secrets.js');

		// Enable fixed pattern for simulated random number generation (RNG)
		secrets.setRNG('testRandom') // True
		
		// Outputs should all be the same
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		```
	_Now we can see the Python and Node.js function in similar ways._

### testRandom

Generating repeatable non-random test bits can be __important__ for cryptographic testing.

The wrapper includes the ability to call `setRNG('testRandom')` before indvidual commands _without_ the need of building a list.  _Without the need to use `chain()`._

This is accomplished by setting the `test` keyword in the command to `True`


!!! tip "Using `testRandom` _without_ `chain()`"

	Indvidual commands can use `setRNG('testRandom')` without passing a list to `chain()`.

	=== " :fontawesome-brands-python: Python"

		``` py
		import js2pysecrets.node as secrets
		
		# Use test keyword to enable fixed pattern for simulated random number generation (RNG)
		
		# Outputs should all be the same
		secrets.random(8, test=True) # '15'
		secrets.random(8, test=True) # '15'
		secrets.random(8, test=True) # '15'
		secrets.random(8, test=True) # '15'
		```

	=== " :fontawesome-brands-node-js: Node.js"

		``` js
		const secrets = require('../node_modules/secrets.js-grempe/secrets.js');

		// Enable fixed pattern for simulated random number generation (RNG)
		secrets.setRNG('testRandom') // True
		
		// Outputs should all be the same
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		secrets.random(8) // '15'
		```


	