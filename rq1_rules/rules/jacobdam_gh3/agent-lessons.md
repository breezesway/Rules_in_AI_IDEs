---
inclusion: always
---

# Agent Lessons

## Rule for Adding Lessons

When you encounter a mistake or issue that could be prevented by following a specific process, add a concise lesson with:
- **Problem**: Brief description of what went wrong
- **Solution**: The correct approach or commands  
- **Commands**: Essential commands (if applicable)

Keep lessons short and actionable. Add new lessons at the bottom before the "Add new lessons here" line.

---

# Lessons Learned

Quick reference for common issues and their solutions when working with Kiro.

## Git Commands Hang in Terminal

**Problem:** Git commands like `git diff` hang because they use interactive pager (less)

**Solution:** Use `--no-pager` flag to bypass pager entirely

**Command:** `git --no-pager diff`

## Flutter Build Runner Deprecated Command

**Problem:** `flutter packages pub run build_runner` shows deprecation warning

**Solution:** Use `dart run build_runner` instead

**Command:** `dart run build_runner build --delete-conflicting-outputs`

## Missing Ferry Generated Files in Commits

**Problem:** Ferry serializer files missed when committing after `build_runner`

**Solution:** Always stage ALL generated files together

**Commands:**
```bash
git add lib/__generated__/ lib/src/init.config.dart
git status  # Verify serializers.gql.dart and serializers.gql.g.dart included
```

---

*Add new lessons here as they are discovered*