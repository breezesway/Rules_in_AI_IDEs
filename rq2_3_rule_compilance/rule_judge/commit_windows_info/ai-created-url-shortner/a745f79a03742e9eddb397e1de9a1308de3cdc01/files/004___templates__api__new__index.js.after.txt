export default {
  prompt: ({ inquirer, args }) => {
    const questions = [];

    // Only prompt for path if not provided via command line
    if (!args.path) {
      questions.push({
        type: "input",
        name: "path",
        message:
          "API endpoint path (relative to server/api, e.g., users/profile, auth/login, health):",
        validate: (input) => {
          if (!input || input.length === 0) {
            return "Endpoint path is required";
          }
          // Check if path segments are kebab-case
          const segments = input.split("/");
          for (const segment of segments) {
            if (
              !/^[a-z][a-z0-9-]*[a-z0-9]$/.test(segment) &&
              !/^[a-z][a-z0-9]*$/.test(segment)
            ) {
              return "Path segments must be kebab-case (e.g., users/profile, auth/login)";
            }
          }
          return true;
        },
        filter: (input) => {
          // Convert to lowercase and replace spaces/underscores with hyphens
          return input.toLowerCase().replace(/[_\s]+/g, "-");
        },
      });
    }

    // Prompt for HTTP method
    if (!args.method) {
      questions.push({
        type: "list",
        name: "method",
        message: "HTTP method:",
        choices: [
          { name: "GET", value: "get" },
          { name: "POST", value: "post" },
          { name: "PUT", value: "put" },
          { name: "DELETE", value: "delete" },
          { name: "PATCH", value: "patch" },
        ],
        default: "get",
      });
    }

    return inquirer.prompt(questions).then((answers) => {
      // Merge command line args with prompted answers
      const result = {
        ...args,
        ...answers,
        // Ensure path is kebab-case even when passed via command line
        path: args.path
          ? args.path.toLowerCase().replace(/[_\s]+/g, "-")
          : answers.path,
        method: args.method || answers.method,
      };

      // Generate values from path
      result.testName = result.path.replace(/\//g, "-");
      result.tag = result.path.split("/")[0]; // Use first segment of path as tag

      // Determine if endpoint typically needs request body based on method
      result.hasRequestBody = ["post", "put", "patch"].includes(result.method);
      result.hasQueryParams = result.method === "get";

      return result;
    });
  },
  actions: [
    // Create API endpoint file
    {
      type: "add",
      path: "server/api/{{path}}.{{method}}.ts",
      templateFile: "_templates/api/new/endpoint.ts.ejs.t",
    },
    // Create test file
    {
      type: "add",
      path: "tests/e2e/api-{{testName}}.spec.ts",
      templateFile: "_templates/api/new/test.ts.ejs.t",
    },
  ],

  afterAll: (answers) => {
    console.log(`
🚀 API endpoint '${answers.path}' boilerplate generated successfully!

📁 Files created:
  ├── server/api/${answers.path}.${answers.method}.ts (endpoint)
  └── tests/e2e/api-${answers.testName}.spec.ts (e2e test)

🔗 Endpoint will be available at: /api/${answers.path}
📖 Method: ${answers.method.toUpperCase()}

💡 Next steps:
  1. Implement your business logic in the endpoint
  2. Update the test with your specific test cases
  3. Test the endpoint: curl -X ${answers.method.toUpperCase()} http://localhost:3000/api/${
      answers.path
    }
  4. View API docs at http://localhost:3000/api/_nitro/openapi.json`);
  },
};
