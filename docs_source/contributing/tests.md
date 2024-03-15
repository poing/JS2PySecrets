# Running the JavaScript Commands

Since the primary goal of this project is to create a Python implementation of Shamir's Secret Sharing that can interoperates with a JavaScript implementation.  This package needs to run the JavaScript commands.

While there are a variety of Python libraries to execute JavaScript, they had limitations.  Some translate JavaScript into Python.  For others, using `require()` was a challange.  In the end, this package uses a wrapper to make function calls directly to Node.js.

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

There is a drawback to this approach, each call to Node.js invokes a new process.  It easily handles single functions, but another approach is needed to handle subsequent calls. 


!!! warning "The Python Wrapper"

	The Python wrapper __does not__ operate like Javascript, calls are not sequential.

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



!!! success "Chaining a Series"

	The Python wrapper __does not__ operate like Javascript, calls are not sequential.

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


!!! tip "Using `testRandom` _without_ `chain()`"

	Since a large percentage of tests only require `testRandom` to be run before the command under test, 

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



	