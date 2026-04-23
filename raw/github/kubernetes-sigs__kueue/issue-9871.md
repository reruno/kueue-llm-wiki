# Issue #9871: JobUID label is missing on Workloads for StatefulSets

**Summary**: JobUID label is missing on Workloads for StatefulSets

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9871

**Last updated**: 2026-03-16T15:25:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-13T14:59:55Z
- **Updated**: 2026-03-16T15:25:43Z
- **Closed**: 2026-03-16T15:25:42Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

**What happened**:

The kueue.x-k8s.io/job-uid label is missing on Workloads created for StatefulSets. 

This label is important to quickly find the Job owning the Workload, this was intention of the old issue https://github.com/kubernetes-sigs/kueue/issues/992

Let's also check LWS and Pod integration.

**What you expected to happen**:

The Job-uid label is present on Workloads regardless of the Job type. 

**How to reproduce it (as minimally and precisely as possible)**:

Create STS in 0.16.3 (latest)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:00:11Z

cc @tenzen-y who actually encountered the issue.

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-13T15:00:50Z

/assign @yaroslava-serdiuk 
tenatively, who is looking for a warm up issue

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T15:06:49Z

Thank you for opening this up!
Let me leave the actual Workload information for each Kueue version

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-13T15:07:44Z

As shown the below, all recent released versions don't add such labels: 
 
- v0.16.1

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  annotations:
    kueue.x-k8s.io/is-group-workload: "true"
  creationTimestamp: "2026-03-13T13:46:21Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  ownerReferences:
  - apiVersion: v1
    kind: Pod
    name: tz-test-0161-0
    uid: cef04843-b289-4738-a370-d2237f9f5e7d
  - apiVersion: apps/v1
    kind: StatefulSet
    name: tz-test-0161
    uid: def85174-ddd0-4cb0-8c4f-886ff9a6e11f
```

- v0.16.2

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  annotations:
    kueue.x-k8s.io/is-group-workload: "true"
    kueue.x-k8s.io/job-owner-gvk: apps/v1, Kind=StatefulSet
    kueue.x-k8s.io/job-owner-name: tz-test-0162
  ownerReferences:
  - apiVersion: apps/v1
    kind: StatefulSet
    name: tz-test-0162
    uid: 5bde7109-d024-40ec-8192-3bfc1597c297
  - apiVersion: v1
    kind: Pod
    name: tz-test-0162-0
    uid: 02100a29-fc40-4ee0-8d43-8c5afa9777fb
```

- v0.16.3

```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Workload
metadata:
  annotations:
    kueue.x-k8s.io/is-group-workload: "true"
    kueue.x-k8s.io/job-owner-gvk: apps/v1, Kind=StatefulSet
    kueue.x-k8s.io/job-owner-name: tz-test-0163
  ownerReferences:
  - apiVersion: apps/v1
    kind: StatefulSet
    name: tz-test-0163
    uid: ce5e6229-89dc-4c2b-b097-3e5818fa7d91
  - apiVersion: v1
    kind: Pod
    name: tz-test-0163-0
    uid: 5b9e925d-d134-4119-a706-79515425576f
```

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-16T10:21:10Z

Hmm. It looks like we have the same in LWS. Previously we used pod-groups and didn’t add it, but now I think we can add it.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-16T12:53:32Z

/unassign @yaroslava-serdiuk
I think she hasnt made much progress yet as i see she is ooo today.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-16T13:00:38Z

/assign
