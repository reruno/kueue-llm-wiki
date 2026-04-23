# Issue #3382: Cleanup use of deref cancel in tests

**Summary**: Cleanup use of deref cancel in tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3382

**Last updated**: 2024-11-05T11:47:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-30T17:17:58Z
- **Updated**: 2024-11-05T11:47:37Z
- **Closed**: 2024-11-05T11:47:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Instead of `deref cancel()` it is better to use `t.Cleanup(cancel)` where possible.

**Why is this needed**:

To better practice to use t.Cleanup in tests: https://stackoverflow.com/questions/61609085/what-is-useful-for-t-cleanup.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-30T17:18:05Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-30T17:18:14Z

cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-04T04:36:20Z

IIUC from [this comment](https://stackoverflow.com/a/61609670/5571851), the difference is that `defer` runs at the end of the function, whereas `t.Cleanup()` runs at the end of the test. I'm not sure it’s correct in our case to use t.Cleanup(). If we call context.WithCancel() in this function, we should cancel it here, not at the end of the test.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-04T05:55:58Z

However I think `t.Cleanup()` can be very useful on this case:

https://github.com/kubernetes-sigs/kueue/blob/243f270a34db0fd85ed76b8ff2fb3ddaafd96b57/cmd/experimental/kjobctl/pkg/builder/slurm_builder_test.go#L75-L93

Like this:

``` 
func beforeSlurmTest(t *testing.T, tc *slurmBuilderTestCase) error {
	file, err := os.CreateTemp("", "slurm")
	if err != nil {
		return err
	}
	defer file.Close()
	t.Cleanup(func() {
		os.Remove(tc.tempFile)
	})

	if _, err := file.WriteString("#!/bin/bash\nsleep 300'"); err != nil {
		return err
	}

	tc.tempFile = file.Name()

	return nil
}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-04T06:24:07Z

I see, let's use it whenever applicable. FYI it was originally started in this comment https://github.com/kubernetes-sigs/kueue/pull/3361#discussion_r1822921952.
