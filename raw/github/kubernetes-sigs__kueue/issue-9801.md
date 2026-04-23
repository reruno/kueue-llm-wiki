# Issue #9801: Define Logging Levels

**Summary**: Define Logging Levels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9801

**Last updated**: 2026-03-11T10:58:13Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-03-11T10:49:30Z
- **Updated**: 2026-03-11T10:58:13Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What would you like to be added**:
I would like to define what we will log at each of our log levels.

**Why is this needed**:
Right now, we do this based on our best judgement. It would be nice to have some rubric to refer to.

This would accomplish 3 goals:
1) increase signal to noise ratio at lower log levels
2) make it more clear to Kueue users what to expect at each log level
3) make it more clear to developers what level to add a new log line at

**Completion requirements**:
- [ ] rubric for developers
- [ ] documentation for kueue users
- [ ] cleanup existing logs to match this rubric

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T10:58:13Z

I think for the basis we could use https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/logging.md
