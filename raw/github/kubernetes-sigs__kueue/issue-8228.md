# Issue #8228: Run A Kubernetes Job  do   not  need to set  "suspend" == true

**Summary**: Run A Kubernetes Job  do   not  need to set  "suspend" == true

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8228

**Last updated**: 2025-12-18T10:01:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@zwbdzb](https://github.com/zwbdzb)
- **Created**: 2025-12-15T03:58:13Z
- **Updated**: 2025-12-18T10:01:20Z
- **Closed**: 2025-12-18T10:01:20Z
- **Labels**: _none_
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 4

## Description

The [document](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/) says  define the job coontrolled by the kueue: 
 You should create the Job in a [suspended state](https://kubernetes.io/docs/concepts/workloads/controllers/job/#suspending-a-job), as Kueue will decide when it’s the best time to start the Job.

 but most jobs created are not suspended by default, I believe this action is intrusive。
 So I verified the effect without this config “suspend: true ”，It has also taken effect, under the control of kueue.  maybe  the document should  remove the "suspend:true" requirement.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-15T04:36:51Z

Good point.

I think we could remove that bullet point.
WDYT @mimowo @tenzen-y?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-15T17:24:12Z

@zwbdzb would you like to open up a PR dropping that bullet point?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T17:28:19Z

Yes, I totally agree. I think this was added to the documenation long time ago, maybe before Kueue injected "suspend" in webhook. In any case, this is not necessary indeed.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-18T08:08:22Z

/assign
