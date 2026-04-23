# Issue #2791: Mention in the installation docs a command for Kueue to be ready

**Summary**: Mention in the installation docs a command for Kueue to be ready

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2791

**Last updated**: 2024-08-07T14:42:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-07T11:20:40Z
- **Updated**: 2024-08-07T14:42:56Z
- **Closed**: 2024-08-07T14:08:52Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What would you like to be added**:

A note in the installation docs to say:

To wait for Kueue to be fully available, run:
```
kubectl wait deploy/kueue-controller-manager -nkueue-system --for=condition=available --timeout=5m
```

Maybe this could even be part of the installation command.

**Why is this needed**:

Some users hit the issue as they start tutorial steps without waiting for Kueue to be fully ready.

The tutorial steps fail at different points, because webhooks are not ready, and result in confusion, and on-call churn.

Some users of Kubernetes don't know how to wait for Kueue to be fully available, and they build scripts without waiting.

**Completion requirements**:

- [x] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-07T11:21:16Z

/cc @tenzen-y @trasc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-07T11:53:06Z

/assign
