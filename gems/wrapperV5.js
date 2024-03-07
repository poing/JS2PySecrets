// wrapperV5.js

/* 
FAILED - FAILED - FAILED - FAILED - FAILED - FAILED

This is the FAILED wrapper.  Better error handling and accepting multiple JavaScript command for the secrets.js package.

FAILED - FAILED - FAILED - FAILED - FAILED - FAILED
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
    const output = { results: [] };

    // Check if inputData has a "tasks" key
    if ("tasks" in inputData && Array.isArray(inputData.tasks)) {
      // Loop through tasks
      for (const task of inputData.tasks) {
        const taskResult = {};

        // Check if task has a "setup" key
        if ("setup" in task && Array.isArray(task.setup)) {
          // Loop through setup tasks
          for (const setupTask of task.setup) {
            const setupFunction = setupTask.function;
            const setupArguments = setupTask.args;

            // Dynamically call the setup function
            const setupFn = secrets[setupFunction];

            if (setupFn && typeof setupFn === 'function') {
              try {
                // Call the setup function
                setupFn(...setupArguments);
                taskResult.setupResult = { success: true };
              } catch (error) {
                // Capture and report the error to stderr
                console.error(error.message);
                taskResult.setupResult = { success: false, error: error.message };
              }
            } else {
              // Report unknown function
              const errorMessage = `Unknown function: ${setupFunction}`;
              console.error(errorMessage);
              taskResult.setupResult = { success: false, error: errorMessage };
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
            try {
              // Check if the argument is a dictionary with 'arrayArg'
              if (arguments && typeof arguments === 'object' && 'arrayArg' in arguments) {
                // Extract the array from the dictionary
                const arrayArg = arguments.arrayArg;
                //console.error(arguments.arrayArg);
                // Call the main function with the array argument
                const result = selectedFunction(arrayArg);
                taskResult.startResult = { success: true, result };
              } else {
                // Call the main function with the provided arguments
                const result = selectedFunction(...arguments);
                taskResult.startResult = { success: true, result };
              }
            } catch (error) {
              // Capture and report the error to stderr
              console.error(error.message);
              taskResult.startResult = { success: false, error: error.message };
            }
          } else {
            // Report unknown function
            const errorMessage = `Unknown function: ${functionName}`;
            console.error(errorMessage);
            taskResult.startResult = { success: false, error: errorMessage };
          }
        }

        // Add task result to the output
        output.results.push(taskResult);
      }

      // Print the output as a JSON object
      console.log(JSON.stringify(output));
    }
  } catch (error) {
    console.error("Error parsing or executing:", error.message);
    // In case of an error, print a JSON object with an "error" key
    console.log(JSON.stringify({ error: error.message }));
  }
}

