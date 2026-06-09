/** @type {import('eslint').Rule.RuleModule} */
export default {
  meta: {
    type: "suggestion",
    docs: {
      description: "Enforce proper Nuxt data fetching patterns",
      category: "Best Practices",
      recommended: true,
    },
    fixable: "code",
    hasSuggestions: true,
    schema: [
      {
        type: "object",
        properties: {
          enforcePageLevelFetching: {
            type: "boolean",
            default: true,
          },
        },
        additionalProperties: false,
      },
    ],
    messages: {
      useFetchInSetup:
        "Use useFetch() or useAsyncData() instead of fetch() in script setup root level",
      use$FetchInFunction:
        "Use $fetch() instead of fetch() in functions, event handlers, and lifecycle hooks",
      no$FetchInSetup:
        "$fetch() should not be used at script setup root level. Use useFetch() or useAsyncData() instead. Note: $fetch() returns data directly while useFetch() returns { data, error, status, etc. }",
      preferUseFetch:
        "Prefer useFetch() over useAsyncData() when making HTTP requests",
      considerPageLevel:
        "Consider moving data fetching to page level and passing data via props",
      useAsyncDataForComplexCases:
        "Consider useAsyncData() for complex data transformation or multiple requests",
    },
  },

  create(context) {
    const options = context.options[0] || {};
    const enforcePageLevelFetching = options.enforcePageLevelFetching !== false;

    let isInScriptSetup = false;
    let isInFunction = false;
    let currentFunctionDepth = 0;
    let isInEventHandler = false;
    let isInLifecycleHook = false;

    // Track if we're in a Vue component vs page
    let isPage = false;
    let filename = context.getFilename();
    if (filename) {
      isPage = filename.includes("/pages/") || filename.includes("\\pages\\");
    }

    function isLifecycleHookCall(node) {
      if (node.type === "CallExpression" && node.callee.type === "Identifier") {
        const lifecycleHooks = [
          "onMounted",
          "onUpdated",
          "onUnmounted",
          "onBeforeMount",
          "onBeforeUpdate",
          "onBeforeUnmount",
          "onActivated",
          "onDeactivated",
          "onErrorCaptured",
          "onRenderTracked",
          "onRenderTriggered",
        ];
        return lifecycleHooks.includes(node.callee.name);
      }
      return false;
    }

    function isEventHandlerFunction(node) {
      // Check if function is likely an event handler based on context
      if (
        node.type === "ArrowFunctionExpression" ||
        node.type === "FunctionExpression"
      ) {
        const parent = node.parent;
        if (parent && parent.type === "Property") {
          const key = parent.key;
          if (key && key.name && key.name.startsWith("on")) {
            return true; // onSubmit, onClick, etc.
          }
        }
        if (parent && parent.type === "CallExpression") {
          const callee = parent.callee;
          if (callee && callee.type === "MemberExpression") {
            const property = callee.property;
            if (property && property.name === "addEventListener") {
              return true;
            }
          }
        }
      }
      return false;
    }

    function getFetchReplacement(node) {
      const isInRootSetup = isInScriptSetup && currentFunctionDepth === 0;

      if (isInRootSetup) {
        // In script setup root level, suggest useFetch
        const args = node.arguments;
        if (args.length > 0) {
          const url = context.getSourceCode().getText(args[0]);
          let optionsText = "";
          if (args.length > 1) {
            optionsText = `, ${context.getSourceCode().getText(args[1])}`;
          }
          return `useFetch(${url}${optionsText})`;
        }
        return "useFetch(url)";
      } else {
        // In functions, event handlers, lifecycle hooks, suggest $fetch
        const fullCall = context.getSourceCode().getText(node);
        return fullCall.replace("fetch(", "$fetch(");
      }
    }

    return {
      // Track when we enter script setup
      Program() {
        // Check if this is a script setup block in a Vue SFC
        const sourceCode = context.getSourceCode();
        const text = sourceCode.getText();
        // Match <script> tags with setup attribute, regardless of other attributes
        isInScriptSetup = /<script[^>]*\bsetup\b[^>]*>/i.test(text);
        currentFunctionDepth = 0;
      },

      // Track function depth
      "FunctionDeclaration, FunctionExpression, ArrowFunctionExpression"(node) {
        currentFunctionDepth++;
        isInFunction = currentFunctionDepth > 0;

        if (isEventHandlerFunction(node)) {
          isInEventHandler = true;
        }
      },

      "FunctionDeclaration, FunctionExpression, ArrowFunctionExpression:exit"(
        _node
      ) {
        currentFunctionDepth--;
        isInFunction = currentFunctionDepth > 0;

        if (isEventHandlerFunction(_node)) {
          isInEventHandler = false;
        }
      },

      // Track lifecycle hooks
      CallExpression(node) {
        if (isLifecycleHookCall(node)) {
          isInLifecycleHook = true;
        }

        // Check for native fetch usage
        if (node.callee.type === "Identifier" && node.callee.name === "fetch") {
          const isInRootSetup = isInScriptSetup && currentFunctionDepth === 0;

          if (isInRootSetup) {
            context.report({
              node,
              messageId: "useFetchInSetup",
              fix(fixer) {
                return fixer.replaceText(node, getFetchReplacement(node));
              },
            });
          } else if (isInFunction || isInEventHandler || isInLifecycleHook) {
            context.report({
              node,
              messageId: "use$FetchInFunction",
              fix(fixer) {
                return fixer.replaceText(node, getFetchReplacement(node));
              },
            });
          }
        }

        // Check for $fetch usage in script setup root level
        if (
          node.callee.type === "Identifier" &&
          node.callee.name === "$fetch"
        ) {
          const isInRootSetup = isInScriptSetup && currentFunctionDepth === 0;

          if (isInRootSetup) {
            context.report({
              node,
              messageId: "no$FetchInSetup",
              // No auto-fix because $fetch and useFetch have different return types
            });
          }
        }

        // Check for useAsyncData vs useFetch preference
        if (
          node.callee.type === "Identifier" &&
          node.callee.name === "useAsyncData"
        ) {
          // Check if this could be simplified to useFetch
          const args = node.arguments;
          if (args.length >= 2 && args[1].type === "ArrowFunctionExpression") {
            const fetcherBody = args[1].body;
            // Simple heuristic: if the fetcher just returns a fetch call, suggest useFetch
            if (
              fetcherBody.type === "CallExpression" &&
              ((fetcherBody.callee.type === "Identifier" &&
                fetcherBody.callee.name === "$fetch") ||
                (fetcherBody.callee.type === "Identifier" &&
                  fetcherBody.callee.name === "fetch"))
            ) {
              context.report({
                node,
                messageId: "preferUseFetch",
                suggest: [
                  {
                    desc: "Replace with useFetch()",
                    fix(fixer) {
                      const url = fetcherBody.arguments[0];
                      let options = "";
                      if (fetcherBody.arguments.length > 1) {
                        options = `, ${context
                          .getSourceCode()
                          .getText(fetcherBody.arguments[1])}`;
                      }
                      if (args.length > 2) {
                        options += `, ${context
                          .getSourceCode()
                          .getText(args[2])}`;
                      }
                      return fixer.replaceText(
                        node,
                        `useFetch(${context
                          .getSourceCode()
                          .getText(url)}${options})`
                      );
                    },
                  },
                ],
              });
            }
          }
        }

        // Suggest page-level fetching for components
        if (
          enforcePageLevelFetching &&
          !isPage &&
          isInScriptSetup &&
          currentFunctionDepth === 0
        ) {
          if (
            (node.callee.type === "Identifier" &&
              (node.callee.name === "useFetch" ||
                node.callee.name === "useAsyncData")) ||
            (node.callee.type === "Identifier" && node.callee.name === "fetch")
          ) {
            context.report({
              node,
              messageId: "considerPageLevel",
              // Don't auto-fix this as it requires architectural changes
            });
          }
        }
      },

      "CallExpression:exit"(node) {
        if (isLifecycleHookCall(node)) {
          isInLifecycleHook = false;
        }
      },
    };
  },
};
