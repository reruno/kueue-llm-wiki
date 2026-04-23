# Issue #2075: [scalability] Do not archive the binary artifacts (scalability runner and minikueue)

**Summary**: [scalability] Do not archive the binary artifacts (scalability runner and minikueue)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2075

**Last updated**: 2024-04-29T15:05:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-26T08:52:16Z
- **Updated**: 2024-04-29T15:05:52Z
- **Closed**: 2024-04-29T15:05:52Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

**What would you like to be cleaned**:

The artifacts are archived and weigh 100MB together [example](https://gcsweb.k8s.io/gcs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2061/pull-kueue-test-scheduling-perf-main/1783766177533661184/artifacts/): 
![image](https://github.com/kubernetes-sigs/kueue/assets/10359181/350609c6-159f-4350-bc40-ef40cb77967f)

**Why is this needed**:

Binaries for perf testing weigh a lot, and they are unlikely to be downloaded.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T08:52:27Z

/assign @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-26T11:54:51Z

/assign
