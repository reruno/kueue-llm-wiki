# Issue #1159: Docs on using queue visibility feature for cluster queues

**Summary**: Docs on using queue visibility feature for cluster queues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1159

**Last updated**: 2023-09-29T16:40:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-09-25T08:21:09Z
- **Updated**: 2023-09-29T16:40:45Z
- **Closed**: 2023-09-29T16:40:45Z
- **Labels**: `kind/documentation`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 7

## Description

A new docs page for the feature: https://github.com/kubernetes-sigs/kueue/issues/168

I think it could go under the tasks page: https://kueue.sigs.k8s.io/docs/tasks/, say "Monitor pending workloads in queue status". 

This could focus on the "done" part for now - the cluster queues. It would be extended for local queues in the future.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-25T08:21:20Z

FYI @stuton

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-25T08:21:52Z

FYI @tenzen-y @alculquicondor 
For thoughts

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-25T08:22:46Z

xref: https://github.com/kubernetes-sigs/kueue/issues/168

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-25T08:41:27Z

How about "Monitor pending workloads"? We use `queue` as a shorter name for localQueue. So, it would be better to avoid using `queue` as a part of the title.

https://github.com/kubernetes-sigs/kueue/blob/4aea01deffc41a0c190df6608000ba2f6ab9a9c9/apis/kueue/v1beta1/localqueue_types.go#L95

### Comment by [@mimowo](https://github.com/mimowo) — 2023-09-25T11:46:16Z

> How about "Monitor pending workloads"? 

sgtm

### Comment by [@stuton](https://github.com/stuton) — 2023-09-25T13:44:16Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-26T02:57:16Z

/kind documentation
