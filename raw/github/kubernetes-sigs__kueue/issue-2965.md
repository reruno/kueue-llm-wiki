# Issue #2965: False Positive Unused golangci-lint

**Summary**: False Positive Unused golangci-lint

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2965

**Last updated**: 2024-09-16T09:05:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-09-03T08:36:53Z
- **Updated**: 2024-09-16T09:05:16Z
- **Closed**: 2024-09-16T09:05:16Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

**What would you like to be cleaned**:
The linter yielded several false-positive unused for the file `pkg/hierarchy/cohort.go` in #2939. As a short-term workaround, I added a rule in `.golangci.yaml`

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-03T10:15:16Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-03T10:15:20Z

How did you catch it? From my side it works fine.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-03T10:24:51Z

Looks like I found.

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2939/pull-kueue-verify-main/1829519586400145408
