# Issue #9801: Define Logging Levels

**Summary**: Define Logging Levels

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9801

**Last updated**: 2026-10-08T16:54:21Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2026-03-11T10:49:30Z
- **Updated**: 2026-10-08T16:54:21Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 5

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-08-06T08:49:40Z

We recently observed that some log levels are performance bottlenecks for hot loops at V4 like logAdmissionAttemptIfVerbose.

I'm not yet sure we need to change this V4 log, but let me see if we can have a more structured approach and recommendations to users. 

/assign
Assigning tentatively to work as pet project, but let me know if someone has cycles to focus on that more. I will also welcome folks to brainstorm.

cc @Singularity23x0 @dkaluza @kshalot @olekzabl

### Comment by [@mimowo](https://github.com/mimowo) — 2026-10-08T16:54:13Z

/reopen
i will continue on migration

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-10-08T16:54:21Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9801#issuecomment-6064837942):

>/reopen
>i will continue on migration


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
