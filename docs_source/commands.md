- secrets.share()
- secrets.combine()
- secrets.newShare()
- secrets.init()
- secrets.getConfig()
- secrets.extractShareComponents()
- secrets.setRNG()
- secrets.random()
- secrets.str2hex()
- secrets.hex2str()

### secrets.share( secret, numShares, threshold, [padLength] )

Divide a `secret` expressed in hexadecimal form into `numShares` number of shares, requiring that `threshold` number of shares be present for reconstructing the `secret`;

- `secret`: String, required: A hexadecimal string.
- `numShares`: Number, required: The number of shares to compute. This must be an integer between 2 and 2^bits-1 (see `secrets.init()` below for explanation of `bits`).
- `threshold`: Number, required: The number of shares required to reconstruct the secret. This must be an integer between 2 and 2^bits-1 (see `secrets.init()` below for explanation of `bits`).
- `padLength`: Number, optional, default `128`: How much to zero-pad the binary representation of `secret`. This ensures a minimum length for each share. See "Note on security" below.

The output of `secrets.share()` is an Array of length `numShares`. Each item in the array is a String. See `Share format` below for information on the format.

### secrets.combine( shares )

Reconstructs a secret from `shares`.

- `shares`: Array, required: An Array of shares. The form is equivalent to the output from `secrets.share()`.

The output of `secrets.combine()` is a String representing the reconstructed secret. Note that this function will ALWAYS produce an output String. However, if the number of `shares` that are provided is not the `threshold` number of shares, the output _will not_ be the original `secret`. In order to guarantee that the original secret is reconstructed, the correct `threshold` number of shares must be provided.

Note that using _more_ than the `threshold` number of shares will also result in an accurate reconstruction of the secret. However, using more shares adds to computation time.

### secrets.newShare( id, shares )

Create a new share from the input shares.

- `id`: Number or String, required: A Number representing the share id. The id is an integer between 1 and 2^bits-1. It can be entered as a Number or a number String expressed in hexadecimal form.
- `shares`: Array, required: The array of shares (in the same format as outputted from `secrets.share()`) that can be used to reconstruct the original `secret`.

The output of `secrets.newShare()` is a String. This is the same format for the share that `secrets.share()` outputs. Note that this function ALWAYS produces an output String. However, as for `secrets.combine()`, if the number of `shares` that are entered is not the `threshold` number of shares, the output share _will not_ be a valid share (i.e. _will not_ be useful in reconstructing the original secret). In order to guarantee that the share is valid, the correct `threshold` number of shares must be provided.

### secrets.init( [bits, rngType] )

Set the number of bits to use for finite field arithmetic.

- `bits`: Number, optional, default `8`: An integer between 3 and 20. The number of bits to use for the Galois field.
- `rngType`: String, optional: A string that has one of the values `["nodeCryptoRandomBytes", "browserCryptoGetRandomValues"]`. Setting this will try to override the RNG that would be selected normally based on feature detection. Warning: You can specify a RNG that won't actually _work_ in your environment.

Internally, secrets.js uses finite field arithmetic in binary Galois Fields of size 2^bits. Multiplication is implemented by the means of log and exponential tables. Before any arithmetic is performed, the log and exp tables are pre-computed. Each table contains 2^bits entries.

`bits` is the limiting factor on `numShares` and `threshold`. The maximum number of shares possible for a particular `bits` is (2^bits)-1 (the zeroth share cannot be used as it is the `secret` by definition.). By default, secrets.js uses 8 bits, for a total 2^8-1 = 255 possible number of shares. To compute more shares, a larger field must be used. To compute the number of bits you will need for your `numShares` or `threshold`, compute the log-base2 of (`numShares`+1) and round up, i.e. in JavaScript: `Math.ceil(Math.log(numShares+1)/Math.LN2)`. You can examine the current calculated `maxShares` value by calling `secrets.getConfig()` and increase the bits accordingly for the number of shares you need to generate.

Note:

- You can call `secrets.init()` anytime to reset _all_ internal state and re-initialize.
- `secrets.init()` does NOT need to be called if you plan on using the default of 8 bits. It is automatically called on loading the library.
- The size of the exp and log tables depends on `bits` (each has 2^bits entries). Therefore, using a large number of bits will cause a slightly longer delay to compute the tables.
- The _theoretical_ maximum number of bits is 31, as JavaScript performs bitwise operations on 31-bit numbers. A limit of 20 bits has been hard-coded into secrets.js, which can produce 1,048,575 shares. secrets.js has not been tested with this many shares, and it is not advisable to go this high, as it may be too slow to be of any practical use.
- The Galois Field may be re-initialized to a new setting when `secrets.newShare()` or `secrets.combine()` are called with shares that are from a different Galois Field than the currently initialized one. For this reason, use `secrets.getConfig()` to check what the current `bits` setting is.

### secrets.getConfig()

Returns an Object with the current configuration. Has the following properties:

