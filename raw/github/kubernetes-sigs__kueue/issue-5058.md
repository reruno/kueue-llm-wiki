# Issue #5058: PropagateResourceRequests always generates diff on CPU

**Summary**: PropagateResourceRequests always generates diff on CPU

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5058

**Last updated**: 2025-04-26T14:03:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexeldeib](https://github.com/alexeldeib)
- **Created**: 2025-04-21T16:01:23Z
- **Updated**: 2025-04-26T14:03:25Z
- **Closed**: 2025-04-26T14:03:25Z
- **Labels**: `kind/bug`
- **Assignees**: [@alexeldeib](https://github.com/alexeldeib)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


PropagateResourceRequests always generates a diff on CPU apparently, which was spamming reconciles

from added logging
```
Mismatch in resource requests for workload main: main != main, OR amounts: true
resources: v1.ResourceList{"cpu":resource.Quantity{i:resource.int64Amount{value:10, scale:0}, d:resource.infDecAmount{Dec:(*inf.Dec)(nil)}, s:"10", Format:"DecimalSI"}}
  rlList: v1.ResourceList{"cpu":resource.Quantity{i:resource.int64Amount{value:10000, scale:-3}, d:resource.infDecAmount{Dec:(*inf.Dec)(nil)}, s:"", Format:"DecimalSI"}}
```
okay, integral CPU vs millicpu

https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/resources/requests.go#L102-L104

let's try milli cpu with a non-integral value
```
resources: v1.ResourceList{"cpu":resource.Quantity{i:resource.int64Amount{value:9001, scale:-3}, d:resource.infDecAmount{Dec:(*inf.Dec)(nil)}, s:"9001m", Format:"DecimalSI"}}
  rlList: v1.ResourceList{"cpu":resource.Quantity{i:resource.int64Amount{value:9001, scale:-3}, d:resource.infDecAmount{Dec:(*inf.Dec)(nil)}, s:"", Format:"DecimalSI"}}
```
oh...the internally generated private string field differs during reflection comparison...because maps.Equal just calls direct struct equality for the entries https://cs.opensource.google/go/go/+/refs/tags/go1.24.2:src/maps/maps.go;l=22

switching to cmp.Equal resolves that


**What happened**:

they are not equal

**What you expected to happen**:

equality should pass for semantically equal values

**How to reproduce it (as minimally and precisely as possible)**:

Create an integration test with workloads blocked on CPU quota using integral CPU requests (e.g. "10"), it will generate a diff. Add logs in code to see the value of private fields that are different.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-21T20:08:51Z

Thank you for reporting this. Could you point out the place where you fase the noisy logs? Or could you pointing out the noisy log messages?

> switching to cmp.Equal resolves that

The `cmp.Equal` has high computing costs. So in k/k, actually, it is prohibited from being used in production code.
So, I guess we should use Quantity Equal function someting like

```go
var a, b resource.Quantity
a.Equal(b)
```

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2025-04-21T21:46:30Z

oh sorry! the logs are my addition inside the func -- I was seeing [this func](https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/pkg/scheduler/scheduler.go#L657) return true when I expected no diff, so I added my own debug logs to validate

```diff
diff --git a/pkg/workload/workload.go b/pkg/workload/workload.go
index e646c9244..f2706b2f2 100644
--- a/pkg/workload/workload.go
+++ b/pkg/workload/workload.go
@@ -654,6 +654,8 @@ func PropagateResourceRequests(w *kueue.Workload, info *Info) bool {
                for idx := range w.Status.ResourceRequests {
                        if w.Status.ResourceRequests[idx].Name != info.TotalRequests[idx].Name ||
                                !cmp.Equal(w.Status.ResourceRequests[idx].Resources, info.TotalRequests[idx].Requests.ToResourceList()) {
+                               fmt.Printf("Mismatch in resource requests for workload %s: %s != %s, OR amounts: %t\n", w.Status.ResourceRequests[idx].Name, w.Status.ResourceRequests[idx].Name, info.TotalRequests[idx].Name, !maps.Equal(w.Status.ResourceRequests[idx].Resources, info.TotalRequests[idx].Requests.ToResourceList()))
+                               fmt.Printf("resources: %#+v\n  rlList: %#+v\n", w.Status.ResourceRequests[idx].Resources, info.TotalRequests[idx].Requests.ToResourceList())
                                match = false
                                break
                        }
@@ -661,6 +663,8 @@ func PropagateResourceRequests(w *kueue.Workload, info *Info) bool {
                if match {
                        return false
                }
+       } else {
+               fmt.Printf("Mismatch in resource requests for workload %s: %d != %d\n", w.Name, len(w.Status.ResourceRequests), len(info.TotalRequests))
        }
 
        res := make([]kueue.PodSetRequest, len(info.TotalRequests))
```

> The cmp.Equal has high computing costs. So in k/k, actually, it is prohibited from being used in production code.
So, I guess we should use Quantity Equal function someting like

TIL, makes sense

### Comment by [@alexeldeib](https://github.com/alexeldeib) — 2025-04-21T22:07:43Z

/assign

might roll a fix into https://github.com/kubernetes-sigs/kueue/pull/4935 but will tackle it either way

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-24T08:22:37Z

cc @gabesaba
