// wrapperV6.js

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

  let lastResult = null;

  try {
    const inputData = parseStringArray(inputJson);
    //const inputData = inputJson;
    //console.log("Commands received from Python: inputJSON: ", inputJson);
    console.log("Commands received from Python:", inputData);
    
    //jsonn = inputData.split(",");
    //console.log("Three: ", jsonn[2]);

    // Check if inputData is an array
    if (Array.isArray(inputData)) {
      // Loop through input data
      for (const command of inputData) {
        // Extract function name and arguments
        const functionName = command[0];
        const args = command.slice(1);

        // Dynamically call the function
        const selectedFunction = secrets[functionName];

        if (selectedFunction && typeof selectedFunction === 'function') {
          try {
            // Call the function with arguments
            lastResult = selectedFunction(...args);
          } catch (error) {
            // Capture and report the error to stderr
            console.error(error.message);
          }
        } else {
          // Report unknown function
          const errorMessage = `Unknown function: ${functionName}`;
          console.error(errorMessage);
        }
      }

      // Print the result of the last command
      console.log(JSON.stringify(lastResult));
    }
  } catch (error) {
    console.error("Error parsing or executing:", error.message);
    // In case of an error, print a JSON object with an "error" key
    console.log(JSON.stringify({ error: error.message }));
  }
}


function parseStringArray(inputString) {
    // Remove the opening and closing brackets and split the string by '], ['
    var arrayStr = inputString.slice(1, -1);
    var arrayItems = arrayStr.split(/\], \[/);

    // Iterate over each item and remove escape characters
    var parsedArray = arrayItems.map(item => {
        // Remove leading and trailing quotes
        item = item.replace(/^"/, '').replace(/"$/, '');

        // Replace escaped single quotes with single quotes
        item = item.replace(/\\'/g, "'");

        return [item];
    });

    // Return the parsed array
    return parsedArray;
}
