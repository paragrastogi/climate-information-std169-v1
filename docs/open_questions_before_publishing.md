# Open questions before publishing

Design questions and known discrepancies to resolve before the Climate Information
schema is finalised. These are **not** blockers for the worked examples, but each
should be settled before public release.

> Companion documents: `docs/implementation_and_application_notes.md` (the data-model
> design notes) and `docs/ashrae_dd_gap_analysis.md` (the column-level cross-check). The
> raw running list of committee questions and decisions is in
> `docs/notes_with_json_example.cleaned.md`.

---

## 1. Derived variables & extensibility

The committee's working principle is that variables derivable from measured variables by
a deterministic calculation should stay out of the **base** model, with guidance on how
providers pre-compute them into use-case "flavours" (e.g. an *ASHRAE-flavour* output
adding enthalpy, ranges, return periods, …). Open:

*Should derived variables be (a) defined-but-optional in the base model, (b) supported only via documented extensibility/custom groups, or (c) split into a separate auxiliary model? See `docs/implementation_and_application_notes.md` §6 for the current exclusion list and the quantities carried despite being derivable.*

