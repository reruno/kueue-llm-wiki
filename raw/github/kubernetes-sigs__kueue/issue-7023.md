# Issue #7023: Introduce a helper for asserting events to reduce code duplication

**Summary**: Introduce a helper for asserting events to reduce code duplication

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7023

**Last updated**: 2026-01-12T18:12:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-26T11:41:18Z
- **Updated**: 2026-01-12T18:12:12Z
- **Closed**: 2026-01-12T18:12:12Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to introduce a helper which allows to encapsulate this pattern ([example](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L347-L353)):

```golang
ok, err := testing.HasEventAppeared(ctx, k8sClient, corev1.Event{
	Reason:  "AdmissionCheckRejected",
	Type:    corev1.EventTypeWarning,
	Message: fmt.Sprintf("Deactivating workload because AdmissionCheck for %v was Rejected: ", ac.Name),
})
g.Expect(err).NotTo(gomega.HaveOccurred())
g.Expect(ok).To(gomega.BeTrue())
```
This repeats many times where we need to repeat the last to lines.

I expect another helper util.VerifyEventAppeared (or util.ExpectEventAppeared)  which would enapsulate the gomega checks.

**Why is this needed**:

Reduce code duplication for common patterns

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T11:41:27Z

cc @PBundyra @olekzabl

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-09-26T21:50:57Z

AFAIU the Gomega docs [encourage](https://onsi.github.io/gomega/#handling-errors) to rewrite this as:

```go
g.Expect(testing.HasEventAppeared(ctx, k8sClient, corev1.Event{
	Reason:  "AdmissionCheckRejected",
	Type:    corev1.EventTypeWarning,
	Message: fmt.Sprintf("Deactivating workload because AdmissionCheck for %v was Rejected: ", ac.Name),
})).To(gomega.BeTrue())
```

This checks if `err != nil` (which seems equivalent to the original code as long as the tested method returns `X, error`).

Though it can be considered less readable (in that it packs a longer expression into a function call arg). \
One way around that would be:

```go
event := corev1.Event{
	Reason:  "AdmissionCheckRejected",
	Type:    corev1.EventTypeWarning,
	Message: fmt.Sprintf("Deactivating workload because AdmissionCheck for %v was Rejected: ", ac.Name),
}
g.Expect(testing.HasEventAppeared(ctx, k8sClient, event)).To(gomega.BeTrue())
```

WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:02:20Z

I'm ok with both approaches. The relevant question is what do you do with `error`? I don't like silencing the errors and returning false in that case.

So, my proposal was to basically encapsulate the existing code in another helper function which would do the gomega checks.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-07T11:18:18Z

> I don't like silencing the errors and returning false in that case.

Oh, I don't think it's silencing. It's rather just that
```
g.Expect(ok, err).To(gomega.BeTrue())
```
is equivalent to
```
g.Expect(ok).To(gomega.BeTrue())
g.Expect(err).NotTo(gomega.HaveOccurred())
```

I just checked it in practice. \
Putting `false, fmt.Errorf("fake error")` into that produced
```
  Unexpected error: fake error
      <*errors.errorString | 0xc000e20c70>: 
      fake error
      {s: "fake error"}
```
in both variants.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T12:17:21Z

Ok, I just didn't see `g.Expect(ok, err).To(gomega.BeTrue())` as part of the proposal. I think at this point it might be simpler to just submit a PR

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T12:24:13Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:30:23Z

/remove-lifecycle stale

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-01-12T16:38:59Z

/assign
