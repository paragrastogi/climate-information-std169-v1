Climate Information Data Model Specification
============================================

An open source data model specification for climate information developed through a stakeholder consensus process by the IBPSA-USA Building Data Exchange Committee.

Access the document here: https://ibpsa-usa.github.io/climate-information/

Contributing
------------

Markdown files in this repo are kept **ASCII-only** for consistency with the schema's
unit strings (`W/m2`, `J/kg`, `^` for exponents) and to stay greppable. A checker
enforces this:

```bash
python3 tools/check_ascii_md.py        # check every tracked *.md
git config core.hooksPath .githooks    # one-time: enable the pre-commit hook
```

With the hook enabled, a commit that adds a non-ASCII character to a `.md` file is
blocked locally; CI runs the same check on every push (`.github/workflows/ascii-check.yaml`).

