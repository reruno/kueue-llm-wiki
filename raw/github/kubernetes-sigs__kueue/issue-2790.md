# Issue #2790: [kueuectl] the kueuectl examples don't work as copy-paste

**Summary**: [kueuectl] the kueuectl examples don't work as copy-paste

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2790

**Last updated**: 2024-08-08T07:31:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-07T10:42:32Z
- **Updated**: 2024-08-08T07:31:28Z
- **Closed**: 2024-08-08T07:31:28Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

**What happened**:

I create a CQ with the command according to help:
```
kubectl-kueue create clusterqueue my-cluster-queue --nominal-quota=alpha:cpu=9;memory=36Gi
```
but it ignores `memory=36Gi` without any warning / error.

This leads to subtle problems as users of `kueuectl` would often not inspect the yaml.

**What you expected to happen**:

I would expect the examples to work as copy-paste.

**How to reproduce it (as minimally and precisely as possible)**:

Run example from `kueuectl create cq --help`

**Anything else we need to know?**:

I think we could consider updating the examples to escape ";",  or consider other delimiter choices which don't require escaping.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-07T10:42:43Z

/cc @trasc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-07T10:47:57Z

@mimowo Try to use quotes:

```bash
kubectl-kueue create clusterqueue my-cluster-queue --nominal-quota="alpha:cpu=9;memory=36Gi"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-07T10:49:58Z

> @mimowo Try to use quotes:

This works, it would be great to adjust the help examples accordingly

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-07T10:51:35Z

/assign
