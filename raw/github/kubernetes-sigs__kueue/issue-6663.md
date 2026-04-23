# Issue #6663: CrashLoopBackOff when using config/alpha-enabled due to missing AdmissionFairSharing config

**Summary**: CrashLoopBackOff when using config/alpha-enabled due to missing AdmissionFairSharing config

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6663

**Last updated**: 2025-08-26T09:32:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@abhijeet-dhumal](https://github.com/abhijeet-dhumal)
- **Created**: 2025-08-25T15:07:29Z
- **Updated**: 2025-08-26T09:32:13Z
- **Closed**: 2025-08-26T09:32:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

When deploying Kueue with `config/alpha-enabled` (which uses `--feature-gates=AllAlpha=true`), the controller crashes with a nil pointer dereference resulting in CrashLoopBackOff

Reference thread : https://github.com/kubernetes-sigs/kueue/pull/6597#issuecomment-3220069521


The issue occurs because:
1. `AllAlpha=true` flag enables the AdmissionFairSharing feature
2. No `admissionFairSharing` configuration is provided in the default config (commented out in `kueue-manager-config` ConfigMap)
3. `cfg.AdmissionFairSharing = nil` (no config provided)
4. Scheduler calls `CalculateEntryPenalty(requests, nil)`
5. Crash at line 49: `afs.UsageSamplingInterval.Seconds()` when `afs` is nil

**What you expected to happen**:

The controller should start successfully when using `config/alpha-enabled`, either by:
- Providing a default configuration for AdmissionFairSharing when the feature is enabled
- Gracefully handling the nil configuration case

**How to reproduce it (as minimally and precisely as possible)**:

1. Deploy Kueue using alpha-enabled configuration:
   ```bash
   kubectl apply -k config/alpha-enabled
   ```
2. Observe controller pod in CrashLoopBackOff state:
   ```bash
   kubectl get pods -n kueue-system
   kubectl logs -n kueue-system -l app=kueue-controller-manager
   ```

**Anything else we need to know?**:

**Workarounds that work:**

1. Add nil check in `pkg/util/admissionfairsharing/admission_fair_sharing.go`:
   ```go
   func CalculateEntryPenalty(totalRequests corev1.ResourceList, afs *config.AdmissionFairSharing) corev1.ResourceList {
   	// Return empty penalty if no admission fair sharing config is provided
   	if afs == nil {
   		return corev1.ResourceList{}
   	}
   	alpha := CalculateAlphaRate(
   		afs.UsageSamplingInterval.Seconds(),
   		afs.UsageHalfLifeTime.Seconds(),
   	)
   	return resource.MulByFloat(totalRequests, alpha)
   }
   ```

2. Or provide explicit AdmissionFairSharing configuration in `kueue-manager-config` ConfigMap:
   ```yaml
   admissionFairSharing:
     usageHalfLifeTime: "168h"
     usageSamplingInterval: "5m"
     resourceWeights:
       cpu: 1
       memory: 1
   ```

This affects TrainJob v2 integration testing as the controller cannot start with alpha features enabled

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T16:04:45Z

Thank you for the report.
Would you be interested in proposing a patch?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T16:05:27Z

> This affects TrainJob v2 integration testing as the controller cannot start with alpha features enabled

Looking at that PR, there isn't any reason why you have to enable the alpha features. TrainJob is not under a feature gate.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-25T18:19:57Z

cc @PBundyra

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-26T08:24:44Z

/assign
