# Cursor AI Agent Project Instructions Generator

A meta-project for generating comprehensive instructions for all future projects using Cursor AI.

## Purpose

This project provides a framework for creating detailed, structured instructions for any type of project, whether technical, creative, business, or personal. It helps to:

- Systematically plan new projects from inception to completion
- Create living documentation that evolves with the project
- Establish consistent workflows for development and tracking
- Leverage AI assistance effectively throughout the project lifecycle

## Structure

The project is organized as follows:

```
.cursor/rules/                     # Main Cursor rules
├── project_instruction_generator.mdc  # Rule for generating project instructions
├── cursor_rule_creator.mdc            # Rule for creating new Cursor rules
└── [other_rules].mdc                  # Additional specialized rules

project_templates/                 # Template examples for different project types
├── technical/
│   ├── web/
│   ├── mobile/
│   ├── api/
│   ├── data/
│   ├── game/
│   └── tool/
├── creative/
│   ├── writing/
│   ├── design/
│   └── media/
├── business/
│   ├── planning/
│   ├── marketing/
│   └── analytics/
└── personal/
    ├── life/
    ├── learning/
    └── productivity/
```

## Usage

### Project Instruction Generator

This rule helps create comprehensive project plans and instructions tailored to your specific project needs. Simply open up the Agent chat in this project folder, describe a project idea you have in as much detail as possible, and a starter prompt/set of instructions will be created for that project.

The instructions will be used to guide Cursor's AI Agent through:

- Initial project assessment and planning
- Creating structured project documentation
- Setting up appropriate tools and environments
- Establishing consistent workflows
- Tracking progress with journal entries
- Quality control and delivery processes

### Begin your project:

1. Create a new empty project folder
2. Copy the appropriate set of generated instructions from this project to your new project folder
3. Add the instructions file to Agent chat
4. Tell Cursor AI to follow the instructions
5. Watch in wonder as the Agent builds your project systematically

### Cursor Rule Creator

This rule helps you create new Cursor rules for specialized project types. It provides guidance on:

- Rule purpose and structure
- Development workflow for rules
- Organization and maintenance
- Best practices for effective rules

### Extending This Project

To add support for new project types:

1. Use the Cursor Rule Creator to develop a new rule
2. Create example templates in the corresponding `project_templates/` directory
3. Remember that template organization can use subdirectories, but Cursor rules must all be placed directly in the `.cursor/rules/` directory 