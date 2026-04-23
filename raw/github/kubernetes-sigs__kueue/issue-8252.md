# Issue #8252: [Discussion] Deprecate External Frameworks in MK config

**Summary**: [Discussion] Deprecate External Frameworks in MK config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8252

**Last updated**: 2025-12-16T14:59:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-12-15T20:47:14Z
- **Updated**: 2025-12-16T14:59:03Z
- **Closed**: 2025-12-16T14:59:02Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 3

## Description

Hi.

I'm looking at how to enable MK with external frameworks. I notice that we have a config api for external frameworks in MK. 

I am curious why we would have different integrations specified in config/integrations/frameworks and mk/integrations.

It would make the most sense to me that MK supports all the workloads specified in integrations/framework. So I think it would be ideal if there was no MK configuration for external frameworks.

And when a user specifies the external frameworks in config/integrations then it should automatically be enabled for MK.

Otherwise I worry that we hit an unecessary bug where someone can configure the hub cluster for external frameworks but the spoke clusters do not have this enabled. So in this case, I would think that the MK environment for external frameworks would not be fully functional.

cc @khrm @mimowo

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T08:32:23Z

This is actually done by purpose. It is possible that some external frameworks don't support MultiKueue. To support MultiKueue the external framework needs to have the `spec.managedBy` which is not guaranteed. 

Also, in the future we are planning to expand that configuration to introduce external controllers for syncing MultiKueue Jobs, and only a small subset of them will use it.

> Otherwise I worry that we hit an unecessary bug where someone can configure the hub cluster for external frameworks but the spoke clusters do not have this enabled.

Yeah, syncing configuration for MultiKueue is a challange overall probably not limited to just this potential issue. Maybe we can mitigate it better with error messages.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-16T14:58:57Z

Sounds good.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-16T14:59:03Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8252#issuecomment-3660985189):

>Sounds good.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
