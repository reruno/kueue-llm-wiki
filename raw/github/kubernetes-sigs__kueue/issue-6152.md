# Issue #6152: Kueue Controller-Manager and client certs provided by apiserver

**Summary**: Kueue Controller-Manager and client certs provided by apiserver

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6152

**Last updated**: 2025-12-21T17:26:12Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@golpa](https://github.com/golpa)
- **Created**: 2025-07-23T22:41:25Z
- **Updated**: 2025-12-21T17:26:12Z
- **Closed**: 2025-12-21T17:26:11Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: 
Trying to evaluate kueue but unable to get it operational. We believe the core problem is that the `v1beta1.visibility.kueue.x-k8s.io` API Service does not become available:  
```
$ sudo kubectl get apiservice
NAME                                      SERVICE                                AVAILABLE                      AGE
...
v1beta1.visibility.kueue.x-k8s.io         kueue-system/kueue-visibility-server   False (FailedDiscoveryCheck)   40d

$ sudo kubectl describe apiservice v1beta1.visibility.kueue.x-k8s.io
...
    Message:               failing or missing response from https://10.96.176.227:443/apis/visibility.kueue.x-k8s.io/v1beta1: bad status from https://10.96.176.227:443/apis/visibility.kueue.x-k8s.io/v1beta1: 401
```

**What you expected to happen**:

An operation apiservice (which presumably would make kueue work)

**How to reproduce it (as minimally and precisely as possible)**:
1. Ensure kube-apiserver is running with `--proxy-client-key-file` and `--proxy-client-cert-file` (see below for why we think this is relevant)
2. Install kueue via helm:
   ```
   helm install kueue oci://registry.k8s.io/kueue/charts/kueue --version 0.12.4 --namespace kueue-system --create-namespace --wait --timeout 300s
   ```
Wait until deployed and run above commands to check api service

**Anything else we need to know?**:
We did a bit digging and we suspect this is related to the kube-apiserver running with `--proxy-client-cert-file` and `--proxy-client-key-file` options.

After starting, the kueue-controller-manager logs this error message every few seconds:
```
E0723 21:31:26.442035       1 authentication.go:74] "Unable to authenticate the request" err="[x509: certificate signed by unknown authority, verifying certificate SN=351854341205648679789924665960308317511398593087, SKID=F9:C4:14:DF:EE:91:77:83:74:23:97:C0:35:2C:93:C4:5E:9D:7F:6B, AKID=25:2A:96:BA:73:9A:DE:0B:FE:C2:ED:8F:83:25:E2:54:11:43:05:9F failed: x509: certificate signed by unknown authority]"
```
Investigating further it appears the SN, SKID, AKID logged in kueue's controller-manager correspond to the certificate that the kube-apiserver uses with `--proxy-client-cert-file` and `--proxy-client-key-file`. Those options were enabled for utilizing kube metrics server.

We suspect the apiserver is providing the proxy certs as a client cert when connecting to kueue-controller-manager. Since that cert is signed by our own CA it's not being trusted. We were unable to find any option in the helm values.yaml file for specifying a trusted CA (ideal) or disabling cert verification. We suspect such an option would address the problem.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.31
- Kueue version (use `git describe --tags --dirty --always`): 0.12.4
- Cloud provider or hardware configuration: 60 node kubernetes bare metal cluster
- OS (e.g: `cat /etc/os-release`): ubuntu
- Kernel (e.g. `uname -a`): 5.4.0-1118-fips
- Install tools: helm
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-24T14:33:09Z

You could disable VisibilityOnDemand feature gate if this is not important to you.

There is a pretty big gap with VisibilityOnDemand around certs.

https://github.com/kubernetes-sigs/kueue/issues/4433

ref: https://github.com/kubernetes-sigs/kueue/issues/5610

### Comment by [@golpa](https://github.com/golpa) — 2025-07-24T15:10:51Z

Too early to tell if that feature is important to us or not so for now we can easily disable it. Based on a quick read on what that feature provides it might be important to us in the future but at least for now we can start trying out Kueue to see if it meets our needs. Hopefully by then this feature will have better cert management. 

Thank you for that suggestion!

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-24T15:22:17Z

Are you passing your custom certs to other components?

### Comment by [@golpa](https://github.com/golpa) — 2025-07-24T15:32:04Z

Primarily the `--proxy-client-key-file` and `--proxy-client-cert-file` were enabled with a cert from our internal CA as a requirement to use kube-metrics so that specific cert is only used for that component.

But our internal CA is used for a lot of other components. Our internal CA is what kubernetes is configured to use as the trusted CA in general. In other words `/run/secrets/kubernetes.io/serviceaccount/ca.crt` inside every pod has the CA cert that would validate our certs including the one above.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-24T15:36:27Z

So you are able to use this functionality with the helm chart?

I know that we did a lot of work to support Helm with Cert Manager and Prometheus but it sounds like you are providing your own secrets and such for it.

Cool!

### Comment by [@golpa](https://github.com/golpa) — 2025-07-24T15:45:52Z

We are in really early testing and haven't actually been able to submit a job to Kueue and see it work in action. Our assumption was because of those errors we saw in the controller-manager which triggered this ticket. Now with your suggestion and by manually removing the apiservice we need to go back and retry it. 🤞 it will now work.

Using cert-manager and prometheus integration are actually high priorities to get working next after we can get a simple job submitted. We have cert-manager configured to provide certs signed by our internal CA and prometheus is also configured to trust our internal CA.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-22T16:22:56Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-21T17:17:16Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-21T17:26:06Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-21T17:26:12Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6152#issuecomment-3679121495):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
