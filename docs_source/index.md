# JS2PySecrets

!!! danger "Work in Progress"

	The Python implementation of Shamir's threshold secret sharing scheme
	is currently under development.  
	
	It doesn't work just yet, but it's progressing.

Python implementation of Shamir's Secret Sharing.

$\LARGE q(x) = a_0 + a_1x + \dotsi + a_{k-1}x^{k-1}$

!!! note ""

    The primary goal of this project is to create a Python implementation of Shamir's
    Secret Sharing that interoperates with an existing JavaScript implementation.
    
    
!!! example "Quick Comparison"

	Here's a quick overview of how Python will look, compared with the JavaScript implimentation.

	=== "Python"

		``` py
		import js2pysecrets as secrets
	
		key = "86A8E7"
	
		shares = secrets.share(key, 6, 3)
		
		recovered = secrets.combine(shares) # "86A8E7"
		```

	=== "JavaScript"

		``` js
		const secrets = require('secrets.js');
	
		var key = "86A8E7";
	
		var shares = secrets.share(key, 6, 3);
		
		var recovered = secrets.combine(shares); // "86A8E7"
		```