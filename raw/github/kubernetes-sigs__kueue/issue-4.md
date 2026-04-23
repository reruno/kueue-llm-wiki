# Issue #4: Add NamespaceSelector to ClusterQueue

**Summary**: Add NamespaceSelector to ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4

**Last updated**: 2022-03-08T19:20:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:06:07Z
- **Updated**: 2022-03-08T19:20:50Z
- **Closed**: 2022-03-08T19:20:50Z
- **Labels**: `kind/feature`, `priority/important-soon`, `size/M`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 6

## Description

NamespaceSelector in capacity allows controlling which namespaces are allowed to use the capacity.

/kind feature

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-18T13:42:20Z

/size M

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-19T03:53:04Z

Does is mean we need a validating webhook?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-02-19T12:22:37Z

> Does is mean we need a validating webhook?

No not a webhook, kueue itself should not consider assigning capacity to queue in not selected namespcaes. We also need to produce events and perhaps update queue status to indicate whether the capacity a queue is pointing to is allowed.

### Comment by [@jiwq](https://github.com/jiwq) — 2022-02-23T15:25:23Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-02T18:44:34Z

/unassign @jiwq 
/assign

we need to do this soon, @jiwq please feel free to pick other issues when you have time.

### Comment by [@jiwq](https://github.com/jiwq) — 2022-03-07T15:46:40Z

@ahg-g Sorry to the late response. I'll continue other work when I have time and submit ASAP. Thanks for your help!
