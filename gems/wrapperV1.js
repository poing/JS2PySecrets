// wrapperV1.js

/* 
This is the first working version of the wrapper. It's called by Python to run 
one (1) JavaScript command for the secrets.js package.

It's rudimentary, and any commands that need to be run before the main function
need to be added. This is because Node is called as a single instance, and it does not support subsequent calls. 

In the next version, the goal is to pass a series of commands and eliminate
the need to include setup commands.
*/

// Require the secrets package and assign it to a variable
const secrets = require('../secrets.js/secrets.js');

// If the script is executed directly, call the appropriate function based on arguments
if (require.main === module) {
  // Retrieve input JSON from command line arguments
  const inputJson = process.argv[2];
  
  // Commands run before the main command
  //secrets.setRNG("testRandom");
  //secrets.init(12, "testRandom");

  if (!inputJson) {
    console.error("No input provided.");
    process.exit(1);
  }

  try {
    // Parse the input JSON
    const input_data = JSON.parse(inputJson);

    const functionName = input_data.functionName;
    const arguments = input_data.arguments;

    // Dynamically call the function
    const selectedFunction = secrets[functionName];

    if (selectedFunction && typeof selectedFunction === 'function') {
      // Call the selected function
      const result = selectedFunction(...arguments);

      // Format the result as a JSON object
      const resultJson = JSON.stringify({ result });

      // Print only the result to the console
      console.log(resultJson);
    } else {
      console.log(JSON.stringify({ error: `Unknown function: ${functionName}` }));
    }
  } catch (error) {
    console.error("Error parsing or executing:", error.message);
    // In case of an error, print a JSON object with an "error" key
    console.log(JSON.stringify({ error: error.message }));
  }
}
