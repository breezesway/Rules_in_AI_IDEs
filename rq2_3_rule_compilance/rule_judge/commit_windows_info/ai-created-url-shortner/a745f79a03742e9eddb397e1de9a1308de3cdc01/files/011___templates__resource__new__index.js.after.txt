export default {
  prompt: ({ inquirer, args }) => {
    const questions = [];

    // Only prompt for resource name if not provided via command line
    if (!args.name) {
      questions.push({
        type: "input",
        name: "name",
        message: "Resource name (singular, e.g., user, post, product):",
        validate: (input) => {
          if (!input || input.length === 0) {
            return "Resource name is required";
          }
          // Check if it's a simple word (no spaces, special chars)
          if (!/^[a-z][a-z0-9]*$/i.test(input)) {
            return "Resource name must be a simple word (e.g., user, post, product)";
          }
          return true;
        },
        filter: (input) => {
          // Convert to lowercase
          return input.toLowerCase();
        },
      });
    }

    return inquirer.prompt(questions).then((answers) => {
      const name = args.name || answers.name;
      return {
        ...args,
        ...answers,
        name: name.toLowerCase(),
        // Generate plural form (simple pluralization)
        plural: name.toLowerCase().endsWith("s")
          ? name.toLowerCase()
          : name.toLowerCase() + "s",
        // Generate capitalized versions
        Name: name.charAt(0).toUpperCase() + name.slice(1).toLowerCase(),
        Plural:
          (name.toLowerCase().endsWith("s")
            ? name.toLowerCase()
            : name.toLowerCase() + "s"
          )
            .charAt(0)
            .toUpperCase() +
          (name.toLowerCase().endsWith("s")
            ? name.toLowerCase()
            : name.toLowerCase() + "s"
          ).slice(1),
      };
    });
  },
  actions: [
    // Create GET /api/resource (list all)
    {
      type: "add",
      path: "server/api/{{plural}}/index.get.ts",
      templateFile: "_templates/resource/new/index.get.ts.ejs.t",
    },
    // Create POST /api/resource (create new)
    {
      type: "add",
      path: "server/api/{{plural}}/index.post.ts",
      templateFile: "_templates/resource/new/index.post.ts.ejs.t",
    },
    // Create GET /api/resource/[id] (get by id)
    {
      type: "add",
      path: "server/api/{{plural}}/[id].get.ts",
      templateFile: "_templates/resource/new/[id].get.ts.ejs.t",
    },
    // Create PUT /api/resource/[id] (update by id)
    {
      type: "add",
      path: "server/api/{{plural}}/[id].put.ts",
      templateFile: "_templates/resource/new/[id].put.ts.ejs.t",
    },
    // Create DELETE /api/resource/[id] (delete by id)
    {
      type: "add",
      path: "server/api/{{plural}}/[id].delete.ts",
      templateFile: "_templates/resource/new/[id].delete.ts.ejs.t",
    },
    // Create POST /api/resource/[id]/action (custom action)
    {
      type: "add",
      path: "server/api/{{plural}}/[id]/action.post.ts",
      templateFile: "_templates/resource/new/[id].action.post.ts.ejs.t",
    },
    // Create test file
    {
      type: "add",
      path: "tests/e2e/api-{{plural}}.spec.ts",
      templateFile: "_templates/resource/new/test.ts.ejs.t",
    },
  ],

  afterAll: (answers) => {
    console.log(`
🚀 API resource '${answers.name}' generated successfully!

📁 Files created:
  └── server/api/${answers.plural}/
      ├── index.get.ts (GET /${answers.plural} - list all)
      ├── index.post.ts (POST /${answers.plural} - create new)
      ├── [id].get.ts (GET /${answers.plural}/:id - get by id)
      ├── [id].put.ts (PUT /${answers.plural}/:id - update by id)
      ├── [id].delete.ts (DELETE /${answers.plural}/:id - delete by id)
      └── [id]/action.post.ts (POST /${answers.plural}/:id/action - custom action)
  └── tests/e2e/api-${answers.plural}.spec.ts (e2e tests)

🔗 Available endpoints:
  • GET    /api/${answers.plural}
  • POST   /api/${answers.plural}
  • GET    /api/${answers.plural}/:id
  • PUT    /api/${answers.plural}/:id
  • DELETE /api/${answers.plural}/:id
  • POST   /api/${answers.plural}/:id/action

💡 Next steps:
  1. Update validation schemas for your ${answers.name} model
  2. Implement database operations in each endpoint
  3. Add guards for authentication/authorization as needed
  4. Test endpoints: npm run test:e2e
  5. View API docs at http://localhost:3000/api/_nitro/openapi.json`);
  },
};
