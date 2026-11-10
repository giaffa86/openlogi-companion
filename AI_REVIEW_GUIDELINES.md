# Review for personal use

Official references consulted on October 28, 2026:

- https://gjs.guide/extensions/review-guidelines/review-guidelines.html
- https://gjs.guide/extensions/review-guidelines/best-practices.html

Keep AI provenance in project documentation only. Source and runtime files
carry only the `GPL-3.0-or-later` SPDX identifier. The
[review guidelines](https://gjs.guide/extensions/review-guidelines/review-guidelines.html)
list comments resembling LLM prompts or other indications of AI output as
reasons for rejection. The author remains responsible for understanding and
maintaining the JavaScript; do not submit without this review.

The ZIP contains no AI notices, prompts, provenance notes or documentation.
`README.md`, this file and `docs/` stay in the repository, outside the bundle.
Previous local reviews recommend checking APIs, cleanup and simplicity, while
keeping code provenance documented in the repository.

Check before every delivery:

1. Use real GNOME 50 APIs, without speculative compatibility or invented methods.
2. No `_enabled`/`_destroyed` lifecycle flags or optional calls to guaranteed APIs.
3. Catch only at fallible boundaries: spawn, reads, wait, JSON and GUI launch.
   Data failures use local codes, without logging upstream messages.
4. Remove timers alongside their replacement. Their owner releases cancellables,
   signals and processes. Do not terminate the GUI or agent on disable.
5. Invalidate stale responses before destroying actors.
6. Build the ZIP from an explicit file list, preserving module directories,
   license and schema XML.
7. Keep GJS and Shell tests separate from real hardware checks; state limitations.

Shexli 0.2.1 reported zero findings, errors and warnings on the package. The
absence of `manual_review` does not remove the need for human subprocess
review. The only runtime execution is the official read-only CLI, with fixed
arguments, limits, timeout and reaping. Configurable constructor arguments in
the provider exist for tests; they are not exposed through preferences or menu
input. No `sh -c` or interpolation of device names.
