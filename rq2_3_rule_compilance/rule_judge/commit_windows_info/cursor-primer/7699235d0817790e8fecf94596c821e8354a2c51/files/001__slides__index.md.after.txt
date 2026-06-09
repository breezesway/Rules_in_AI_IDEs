---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# **Cursor IDE**
## Building your stdlib

A deep dive into Cursor's self-learning capabilities through `.cursor/rules`

*Inspired by a Geoffrey Huntley blog post: [stdlib](https://ghuntley.com/stdlib/)*

---

# What We'll Cover

1. What is Cursor?
2. Understanding Cursor Rules
3. The Power of Self-Learning
4. Best Practices & Tips

<!-- Speaker notes
This presentation demonstrates how Cursor's ability to learn and create new rules makes it an incredibly powerful development tool
-->

---

# What is Cursor?

An AI-first IDE that revolutionizes how we write code

- 💡 Intelligent Code Completion
- 🔍 Context-Aware Understanding
- 🤝 Natural Language Interaction
- 📚 Documentation Generation
- 🧠 Self-Learning Capabilities

---

# Why Cursor?

- **Faster Development**: AI assistance speeds up coding
- **Smarter Suggestions**: Understands project context
- **Learning System**: Improves over time
- **Customizable**: Adapts to your codebase
- **Open Source**: Community-driven improvements

---

# Cursor Modes

- **Ask**: User-initiated queries for code explanations, refactoring, or problem-solving
- **Manual**: Direct control over code editing with AI assistance when requested
- **Agent** (⌘I): Proactive AI that suggests improvements, identifies issues, and learns from your codebase

---

# Understanding Cursor Rules

The `.cursor/rules` system: Your AI's knowledge base

---

# What are Cursor Rules?

- Markdown files (`*.mdc` format)
- Project-specific guidelines
- AI behavior modifiers
- Codebase documentation
- Learning framework

---

# Rule Types

1. **Auto-attached**
   - Triggered by file patterns, e.g. `*.js`, `*.toml`, `content/*.md`, etc...
2. **Agent-requested**
   - Used when relevant, cursor agent reads the description of all rules to decide.
3. **Always**
   - Applied to every interaction, no matter what.
4. **Manual**
   - Explicitly referenced, either in agent chat or in another rule

---

# Rule Structure

```markdown
---
description: Rule purpose
globs: ["*.ts", "*.tsx"]
type: auto_attached
---
# Rule Title

## Context
What the rule addresses

## Guidelines
Specific instructions

## Examples
Code samples
```

---

# The Power of Self-Learning

How Cursor evolves with your project

1. 🔍 Identify patterns & errors
2. 📝 Document solutions
3. 🏗️ Create new rules
4. 🔄 Apply & refine

---

# Error Analysis Framework

1. Identify root cause
2. Document incorrect approach
3. Record correct solution
4. Create/update rules

---

# Rule Categories

- Type Errors
- Integration Issues
- Performance Patterns
- Dependency Management
- Project Conventions

---

# Benefits of Self-Learning

- 📈 Continuous improvement
- 🎯 More accurate suggestions
- 🚀 Faster development
- 🛠️ Reduced errors
- 📚 Growing knowledge base

---

# Live Demo

Watch Cursor learn and create new rules

1. Encounter a common error
2. Analyze the problem
3. Create a new rule
4. Test the improvement

---

# Example Rule Creation

```markdown
---
description: Handle TypeScript enum type safety
globs: ["*.ts", "*.tsx"]
type: auto_attached
---

# TypeScript Enum Best Practices

## Problem
Inconsistent enum usage leading to type errors

## Solution
Standardized enum pattern with type safety

## Examples
Before/After code samples
```

---

# Getting Started

1. Install Cursor IDE
2. Create `.cursor/rules` directory
3. Add your first rule
4. Watch it learn and grow

---

# Resources

- [Cursor IDE Website](https://cursor.sh)
- [Documentation](https://docs.cursor.com/get-started/welcome)
- [GitHub Repository](https://github.com/getcursor/cursor)
- [Community Forum](https://forum.cursor.com/)

---

# Thank You!

Start small with rules, and let them grow naturally as you encounter new patterns and challenges

[cursor.sh](https://cursor.sh)
