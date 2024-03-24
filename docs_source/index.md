# JS2PySecrets

$q(x) = a_0 + a_1x + \dotsi + a_{k-1}x^{k-1}$

A port of the [`secrets.js`](https://github.com/grempe/secrets.js) JavaScript package to Python. 

This package allows for cross-platform compatible shares, *generated using [Shamir's Secret Sharing](http://en.wikipedia.org/wiki/Shamir's_Secret_Sharing)*, to seamlessly interoperate between JavaScript and Python.

Function names and arguments used in the JavaScript package have been maintained for consistency and maintainability. 

The functionality is essentially the same as the JavaScript package, with an exception around random number generation.  Python doesn't have to adapt to different environments for random number generation like the JavaScript does.

!!! example "Quick Comparison"

	Here's a quick overview of how Python will look, compared with the JavaScript implimentation.

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


!!! tip "Random Number Generator"

	This package handles random number generation different that the JavaScript package.  This difference affects:
	
	- `init()`
	- `setRNG()`
	- `getConfig()`
	
	

	!!! warning "Random Data CAN Be Captured"

		Capturing the random data used to generate shares is possible.  It's __not__ enabled by default and the `function()` necessary to process the random data is at the discretion users of this package.  
	
		The ability to access the random data is __solely__ intended for random dithering _(like the images below)_.
	
	=== "secrets"
		![Image title](images/secrets.png){ align=left }

		The `secrets` module is used for generating cryptographically strong random numbers suitable for managing data such as passwords, account authentication, security tokens, and related secrets.

		The `secrets` module __should be used__ instead of the default pseudo-random number generator in the `random` module, which is designed for modelling and simulation, not security or cryptography.

	=== "random"
		![Image title](images/random.png){ align=left }
		



		!!! warning "Warning"

			The pseudo-random generators in the `random` module __should not__ be used for security purposes. For security or cryptographic uses, use the `secrets` module. 		

	=== "testRandom"
		![Image title](images/testRandom.png){ align=left }

		!!! danger "Do Not Use"

			__For testing purposes only!__
			
			The `testRandom` function serves as useful tool for development, generating predictable values. However, when it comes to applications involving security or cryptography, it's crucial to employ a robust random number generator. 
		
