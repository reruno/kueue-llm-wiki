# Issue #5313: Workloads requesting TAS cannot run via MultiKueue

**Summary**: Workloads requesting TAS cannot run via MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5313

**Last updated**: 2025-11-07T09:34:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-22T14:18:49Z
- **Updated**: 2025-11-07T09:34:50Z
- **Closed**: 2025-11-07T09:12:56Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg), [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 10

## Description

**What happened**:

We cannot run workloads requesting TAS via MultiKueue. This is problematic, because TAS workloads have dedicated annotations like "preferred: rack". However workloads with such annotations only match TAS ResourceFlavors.

**What you expected to happen**:

We can configure Kueue to schedule workloads requesting TAS via MultiKueue. They should execute on the workers, but we should have a way to run them.

The natural approach is to configure TAS RF on the management cluster (both on manager and worker). 

**How to reproduce it (as minimally and precisely as possible)**:

1. Setup MultiKueue and configure CQ using TAS ResourceFlavor. The CQ will get deactivated immediately because of the soft validation we have: https://github.com/kubernetes-sigs/kueue/blob/4bfc9a0ec7d6d32b8b29eeba9baf7b42cfdf3508/pkg/cache/clusterqueue.go#L243-L246

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-22T14:19:37Z

/assign @IrvingMg 
who already started to look into running TAS workloads over MultiKueue and hit the issue.

cc @mwysokin @mwielgus @tenzen-y @mszadkow

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-05-28T02:28:35Z

Hey, what's the current status with multiKueue + TAS? No updates on website I believe.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-28T03:26:58Z

> Hey, what's the current status with multiKueue + TAS? No updates on website I believe.

As described in this issue, TAS+MultiKueue does not work well even though you use Kueue v0.12.0.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-28T03:28:05Z

As a feature stage, TAS is alpha, and MultiKueue is Beta. However, we do not have any feature stage against that combination.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2025-05-28T04:02:33Z

Thanks.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-06-20T17:08:48Z

/assign @vladikkuzn

### Comment by [@CecileRobertMichon](https://github.com/CecileRobertMichon) — 2025-09-02T16:44:23Z

Very interested in this feature

### Comment by [@jessicaxiejw](https://github.com/jessicaxiejw) — 2025-09-02T16:49:10Z

same here, would be nice to have the feature

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T09:25:15Z

@jessicaxiejw @CecileRobertMichon @mwysokin I just merged the feature, and it will be released as part of 0.15, planned tentatively for 17th November, but may slit up to 2 weeks.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-07T09:34:43Z

I also opened a task to document it: https://github.com/kubernetes-sigs/kueue/issues/7579
