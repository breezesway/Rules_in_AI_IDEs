# Prompt Engineering Guidelines

This document defines how Kiro specifications are translated into effective prompts for adventure generation, ensuring consistent quality and adherence to professional standards.

## Core Prompt Structure

### 1. System Message Patterns
```
Professional Mode: "You are a professional adventure designer. Generate a complete, high-quality TTRPG adventure in valid JSON format following ALL specified requirements exactly."

Standard Mode: "You are a creative and experienced Game Master. Generate detailed, engaging TTRPG adventures in valid JSON format."
```

### 2. Prompt Engineering Principles

#### Specification Mapping
- **Advanced Prompt System** → Complex multi-layered narratives with branching paths
- **Professional Mode** → Publication-ready content with complete stat blocks
- **Visual Tiers** → Rich descriptive content optimized for image generation
- **Unified Tiers** → Content scaled to user tier capabilities

#### Quality Requirements Integration
From `.kiro/specs/professional-mode-integration/requirements.md`:
- PLAYABLE structure with 3-5 detailed scenes
- MECHANICAL balance with consistent DCs
- COMPLETENESS with full stat blocks and details
- GM USABILITY with read-aloud text and guidance
- PROFESSIONAL polish with no contradictions

## Prompt Templates

### Adventure Generation Template
```
You are an award-winning Game Master with 20+ years of experience.

CRITICAL REQUIREMENTS:
1. Generate exactly 3-5 playable scenes with specific objectives
2. Include complete stat blocks for ALL creatures mentioned
3. Provide consistent DCs within 2 points for equivalent difficulty
4. Add read-aloud text for key moments
5. Include failure consequences that don't block progress

USER PROMPT: "{derived_from_spec}"
GAME SYSTEM: {game_system}
PROFESSIONAL MODE: {enabled/disabled}

IMPORTANT: Respond ONLY with valid JSON in the exact structure specified.
```

### NPC Generation Template
```
Generate a professional NPC with complete mechanical and roleplay details.

REQUIREMENTS:
- Full stat block appropriate to CR/level
- Detailed personality and motivation
- Combat tactics and social behavior
- Connection to adventure narrative
- Dialogue samples for different situations

NPC CONTEXT: "{context_from_adventure}"
```

### Image Prompt Template
```
Generate [monster/character/scene] image prompt for fantasy TTRPG adventure.

VISUAL CONSISTENCY REQUIREMENTS:
- Theme: {adventure.theme}
- Tone: {adventure.tone} 
- Art Style: Professional fantasy art, digital painting style
- Lighting: Dramatic lighting appropriate to scene mood
- Composition: Clear focal point, adventure-game appropriate

SUBJECT: {detailed_description}
```

## Quality Validation Patterns

### JSON Structure Validation
- Always include validation checklist in prompts
- Require specific field structure matching frontend expectations
- Include error recovery instructions for malformed responses

### Content Quality Checks
- Verify all mentioned elements have corresponding details
- Ensure mechanical balance across encounters
- Check narrative consistency and logical progression
- Validate GM usability with clear instructions

## Implementation Notes

### Model-Specific Optimizations
- **GPT-5-mini**: Focus on structured output, clear instructions
- **Claude-4-Sonnet**: Leverage reasoning capabilities for complex narratives  
- **Gemini-2.5-Flash**: Optimize for creative visual descriptions

### Professional Mode Enhancements
- Activate when `.kiro/specs/professional-mode-integration/*` is referenced
- Include advanced validation requirements
- Enable multi-layered narrative structures
- Add publication-ready formatting guidelines

## Steering Rules

1. **Consistency First**: All prompts must produce consistent output structure
2. **Specification Adherence**: Map Kiro specs directly to prompt requirements
3. **Quality Gates**: Include validation steps in generation process
4. **User Experience**: Optimize for GM usability and player engagement
5. **Technical Integration**: Ensure compatibility with PDF export and image generation

---

*This document is maintained by the Kiro steering system and should be updated when new specifications are added.*