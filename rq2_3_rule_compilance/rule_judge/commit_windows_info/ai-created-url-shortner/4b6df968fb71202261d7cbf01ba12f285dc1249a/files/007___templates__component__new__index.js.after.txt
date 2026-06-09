export default {
  prompt: ({ inquirer, args }) => {
    const questions = [];

    // Only prompt for name if not provided via command line
    if (!args.name) {
      questions.push({
        type: "input",
        name: "name",
        message: "Component name (PascalCase):",
        validate: (input) => {
          if (!input || input.length === 0) {
            return "Component name is required";
          }
          // Check if it's PascalCase
          if (!/^[A-Z][a-zA-Z0-9]*$/.test(input)) {
            return "Component name must be PascalCase (e.g., UserProfile, HeaderNav)";
          }
          return true;
        },
        filter: (input) => {
          // Convert to PascalCase just in case
          return input.charAt(0).toUpperCase() + input.slice(1);
        },
      });
    }

    return inquirer.prompt(questions).then((answers) => {
      // Merge command line args with prompted answers
      return {
        ...args,
        ...answers,
        // Ensure name is PascalCase even when passed via command line
        name: args.name
          ? args.name.charAt(0).toUpperCase() + args.name.slice(1)
          : answers.name,
      };
    });
  },
  actions: [
    // Create component directory
    {
      type: "add",
      path: "app/components/{{name}}/{{name}}.vue",
      templateFile: "_templates/component/new/component.vue.ejs.t",
    },
    // Create child component
    {
      type: "add",
      path: "app/components/{{name}}/{{name}}Child.vue",
      templateFile: "_templates/component/new/child-component.vue.ejs.t",
    },
    // Create unit test
    {
      type: "add",
      path: "app/components/{{name}}/{{name}}.nuxt.test.ts",
      templateFile: "_templates/component/new/test.ts.ejs.t",
    },
    // Create README
    {
      type: "add",
      path: "app/components/{{name}}/README.md",
      templateFile: "_templates/component/new/readme.md.ejs.t",
    },
  ],

  afterAll: (answers) => {
    console.log(`
🎉 Component '${answers.name}' boilerplate generated successfully!

📁 Files created:
  └── app/components/${answers.name}/
      ├── ${answers.name}.vue (main component)
      ├── ${answers.name}Child.vue (child component)
      ├── ${answers.name}.nuxt.test.ts (unit test)
      └── README.md (documentation)

  Now you can customize the component to the use cases at hand. 
  Also remember to add examples of the component to the playground by in a new file app/pages/playground/${answers.name}Demo.vue

💡 Pro tip: The component is auto-imported by Nuxt - no manual imports needed!`);
  },
};
