# Issue #9658: CustomConfigs in the ManageJobsWithoutQueueName tests only change configuration in BeforeAll

**Summary**: CustomConfigs in the ManageJobsWithoutQueueName tests only change configuration in BeforeAll

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9658

**Last updated**: 2026-03-04T06:28:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-03T16:24:46Z
- **Updated**: 2026-03-04T06:28:18Z
- **Closed**: 2026-03-04T06:28:18Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to only call UpdateKueueConfigurationAndRestart in the BeforeAll, examples which don't do that:
In [BeforeEach](https://github.com/kubernetes-sigs/kueue/blob/f415c6165c3642b71c0e03771719a63aead619de/test/e2e/customconfigs/managejobswithoutqueuename_test.go#L95-L107) and [AfterEach](https://github.com/kubernetes-sigs/kueue/blob/f415c6165c3642b71c0e03771719a63aead619de/test/e2e/customconfigs/managejobswithoutqueuename_test.go#L109-L113)

**Why is this needed**:

Since changing configuration is expensive we should minimize the number of times we do it. By using BeforeAll we can wrap multiple tests without changing configuration. Also, we don't need to change the configuration in the AfterEach. We can rely that the new test suite will change it in its BeforeAll based on the "memorized" original configuration.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T16:24:58Z

cc @mbobrovskyi ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-04T02:21:40Z

We can’t move it to the `BeforeAll` block because we need to know the namespace name. Since we only have one test, keeping it in `BeforeEach` is probably fine for now. WDYT?

I’ve created a cleanup/optimization PR: #9659.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-04T06:10:47Z

Ok. the alternative is to move the namespace generation to BeforeAll for this test set? This feels also reasonable.

Still be dont need ot in AfterEach, AfterAll
