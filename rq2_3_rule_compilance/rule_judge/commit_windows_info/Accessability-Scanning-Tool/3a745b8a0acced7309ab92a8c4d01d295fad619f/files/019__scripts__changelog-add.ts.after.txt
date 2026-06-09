#!/usr/bin/env node

import * as fs from 'fs';
import * as readline from 'readline';

// ANSI color codes for better output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    red: '\x1b[31m',
} as const;

type ColorName = keyof typeof colors;

function log(message: string, color: ColorName = 'reset'): void {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function createReadlineInterface(): readline.Interface {
    return readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });
}

function question(rl: readline.Interface, prompt: string): Promise<string> {
    return new Promise(resolve => {
        rl.question(`${colors.cyan}${prompt}${colors.reset}`, resolve);
    });
}

function addToChangelog(section: string, entry: string): boolean {
    const changelogPath = 'CHANGELOG.md';

    if (!fs.existsSync(changelogPath)) {
        log('❌ CHANGELOG.md not found', 'red');
        return false;
    }

    let changelog = fs.readFileSync(changelogPath, 'utf8');

    // Find the [Unreleased] section
    const unreleasedIndex = changelog.indexOf('## [Unreleased]');
    if (unreleasedIndex === -1) {
        log('❌ [Unreleased] section not found in CHANGELOG.md', 'red');
        return false;
    }

    // Find the specific section (Added, Changed, Fixed, etc.)
    const sectionHeader = `### ${section}`;
    const sectionIndex = changelog.indexOf(sectionHeader, unreleasedIndex);

    if (sectionIndex === -1) {
        // Create the section if it doesn't exist
        const nextVersionIndex = changelog.indexOf('\n## [', unreleasedIndex + 1);
        const insertionPoint = nextVersionIndex !== -1 ? nextVersionIndex : changelog.length;

        const newSection = `\n### ${section}\n- ${entry}\n`;
        changelog = changelog.slice(0, insertionPoint) + newSection + changelog.slice(insertionPoint);
    } else {
        // Add to existing section
        const nextSectionIndex = changelog.indexOf('\n### ', sectionIndex + 1);
        const nextVersionIndex = changelog.indexOf('\n## [', sectionIndex + 1);

        let insertionPoint: number;
        if (
            nextSectionIndex !== -1 &&
            (nextVersionIndex === -1 || nextSectionIndex < nextVersionIndex)
        ) {
            insertionPoint = nextSectionIndex;
        } else if (nextVersionIndex !== -1) {
            insertionPoint = nextVersionIndex;
        } else {
            insertionPoint = changelog.length;
        }

        const newEntry = `- ${entry}\n`;
        changelog = changelog.slice(0, insertionPoint) + newEntry + changelog.slice(insertionPoint);
    }

    fs.writeFileSync(changelogPath, changelog);
    return true;
}

async function main(): Promise<void> {
    const rl = createReadlineInterface();

    try {
        log('📝 Add entry to CHANGELOG.md', 'cyan');
        log('Available sections: Added, Changed, Deprecated, Removed, Fixed, Security', 'blue');

        const section = await question(rl, 'Enter section (Added/Changed/Fixed/etc.): ');
        const entry = await question(rl, 'Enter changelog entry: ');

        if (!section || !entry) {
            log('❌ Both section and entry are required', 'red');
            process.exit(1);
        }

        // Capitalize first letter
        const capitalizedSection = section.charAt(0).toUpperCase() + section.slice(1);

        if (addToChangelog(capitalizedSection, entry)) {
            log(`✅ Added entry to ${capitalizedSection} section`, 'green');
        } else {
            log('❌ Failed to add entry to changelog', 'red');
            process.exit(1);
        }
    } catch (error) {
        log(`❌ Error: ${error instanceof Error ? error.message : String(error)}`, 'red');
        process.exit(1);
    } finally {
        rl.close();
    }
}

// Only run main if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    main();
}

export { addToChangelog }; 