---
inclusion: always
---

# Kiro Lessons Learned

Quick reference for common issues and their solutions when working with Kiro.

## Git Commands Hang in Terminal

**Problem:** Git commands like `git diff` hang because they use interactive pager (less)

**Solution:** Use `--no-pager` flag to bypass pager entirely

**Command:** `git --no-pager diff`

---

*Add new lessons here as they are discovered*