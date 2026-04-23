# Issue #199: Add ClusterQueue and Queue Metrics

**Summary**: Add ClusterQueue and Queue Metrics

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/199

**Last updated**: 2022-08-09T18:27:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-04-09T23:10:53Z
- **Updated**: 2022-08-09T18:27:50Z
- **Closed**: 2022-08-09T17:36:37Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/ux`, `kind/productionization`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 10

## Description

**What would you like to be added**:

Metrics to track:
1. [x] Queue/ClusterQueue pending workloads (gauge) 
2. [x] Queue/ClusterQueue admitted workloads (gauge) 
3. [x] Admission cycle latency (histogram)
4. [x] Workload waiting time in the queue (histogram)



what else?

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-26T08:36:01Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-26T13:48:13Z

Oops, I forgot to put my name on this. I was already working on it. I hope you don't mind @kerthcet?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-26T14:03:36Z

Plz go ahead.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-26T14:13:14Z

/unassign
/assign @alculquicondor

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-26T14:19:53Z

I have nearly finished the `Queue/ClusterQueue pending workloads (gauge)`, some tests left. if you haven't work on this one, I can finish this one to prevent redundant works. If not, please forget what I said.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-04-26T14:42:46Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-07T09:16:48Z

Aldo, I guess the following represents progress on this issue, correct?

1. [x] Queue/ClusterQueue pending workloads (gauge) 
2. [x] Admission cycle latency (histogram)
3. [x] Queue/ClusterQueue admitted workloads (gauge) 
4. [ ] Workload waiting time in the queue (histogram)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-09T16:54:05Z

correct, thanks

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-07-18T13:44:58Z

@alculquicondor are you planning to add workload waiting time?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-18T14:23:05Z

yes. But feel free to take that if you have time this week. Otherwise I'll do it next week.
