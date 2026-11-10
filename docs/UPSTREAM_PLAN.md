# Plan for opening a device page in OpenLogi

Agreed on October 28, 2026: steps 1, 2 and 3 run in sequence; the tests in step 3
accompany the PR from step 2.

## 1. Agree on the interface through an issue

- [ ] Recheck the current upstream branch and search for equivalent issues/PRs.
- [ ] Prepare a short issue describing the GNOME companion use case, opening a
  device page from external apps and the limitation in the reviewed 0.8.18 release.
- [ ] Propose a minimal public action consistent with upstream mechanisms;
  agree on transport, device identity and errors before implementation.
- [ ] Publish the issue when requested by the user and wait for maintainer
  discussion. This project has not published an issue.

## 2. Prepare a small PR

- [ ] Work in a separate OpenLogi checkout on the current branch.
- [ ] Implement only GUI launch/activation and device selection through the
  agreed interface, without unrelated changes.
- [ ] Handle forwarding to an existing instance, cold start and inventory not ready.
- [ ] Document the contract, limitations and error behavior.
- [ ] Prepare the description and test results; publish the PR when requested.

## 3. Include tests in the PR

- [ ] GUI closed: launch, wait for inventory and select the correct device.
- [ ] GUI open: select and focus without duplicate windows or processes.
- [ ] GUI minimized: restore, focus and select.
- [ ] Missing or ambiguous identity, or absent/offline device: return an explicit
  error without selecting a different device.
- [ ] Scanning/unavailable inventory and closely spaced requests.
- [ ] Verify on real Linux, with relevant automated tests and upstream checks.
- [ ] Integrate the companion only after checking the API in the release that
  ships it. Until then, **Show OpenLogi window** opens the general window and
  device rows remain read-only.

## Status

Plan recorded. No issue or PR sent by this project; no upstream changes made.
The November 10, 2026 review of v0.9.0 found the same limitation and an existing
[equivalent issue, #1375](https://github.com/AprilNEA/OpenLogi/issues/1375).
Recheck that request before opening another one. The initial technical proposal,
remaining limitations and reminder are in [OPEN_ITEMS.md](OPEN_ITEMS.md).
