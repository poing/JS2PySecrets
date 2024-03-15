# JS2PySecrets

!!! danger "Work in Progress"

	The Python implementation of Shamir's Secret Sharing is currently under development.  
	
	It doesn't work just yet, but it's progressing.

Python implementation of Shamir's Secret Sharing.

$q(x) = a_0 + a_1x + \dotsi + a_{k-1}x^{k-1}$

!!! note ""

    The primary goal of this project is to create a Python implementation of Shamir's
    Secret Sharing that interoperates with an existing JavaScript implementation.

<!--
/// html | inline



            <div class="row">
                <div class="col-sm-6">
                    <h2>Split</h2>
                    <div>
                        Require
                        <input class="required form-control" type="number" value="3" min="2" max="255">
                        parts from
                        <input class="total form-control" type="number" value="5" min="2" max="255">
                        to reconstruct the following secret
                    </div>
                    <textarea class="secret form-control" rows=10 placeholder="Enter your secret here"></textarea>
                    <h2>Usage</h2>
                    <p>Double click each part below to select the content for that part. Copy and paste the content for each part into <span class="distributesize">5</span> individual files on your computer.</p>
                    <p>Distribute one file to each person in your group.</p>
                    <p>If <span class="recreatesize">3</span> of those people can combine the contents of their file using this page, they can view the secret.</p>
                    <p>Remember to delete the parts from your computer once you're finished. If you use a rubbish bin for deleted files, also remove them from the rubbish bin.</p>
                    <p class="error text-danger"></p>
                    <h2>Parts</h2>
                    <ol class="generated">
                        <li>Enter your secret above.</li>
                    </ol>
                </div></div>

///
-->
  
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
		
