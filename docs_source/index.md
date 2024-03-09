# JS2PySecrets

$\LARGE q(x) = a_0 + a_1x + \dotsi + a_{k-1}x^{k-1}$

This is a `Python` implementation of [Shamir's Secret Sharing](http://en.wikipedia.org/wiki/Shamir's_Secret_Sharing).  

based **and compatible with** the `JavaScript` fork of `secrets.js` [*maintained by `grempe`*](https://github.com/grempe/secrets.js).  Which is orginally based on the code created by `amper5and` on Github. The [original secrets.js can be found there](https://github.com/amper5and/secrets.js/).

!!! danger "Work in Progress"

	The Python implementation of Shamir's threshold secret sharing scheme
	is currently under development.  
	
	It doesn't work just yet, but it's progressing.
	
	

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

* `mkdocs -h` - Print help message and exit.

* [mkdocs-material](https://squidfunk.github.io/mkdocs-material/reference/)


## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.



!!! warning "Phasellus posuere in sem ut cursus"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.
    
``` py title="bubble_sort.py" 
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```    