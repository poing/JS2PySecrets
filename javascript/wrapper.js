// wrapper.js

/* 
A revised and simplified version of JavaScript the wrapper.  Accepts multiple JavaScript commands for the secrets.js package, returning the output of the last command.
*/

// Hex to ASCII
function hex2a(hex) 
{
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}     

// Require the secrets package and assign it to a variable
const secrets = require('../node_modules/secrets.js-grempe/secrets.js');

// If the script is executed directly, call the appropriate function based on arguments
if (require.main === module) {
  const commands = hex2a(process.argv[2]);
   
  if (!commands.length) {
    console.error("No commands provided.");
    process.exit(1);
  }

  try {
	// The the commands to execute
	const inputData = JSON.parse(commands);

	// Debugging statements
	//console.log("Commands received from Python:", commands);
	//console.log("inputData[0][0]: ", inputData[0][0]); // returns: init(33)

	// Loop through commands	
	for (const command of inputData) {
		// Evaluate each command
		lastResult = eval('secrets.' + command);
	}

	// Return the result of the last command
	console.log(JSON.stringify(lastResult));

  } catch (error) {
    console.error("Error executing command:", error.message);
    process.exit(1);
  }
}
