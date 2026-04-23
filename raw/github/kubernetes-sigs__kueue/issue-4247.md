# Issue #4247: FairSharing.Weight sensitive to high and low values

**Summary**: FairSharing.Weight sensitive to high and low values

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4247

**Last updated**: 2025-09-25T11:34:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-02-12T10:43:15Z
- **Updated**: 2025-09-25T11:34:26Z
- **Closed**: 2025-09-25T11:34:26Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 13

## Description

When `FairSharing.Weight` is set to a high number (~100+), _especially_ when the quantity of the resource in question is rather small (e.g. `gpu`), the fair sharing value quickly collapses to 0.

We should document (and perhaps limit via API validation) recommended range of `FairSharing.Weight`, and consider making it less sensitive to this collapse.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:14:11Z

SGTM

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:14:50Z

Maybe, this will improve UX? Let's say this as feature.

/remove-kind cleanup
/kind feature

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-06T15:24:06Z

This is affecting a user. See #4333

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-04T16:10:03Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T16:13:46Z

/remove-lifecycle stale

### Comment by [@sanposhiho](https://github.com/sanposhiho) — 2025-07-10T06:53:35Z

This looks more like a bug (at the API level) from a certain perspective, because you accept `resource.Quantity`, but only a specific range of numbers will work..

### Comment by [@amy](https://github.com/amy) — 2025-08-19T19:00:49Z

/cc

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-19T13:06:51Z

We are losing some precison due to MilliValue https://github.com/kubernetes-sigs/kueue/blob/b3c4426a1428a0ac8fb339631b0e456d08a79e01/pkg/cache/scheduler/fair_sharing.go#L84

Additionally, it seems there is a lower-bound to the size of values `resource.Quantity` can represent before it collapses to zero

edit: I updated this, as the previous result was wrong (because of `fmt.Sprintf` losing float precision). MilliValue is accurate down to 10^-3, while AsFloat64Slow is accurate down to 10^-9.

```
func accuracy(q string) {
	fmt.Println("Quantity:", q)
	quantity := resource.MustParse(q)
	milli := quantity.DeepCopy()
	approx := quantity.DeepCopy()
	slow := quantity.DeepCopy()

	fmt.Println("  MilliValue:", milli.MilliValue())
	fmt.Println("  ApproxValue:", approx.AsApproximateFloat64())
	fmt.Println("  SlowValue:", slow.AsFloat64Slow())
}

accuracy("0.1")
accuracy("0.0001")
accuracy("0.000001")
accuracy("0.0000000001")
accuracy("0.00000000001")
```

```
Quantity: 0.1
  MilliValue: 100
  ApproxValue: 0.1
  SlowValue: 0.1
Quantity: 0.0001
  MilliValue: 1
  ApproxValue: 0.0001
  SlowValue: 0.0001
Quantity: 0.000001
  MilliValue: 1
  ApproxValue: 1e-06
  SlowValue: 1e-06
Quantity: 0.0000000001
  MilliValue: 1
  ApproxValue: 1e-09
  SlowValue: 1e-09
Quantity: 0.00000000001
  MilliValue: 1
  ApproxValue: 1e-09
  SlowValue: 1e-09
```

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-19T13:10:46Z

/retitle FairSharing.Weight sensitive to high and low values

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-24T09:44:05Z

/reopen

fixed the high-value sensitivity, but not low-value

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-24T09:44:10Z

@gabesaba: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4247#issuecomment-3327485372):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-09-24T11:39:09Z

Does it also mean we should use [AsApproximateFloat64](https://github.com/kubernetes/apimachinery/blob/v0.34.1/pkg/api/resource/quantity.go#L467) [¶](https://pkg.go.dev/k8s.io/apimachinery/pkg/api/resource#Quantity.AsApproximateFloat64) instead of [AsFloat64Slow](https://github.com/kubernetes/apimachinery/blob/v0.34.1/pkg/api/resource/quantity.go#L488) [¶](https://pkg.go.dev/k8s.io/apimachinery/pkg/api/resource#Quantity.AsFloat64Slow)?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-24T12:26:06Z

I don't think so. There are still some small precision issues (you can play around with code below). Especially if we can get #6983 working, so that this call isn't on hot-path

```
func same(t *testing.T, q string) {
	quantity := resource.MustParse(q)

	if quantity.AsApproximateFloat64() != quantity.AsFloat64Slow() {
		t.Error(q, quantity.AsApproximateFloat64(), quantity.AsFloat64Slow())
	}
}

func TestSame(t *testing.T) {
	//for i := range 1_000_000_000 {
	for i := range 1_000 {
		floatStr := fmt.Sprintf("0.%09d", i)
		same(t, floatStr)
	}
}

```

```
    fair_sharing_test.go:788: 0.000000003 3.0000000000000004e-09 3e-09
    fair_sharing_test.go:788: 0.000000006 6.000000000000001e-09 6e-09
    fair_sharing_test.go:788: 0.000000007 7.000000000000001e-09 7e-09
    fair_sharing_test.go:788: 0.000000009 9.000000000000001e-09 9e-09
    fair_sharing_test.go:788: 0.000000011 1.1000000000000001e-08 1.1e-08
    fair_sharing_test.go:788: 0.000000012 1.2000000000000002e-08 1.2e-08
    fair_sharing_test.go:788: 0.000000014 1.4000000000000001e-08 1.4e-08
    fair_sharing_test.go:788: 0.000000015 1.5000000000000002e-08 1.5e-08
    fair_sharing_test.go:788: 0.000000018 1.8000000000000002e-08 1.8e-08
    fair_sharing_test.go:788: 0.000000021 2.1000000000000003e-08 2.1e-08
    fair_sharing_test.go:788: 0.000000022 2.2000000000000002e-08 2.2e-08
    fair_sharing_test.go:788: 0.000000024 2.4000000000000003e-08 2.4e-08
    fair_sharing_test.go:788: 0.000000025 2.5000000000000002e-08 2.5e-08
    fair_sharing_test.go:788: 0.000000028 2.8000000000000003e-08 2.8e-08
    fair_sharing_test.go:788: 0.000000030 3.0000000000000004e-08 3e-08
    fair_sharing_test.go:788: 0.000000033 3.3000000000000004e-08 3.3e-08
```
