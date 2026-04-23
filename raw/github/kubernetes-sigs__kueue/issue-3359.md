# Issue #3359: Delete redundant retry logic in multikueue controller

**Summary**: Delete redundant retry logic in multikueue controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3359

**Last updated**: 2024-11-06T19:49:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-10-29T12:24:46Z
- **Updated**: 2024-11-06T19:49:31Z
- **Closed**: 2024-11-06T19:49:31Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Multikueue controller sets AdmissionCheck to Pending after it was set to Retry. Workload controller already does, after the #3323 

**Why is this needed**:
Cleanup

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T12:27:06Z

/cc @mbobrovskyi @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T12:32:14Z

@PBundyra Will you work on this part of https://github.com/kubernetes-sigs/kueue/issues/3231?
Or separately?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-10-29T12:35:26Z

> @PBundyra Will you work on this part of #3231? Or separately?

I believe it should be approached separately

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T12:37:03Z

> > @PBundyra Will you work on this part of #3231? Or separately?
> 
> I believe it should be approached separately

That makes sense. In that case, you can focus on #3231, and anyone can help with this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T12:49:01Z

FYI I summarized the redundant code in the https://github.com/kubernetes-sigs/kueue/issues/3351#issuecomment-2444059575.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-30T10:16:53Z

/assign