- `bits`: [Number] The number of bits used for the current initialized finite field
- `radix`: [Number] The current radix (Default: 16)
- `maxShares`: [Number] The max shares that can be created with the current `bits`. Computed as `Math.pow(2, config.bits) - 1`
- `hasCSPRNG`: [Boolean] Indicates whether or not a Cryptographically Secure Pseudo Random Number Generator has been found and initialized.
- - `typeCSPRNG`: [String] Indicates which random number generator function has been selected based on either environment feature detection (the default) or by manually specifying the RNG type using `secrets.init()` or `secrets.setRNG()`. The current possible types that can be displayed here are ["nodeCryptoRandomBytes", "browserCryptoGetRandomValues"].

### secrets.extractShareComponents( share )

Returns an Object with the extracted parts of a public share string passed as an argument. Has the following properties:

- `bits`: [Number] The number of bits configured when the share was created.
- `id`: [Number] The ID number associated with the share when created.
- `data`: [String] A hex string of the actual share data.

### secrets.setRNG( function(bits){} | rngType )

Set the pseudo-random number generator used to compute shares.

secrets.js uses a PRNG in the `secrets.share()` and `secrets.random()` functions. By default, it tries to use a cryptographically strong PRNG. In Node.js this is `crypto.randomBytes()`. In browsers that support it, it is `crypto.getRandomValues()` (using typed arrays, which must be supported too).

To supply your own PRNG, use `secrets.setRNG()`. It expects a Function of the form `function(bits){}`. It should compute a random integer between 1 and 2^bits-1. The output must be a String of length `bits` containing random 1's and 0's (cannot be ALL 0's). When `secrets.setRNG()` is called, it tries to check the PRNG to make sure it complies with some of these demands, but obviously it's not possible to run through all possible outputs. So make sure that it works correctly.

- `rngType`: String, optional: A string that has one of the values `["nodeCryptoRandomBytes", "browserCryptoGetRandomValues"]`. Setting this will try to override the RNG that would be selected normally based on feature detection. Warning: You can specify a RNG that won't actually _work_ in your environment.

### secrets.random( bits )

Generate a random `bits` length string, and output it in hexadecimal format. `bits` must be an integer greater than 1.

### secrets.str2hex( str, [bytesPerChar] )

Convert a UTF string `str` into a hexadecimal string, using `bytesPerChar` bytes (octets) for each character.

- `str`: String, required: A UTF string.
- `bytesPerChar`: Number, optional, default `2`. The maximum `bytesPerChar` is 6 to ensure that each character is represented by a number that is below JavaScript's 2^53 maximum for integers.

### secrets.hex2str( str, [bytesPerChar] )

Convert a hexadecimal string into a UTF string. Each character of the output string is represented by `bytesPerChar` bytes in the String `str`. See note on `bytesPerChar` under `secrets.str2hex()` above.

## Share Format

Each share is a string in the format `<bits><id><value>`. Each part of the string is described below:

- `bits`: The first character, expressed in Base36 format, is the number of bits used for the Galois Field. This number must be between 3 and 20, expressed by the characters [3-9, a-k] in Base36.
- `id`: The id of the share. This is a number between 1 and 2^bits-1, expressed in hexadecimal form. The number of characters used to represent the id is the character-length of the representation of the maximum id (2^bits-1) in hexadecimal: `(Math.pow(2,bits)-1).toString(16).length`.
- `data`: The value of the share, expressed in hexadecimal form. The length of this string depends on the length of the secret.

You can extract these attributes from a share in your possession with the `secrets.extractShareComponents(share)` function which will return an Object with these attributes. You may use these values, for example, to call `secrets.init()` with the proper bits setting for shares you want to combine.

## Note on Security

Shamir's secret sharing scheme is "information-theoretically secure" and "perfectly secure" in that less than the requisite number of shares provide no information about the secret (i.e. knowing less than the requisite number of shares is the same as knowing none of the shares). However, because the size of each share is the same as the size of the secret (when using binary Galois fields, as secrets.js does), in practice it does leak _some_ information, namely the _size_ of the secret. Therefore, if you will be using secrets.js to share _short_ password strings (which can be brute-forced much more easily than longer ones), it would be wise to zero-pad them so that the shares do not leak information about the size of the secret. With this in mind, secrets.js will zero-pad in multiples of 128 bits by default which slightly increases the share size for small secrets in the name of added security. You can increase or decrease this padding manually by passing the `padLength` argument to `secrets.share()`.

When `secrets.share()` is called with a `padLength`, the `secret` is zero-padded so that it's length is a multiple of the padLength. The second example above can be modified to use 1024-bit zero-padding, producing longer shares:

=== " :fontawesome-brands-python: Produce Longer Shares"

	```python
	import js2pysecrets as secrets
	
	pw = "<<PassWord123>>"

	# convert the text into a hex string
	pwHex = secrets.str2hex(pw) // => 240-bit password

	# split into 5 shares, with a threshold of 3, WITH zero-padding
	shares = secrets.share(pwHex, 5, 3, 1024) // => 1024-bit padded shares

	# combine 3 shares
	comb = secrets.combine([shares[1], shares[3], shares[4]])

	# convert back to UTF string
	comb = secrets.hex2str(comb)

	print(comb == pw) // => true
	```