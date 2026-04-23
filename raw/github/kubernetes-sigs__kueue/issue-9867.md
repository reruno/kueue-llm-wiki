# Issue #9867: Release automation: submit the PR to update only changelog for the N-2 patch

**Summary**: Release automation: submit the PR to update only changelog for the N-2 patch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9867

**Last updated**: 2026-03-17T06:00:27Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-13T13:41:10Z
- **Updated**: 2026-03-17T06:00:27Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

**What would you like to be added**:

I would like to extend our release automation to generate and submit PR for the N-2 patch release.

Basically a PR like this https://github.com/kubernetes-sigs/kueue/pull/9865

And reference in the release issue 

<img width="882" height="300" alt="Image" src="https://github.com/user-attachments/assets/9a04b60a-807b-4331-a209-d85d7d39162f" />

Maybe it could be `./hack/releasing/prepare_pull.sh --target changelog $VERSION`

Or we could also rename `--target` to `--mode`, but no need.

**Why is this needed**:

To save some time when doing the N-2 release.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T13:41:20Z

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T13:41:25Z

cc @tenzen-y @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T13:55:40Z

I fully support this request 👍

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-17T06:00:24Z

/assign
