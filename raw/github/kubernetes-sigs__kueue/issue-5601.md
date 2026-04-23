# Issue #5601: Remove redundant setup code for scheme in unit tests

**Summary**: Remove redundant setup code for scheme in unit tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5601

**Last updated**: 2025-06-11T06:27:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-10T12:02:42Z
- **Updated**: 2025-06-11T06:27:01Z
- **Closed**: 2025-06-11T06:27:01Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

drop the setup code from unit tests:
```golang
	// Setup.
	scheme := runtime.NewScheme()
	if err := kueue.AddToScheme(scheme); err != nil {
		t.Fatalf("Failed adding kueue scheme: %s", err)
	}
```

**Why is this needed**:

this code is not needed in some tests like TestGetPendingWorkloadsInfo. Maybe it was needed historically, but not since we are using utiltesting.NewFakeClient() as indicated in the comment: https://github.com/kubernetes-sigs/kueue/pull/5587#discussion_r2137545613

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T12:02:51Z

cc @kaisoz @tenzen-y

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-10T13:58:01Z

/assign 
Thanks!
