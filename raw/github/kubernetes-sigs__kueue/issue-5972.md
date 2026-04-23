# Issue #5972: The docs script blocks updates to English docs when not in sync with Chinese

**Summary**: The docs script blocks updates to English docs when not in sync with Chinese

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5972

**Last updated**: 2025-07-14T20:10:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-14T13:55:41Z
- **Updated**: 2025-07-14T20:10:28Z
- **Closed**: 2025-07-14T14:42:26Z
- **Labels**: `kind/bug`, `kind/documentation`, `area/localization`
- **Assignees**: _none_
- **Comments**: 4

## Description


**What happened**:

The script added in https://github.com/kubernetes-sigs/kueue/pull/5798 blocks PRs updating documentation in English, such as https://github.com/kubernetes-sigs/kueue/pull/4444

**What you expected to happen**:

Documentation updates to English are not blocked by the script. The script can be used to block translation, or just for local checking what is not in sync.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-14T13:55:52Z

cc @samzong @mbobrovskyi @kannon92

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-14T13:57:11Z

/kind documentation
/area localization

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-14T13:58:18Z

I don't think that we should check English and other languages synchronization in CI.
When we approve other languages, we approve the idea because it does not bring a massive additional effort.

We should not perform the scripts in CI, but I'm ok with keeping the script for local execution.

### Comment by [@samzong](https://github.com/samzong) — 2025-07-14T20:10:27Z

Thanks to @tenzen-y for quickly fixing this issue. Apologies for introducing an unexpected check that impacted everyone’s work. 

This aligns with my earlier expectation: it should be a script without blocking make verify, or we shouldn’t use exit 1.

(play with my kid and didn’t check email.)
