// wrapperV7.js

/* 
This is the third working version of the wrapper.  Better error handling and accepting multiple JavaScript commands for the secrets.js package.
*/

// Require the secrets package and assign it to a variable
const secrets = require('../secrets.js/secrets.js');

// If the script is executed directly, call the appropriate function based on arguments
if (require.main === module) {
  const inputJson = process.argv[2];

  if (!inputJson) {
    console.error("No input provided.");
    process.exit(1);
  }

  try {
    const inputData = JSON.parse(inputJson);
    console.log("Commands received from Python:", inputData);
    
    // Check if inputData is an array
    if (Array.isArray(inputData)) {
      // Loop through input data
      for (const command of inputData) {
        // Evaluate each command
        eval(command);
      }
    }
  } catch (error) {
    console.error("Error parsing or executing:", error.message);
    // In case of an error, print a JSON object with an "error" key
    console.log(JSON.stringify({ error: error.message }));
  }
}
