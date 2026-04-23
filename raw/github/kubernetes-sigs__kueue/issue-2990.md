# Issue #2990: Visibility Test Flake

**Summary**: Visibility Test Flake

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2990

**Last updated**: 2024-09-05T16:33:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-09-05T10:04:13Z
- **Updated**: 2024-09-05T16:33:59Z
- **Closed**: 2024-09-05T16:33:59Z
- **Labels**: `kind/flake`, `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2989/pull-kueue-test-e2e-main-1-31/1831630396710719488

```
Summarizing 1 Failure:
  [FAIL] Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job [It] Should allow fetching information about pending workloads in ClusterQueue
  /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:186
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-05T10:06:20Z

/kind flake
/cc @PBundyra 
(as the feature owner)
/cc @mbobrovskyi @trasc 
in case you have capacity to look at it

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-05T13:40:56Z

/assign
