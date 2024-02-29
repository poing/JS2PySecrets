// wrapperV9.js

/* 
This is the third working version of the wrapper.  Better error handling and accepting multiple JavaScript commands for the secrets.js package.
*/

// Used to decode the CLI arg
// function decodeFromBase36(base36String) {
//     const decodedData = {};
//     while (base36String.length > 0) {
//         const key = base36String.substring(0, 4);
//         const value = parseInt(base36String.substring(4, 6), 36);
//         decodedData[key] = value;
//         base36String = base36String.substring(6);
//     }
//     return decodedData;
// }

function hex2a(hex) 
{
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}     

function escapeSingleQuotes(str) {
    return str.replace(/'/g, "\\'");
}

// Require the secrets package and assign it to a variable
const secrets = require('../secrets.js/secrets.js');

// If the script is executed directly, call the appropriate function based on arguments
if (require.main === module) {
  const commands = hex2a(process.argv[2]); // Change here

  if (!commands.length) {
    console.error("No commands provided.");
    process.exit(1);
  }

  try {

	  console.log("Commands received from Python:", commands);
	  
	  //return commands;
	  const inputData = JSON.parse(commands);
	  //cleanup = escapeSingleQuotes(commands);
	  //console.log("Cleanup: ", cleanup);
	  //inputData = JSON.parse(cleanup);
	  //inputData = JSON.parse(commands);
	  console.log("inputData[1][0]: ", inputData[1][0]);

    // Loop through commands
//    for (const command of commands) {
      // Evaluate each command
//      eval(command);
//    }
  } catch (error) {
    console.error("Error executing command:", error.message);
    process.exit(1);
  }
}
