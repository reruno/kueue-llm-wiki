# Issue #9801: Define Logging Levels

**Summary**: Define Logging Levels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9801

**Last updated**: 2026-04-30T14:31:20Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-03-11T10:49:30Z
- **Updated**: 2026-04-30T14:31:20Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

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

### Comment by [@dkaluza](https://github.com/dkaluza) — 2026-04-30T14:01:41Z

In my opinion it would be also good to standardize which fields/keys will always be present in logs and what is their meaning (It can be a separate effort). This can give us sort of contract that can be used in further integrations, e.g. filtering in the log sink. 

Right now it is hard to tell, for example, how is always log level defined in the logs or if it will stay defined in the same way in the future. Especially that mentioned sig-instrumentation is defining it as "v" key in json format, and I haven't seen it in some of our info logs.
