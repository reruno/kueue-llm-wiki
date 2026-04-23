# Issue #8634: TAS: Verify assigned rank in ungater UTs

**Summary**: TAS: Verify assigned rank in ungater UTs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8634

**Last updated**: 2026-04-14T13:06:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-16T12:13:12Z
- **Updated**: 2026-04-14T13:06:42Z
- **Closed**: 2026-04-14T13:06:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@omerap12](https://github.com/omerap12)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I'd like to verify if scheduled Pods get proper nodes based on rank-ordering in 

https://github.com/kubernetes-sigs/kueue/blob/0880bb125aada2662cb298d6910cdce30a7a9c1a/pkg/controller/tas/topology_ungater_test.go#L71

**Why is this needed**:
Currently, TestReconcile deson't care which Pod gets which assignment during UTs as described in the following:

https://github.com/kubernetes-sigs/kueue/blob/0880bb125aada2662cb298d6910cdce30a7a9c1a/pkg/controller/tas/topology_ungater_test.go#L72-L81

It just verifies the number of assignments. However, in the case of rank-ordering TAS, the actual assignmen is matter.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T12:13:56Z

@mimowo, I don't remember the reason why we don't verify the actual assignment for rank-ordering TAS.
Do you remember the reason?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:20:54Z

Actually we have such tests, for example: https://github.com/kubernetes-sigs/kueue/blob/eefce7b724f27fa01db4d36032284e59a78cd7d6/pkg/controller/tas/topology_ungater_test.go#L1457
This in `wantPods` assets the Pod-to-Node assignment and this assignment is determined by the rank-based ordering.

Maybe we could somehow make the asserts more explicit, but the functionality itself is tested already. For example I believe if you swap the Pods' `batchv1.JobCompletionIndexAnnotation` (or remove) you will get different assignmentts.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T12:27:00Z

> Actually we have such tests, for example:
> 
> [kueue/pkg/controller/tas/topology_ungater_test.go](https://github.com/kubernetes-sigs/kueue/blob/eefce7b724f27fa01db4d36032284e59a78cd7d6/pkg/controller/tas/topology_ungater_test.go#L1457)
> 
> Line 1457 in [eefce7b](/kubernetes-sigs/kueue/commit/eefce7b724f27fa01db4d36032284e59a78cd7d6)
> 
>  "ranks: support rank-based ordering for JobSet - for all Pods": { 
> 
> This in `wantPods` assets the Pod-to-Node assignment and this assignment is determined by the rank-based ordering.
> Maybe we could somehow make the asserts more explicit, but the functionality itself is tested already. For example I believe if you swap the Pods' `batchv1.JobCompletionIndexAnnotation` (or remove) you will get different assignmentts.

Yes, we have "test case", but we verify only the set of assignment: https://github.com/kubernetes-sigs/kueue/blob/0880bb125aada2662cb298d6910cdce30a7a9c1a/pkg/controller/tas/topology_ungater_test.go#L2306-L2317

We don't care which Pod gets which Node assignment. Am I missing something?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:32:15Z

We verify the final NodeSelector for each Pod: https://github.com/kubernetes-sigs/kueue/blob/eefce7b724f27fa01db4d36032284e59a78cd7d6/pkg/controller/tas/topology_ungater_test.go#L1526-L1527

So this is checking the assignment. However, for what I see most (or all) test cases test block -> rack without going to the node level. So, we could extend that tests for the "node-level" topology, which would also be closer to our the usage we actually observe (most deployments Ive seen specifty kubernetes.io/hostname as the lowest level)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:33:57Z

Oh, actually I'm mistaken, NodeSelector is excluded from comparison: https://github.com/kubernetes-sigs/kueue/blob/eefce7b724f27fa01db4d36032284e59a78cd7d6/pkg/controller/tas/topology_ungater_test.go#L2296-L2299

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:36:22Z

Ok, I think I remember and this is for historical reasons. At the beginning we didn't have rank-based ordering, so we couldn't assert exactly on the node selectors, because the tests would flake - the assignments could have been random.

As we now have rank-based ordering we could indeed assert the NodeSelectors exactly. I guess we could add flag to the test cases which are guaranteed to be stable, like "nodeSelectorAssertMode" being "Exact" or "CountsOnly"

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T12:44:17Z

> Oh, actually I'm mistaken, NodeSelector is excluded from comparison:

Yeah, exactly. 

> Ok, I think I remember and this is for historical reasons. At the beginning we didn't have rank-based ordering, so we couldn't assert exactly on the node selectors, because the tests would flake - the assignments could have been random.
> 
> As we now have rank-based ordering we could indeed assert the NodeSelectors exactly. I guess we could add flag to the test cases which are guaranteed to be stable, like "nodeSelectorAssertMode" being "Exact" or "CountsOnly"

It would be better to introduce such test because I faced actual behavior (E2E test / manually test) is not expected even if those UTs succeeded, during https://github.com/kubernetes-sigs/kueue/pull/8618 impls.

So, avoiding such cases (no way to verify TAS rank-based ordering in UTs) would be better.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T12:49:28Z

Great, maybe you can even produce such a preparetory PR to just use "Exact" assert on NodeSelectors whenever possible ( at least for all rank-based ordering tests).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T13:12:51Z

> Great, maybe you can even produce such a preparetory PR to just use "Exact" assert on NodeSelectors whenever possible ( at least for all rank-based ordering tests).

Yes, we should verify "Exact" behavior only when rank-ordering is enabled. After I fix some bugs, I might be able to pick this one, but I don't block anyone here. So, if anyone is interested in this issue, feel free to take this one.

### Comment by [@omerap12](https://github.com/omerap12) — 2026-04-05T17:09:52Z

Hey @tenzen-y, 
Would love to take this one if that's ok with you :) 
/assign
