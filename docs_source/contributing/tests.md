# Running the JavaScript Commands

Since the primary goal of this project is to create a Python implementation of Shamir's Secret Sharing that can interoperates with a JavaScript implementation.  This package needs to run the JavaScript commands.

While there are a variety of Python libraries to execute JavaScript, they had limitations.  Some translate JavaScript into Python.  For others, using `require()` was a challange.  In the end, this package uses a wrapper to make function calls directly to NodeJS.

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

The only drawback to this approach, is each call to NodeJS invokes a new process.  It easily handles single functions.  But another approach is needed for subsequent calls. 


!!! warning "The Python Wrapper"

	The Python wrapper __does not__ operate like Javascript   calls are not sequential.

	=== " :fontawesome-brands-python: Python"

		``` py
		import js2pysecrets as secrets
	
		key = "86A8E7"
	
		shares = secrets.share(key, 6, 3)
		
		recovered = secrets.combine(shares) # '86a8e7'
		```

	=== " :fontawesome-brands-square-js: JavaScript"

		``` js
		const secrets = require('secrets.js');
	
		var key = "86A8E7";
	
		var shares = secrets.share(key, 6, 3);
		
		var recovered = secrets.combine(shares); // "86a8e7"
		```




	