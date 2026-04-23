# Issue #94: Migrate GINKO framework to V2

**Summary**: Migrate GINKO framework to V2

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/94

**Last updated**: 2022-03-09T22:56:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Created**: 2022-03-04T19:48:38Z
- **Updated**: 2022-03-09T22:56:02Z
- **Closed**: 2022-03-09T22:56:02Z
- **Labels**: `priority/backlog`
- **Assignees**: _none_
- **Comments**: 0

## Description

Spin off https://github.com/kubernetes-sigs/kueue/pull/89#discussion_r819686679

We should consider upgrading ginko to v2 as stated in their logs 

-  Learn more at: https://github.com/onsi/ginkgo/blob/ver2/docs/MIGRATING_TO_V2.md#removed-custom-reporters

for now we can work around by using `ACK_GINKGO_DEPRECATIONS=1.16.5` env var when running the integration tests
