// wrapperV2.js

/* 
This is the second working version of the wrapper. accepting multiple JavaScript command for the secrets.js package.
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
    //console.log(typeof inputData.tasks);

    // Check if inputData has a "tasks" key
    if ("tasks" in inputData && Array.isArray(inputData.tasks)) {
      // Loop through tasks
      for (const task of inputData.tasks) {
        // Check if task has a "setup" key
        if ("setup" in task && Array.isArray(task.setup)) {
          // Loop through setup tasks
          for (const setupTask of task.setup) {
            const setupFunction = setupTask.function;
            const setupArguments = setupTask.args;

            // Dynamically call the setup function
            const setupFn = secrets[setupFunction];

            if (setupFn && typeof setupFn === 'function') {
              // Call the setup function
              setupFn(...setupArguments);
            } else {
              console.log(JSON.stringify({ error: `Unknown function: ${setupFunction}` }));
            }
          }
        }

        // Check if task has a "start" key
        if ("start" in task) {
          const functionName = task.start.function;
          const arguments = task.start.args;

          // Dynamically call the main function
          const selectedFunction = secrets[functionName];

          if (selectedFunction && typeof selectedFunction === 'function') {
            // Call the main function
            const result = selectedFunction(...arguments);

            // Format the result as a JSON object
            const resultJson = JSON.stringify({ result });

            // Print only the result to the console
            console.log(resultJson);
          } else {
            console.log(JSON.stringify({ error: `Unknown function: ${functionName}` }));
          }
        }
      }
    }
  } catch (error) {
    console.error("Error parsing or executing:", error.message);
    // In case of an error, print a JSON object with an "error" key
    console.log(JSON.stringify({ error: error.message }));
  }
}
