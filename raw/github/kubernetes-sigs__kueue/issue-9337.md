# Issue #9337: Improve scheduling performance by caching nodes

**Summary**: Improve scheduling performance by caching nodes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9337

**Last updated**: 2026-03-10T11:47:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@j-skiba](https://github.com/j-skiba)
- **Created**: 2026-02-18T10:51:53Z
- **Updated**: 2026-03-10T11:47:13Z
- **Closed**: 2026-03-10T11:47:13Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

**What would you like to be added**:

I ran performance tests a few times with bigger node sets than the [current one](https://github.com/kubernetes-sigs/kueue/blob/main/test/performance/scheduler/configs/tas/generator.yaml) as currently we support 60k nodes in TAS.

It seems like for bigger clusters the biggest bottleneck for the scheduling are GC procedures and [node listing](https://github.com/kubernetes-sigs/kueue/blob/321e6e909eaa095e65906653396f22ccad2b2033/pkg/cache/scheduler/tas_flavor.go#L117). As we approach bigger number of nodes the GC procedures consume more time (pictures attached) given complexity of node object.

We could improve scheduling time by caching nodes. It seems like we utilize just a few fields from the node object: `Name`, `Allocatable`, `Labels` and `Taints` except for [here](https://github.com/kubernetes-sigs/kueue/blob/ffe623479f67eb689af8e16e61f979e8ae42f8db/pkg/cache/scheduler/tas_flavor_snapshot.go#L1398) where we match node affinity and we need a node object - here maybe we could "recreate" a node object manually based on the stored `Name` and `Labels` and use it for comparison, I'm not sure if that's fine.

so I would propose a cached node object to look like this:
```go
type NodeInfo struct {
	// Name holds the node's name, used to evaluate node affinity.
	Name string

	// Allocatable capacity from Status.Allocatable.
	Allocatable corev1.ResourceList

	// Labels are used to match Topology levels and NodeSelectors.
	Labels map[string]string

	// Taints are used to check tolerations.
	Taints []corev1.Taint
}
```

I ran 4 scenarios with cpu and heap profiling:

[the current configuration](https://github.com/kubernetes-sigs/kueue/blob/main/test/performance/scheduler/configs/tas/generator.yaml):
- cpu
<img width="2558" height="665" alt="Image" src="https://github.com/user-attachments/assets/1c19a3cc-1461-49de-a1d0-71b2422dd0ee" />
- heap alloc_objects
<img width="2554" height="1046" alt="Image" src="https://github.com/user-attachments/assets/1c0a60fc-b59b-459b-a12a-2fd8147ae374" />



[2k nodes configuration](https://gist.github.com/j-skiba/0764c6d1cec7f32bc0d08b88ccaffd31):
- cpu
<img width="2558" height="627" alt="Image" src="https://github.com/user-attachments/assets/adfaf91a-babd-447c-82da-f338d5a0a86e" />
- heap alloc_objects
<img width="2558" height="678" alt="Image" src="https://github.com/user-attachments/assets/16c4ff42-7545-4e9f-8fba-281e7df64359" />



[20k nodes configuration](https://gist.github.com/j-skiba/f53a74e94aafd67421134721f7e62ff4):
- cpu
<img width="2559" height="639" alt="Image" src="https://github.com/user-attachments/assets/d77da125-7f5b-4cb9-907d-8aa752280d44" />
- heap alloc_objects
<img width="2560" height="458" alt="Image" src="https://github.com/user-attachments/assets/43740992-8f74-4dc4-a479-1695ee66c69a" />



[60k nodes configuration](https://gist.github.com/j-skiba/6b397714dc445ecb3ef99157dc7230f1):
- cpu
<img width="2560" height="606" alt="Image" src="https://github.com/user-attachments/assets/357de582-2a10-451d-a225-d1a8f32a181d" />
- heap alloc_objects
<img width="2560" height="441" alt="Image" src="https://github.com/user-attachments/assets/caf45ff7-c39c-44e7-ae1e-5dc70e9c96f1" />

Similar issues: https://github.com/kubernetes-sigs/kueue/issues/8449

**Why is this needed**:

Improvement of scheduling performance for bigger scale clusters.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@j-skiba](https://github.com/j-skiba) — 2026-02-18T11:02:53Z

the results are from `make run-tas-performance-scheduler`

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-18T11:03:11Z

This is a great finding! Thank you 👍

### Comment by [@mykysha](https://github.com/mykysha) — 2026-03-04T12:17:44Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-05T06:32:55Z

/unassign @mykysha 
/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T18:59:06Z

/priority important-soon
