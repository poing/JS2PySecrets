# JS2PySecrets

$q(x) = a_0 + a_1x + \dotsi + a_{k-1}x^{k-1}$

A port of the [`secrets.js`](https://github.com/grempe/secrets.js) JavaScript package to Python. 

This package allows for cross-platform compatible shares, *generated using [Shamir's Secret Sharing](http://en.wikipedia.org/wiki/Shamir's_Secret_Sharing)*, to seamlessly interoperate between JavaScript and Python.

Function names and arguments used in the JavaScript package have been maintained for consistency and maintainability. 

The functionality is essentially the same as the JavaScript package, with an exception around random number generation.  Python doesn't have to adapt to different environments for random number generation like the JavaScript does.

!!! info "Quick Comparison"

	Here's a quick overview of the Python use, compared with the JavaScript use.

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

!!! example "Examples"

	=== " :fontawesome-brands-python: Divide a Hex Key"

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

	=== " :fontawesome-brands-python: Divide a Password"

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





