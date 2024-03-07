// wrapperV8.js

/* 
This is the third working version of the wrapper.  Better error handling and accepting multiple JavaScript commands for the secrets.js package.
*/

// Require the secrets package and assign it to a variable
const secrets = require('../secrets.js/secrets.js');

// If the script is executed directly, call the appropriate function based on arguments
if (require.main === module) {
  const commands = process.argv.slice(2);
  
  if (!commands.length) {
    console.error("No commands provided.");
    process.exit(1);
  }

  try {
	  console.log("Commands received from Python:", commands);

    // Loop through commands
    for (const command of commands) {
      // Evaluate each command
      eval(command);
    }
  } catch (error) {
    console.error("Error executing command:", error.message);
    process.exit(1);
  }
}
