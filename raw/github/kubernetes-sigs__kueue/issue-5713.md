# Issue #5713: ☂️ Release v0.13.0 requirements

**Summary**: ☂️ Release v0.13.0 requirements

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5713

**Last updated**: 2025-07-07T07:48:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-23T09:37:34Z
- **Updated**: 2025-07-07T07:48:55Z
- **Closed**: 2025-07-07T07:48:54Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 7

## Description

We are targeting the release on 14th July.

### Priorities

- https://github.com/kubernetes-sigs/kueue/issues/5505
- https://github.com/kubernetes-sigs/kueue/issues/5439

### Nice-to-haves

- https://github.com/kubernetes-sigs/kueue/issues/2941
- https://github.com/kubernetes-sigs/kueue/issues/5712
- https://github.com/kubernetes-sigs/kueue/issues/4531
- https://github.com/kubernetes-sigs/kueue/issues/5313
- https://github.com/kubernetes-sigs/kueue/issues/5704
- https://github.com/kubernetes-sigs/kueue/issues/5141
- https://github.com/kubernetes-sigs/kueue/issues/5528
- https://github.com/kubernetes-sigs/kueue/issues/1833
- https://github.com/kubernetes-sigs/kueue/issues/5424
- https://github.com/kubernetes-sigs/kueue/issues/5719
- https://github.com/kubernetes-sigs/kueue/issues/5260

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T09:41:02Z

Hi folks, it is less than a month since the planned release so let me post the planned features so that we can prioritize reviews.

cc @tenzen-y @dgrove-oss @gabesaba @mwielgus @mwysokin

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-23T19:47:50Z

Is there any information on when TAS can be promoted to beta?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-24T05:36:46Z

Good question. We have this issue https://github.com/kubernetes-sigs/kueue/issues/3450 but it seems that all points there are already addressed. So from the perspective of what was planned initially we could do it even in 0.13.

However we have some ongoing work like 2level scheduling for JobSet and LWS, or node hot swap, and so we may prefer to wait for feedback and graduate in 0.14. 

@kannon92 do you have any expectations here from your side?

cc @mwysokin @mwielgus in case you have an opinion here.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-24T10:34:50Z

I don’t have any expectations. I just wasn’t sure when that would happen.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-24T10:40:39Z

I'm with @mimowo (Beta in 0.14)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-07T07:48:49Z

/close 
To continue tracking the release progress in https://github.com/kubernetes-sigs/kueue/issues/5886

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-07T07:48:55Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5713#issuecomment-3043848217):

>/close 
>To continue tracking the release progress in https://github.com/kubernetes-sigs/kueue/issues/5886


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
