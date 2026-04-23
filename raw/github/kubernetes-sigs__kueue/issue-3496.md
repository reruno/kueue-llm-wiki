# Issue #3496: Repeated errors in kueue-manager log when Kueue 0.9 is installed on Kubernetes 1.29

**Summary**: Repeated errors in kueue-manager log when Kueue 0.9 is installed on Kubernetes 1.29

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3496

**Last updated**: 2025-01-16T08:42:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-11-08T22:10:13Z
- **Updated**: 2025-01-16T08:42:08Z
- **Closed**: 2025-01-16T08:42:06Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I created a fresh kind 0.24 cluster with Kubernetes 1.27.17.  I installed the Kueue 0.9 release on the cluster. 

Every 30 seconds (+/-) the kueue-controller-manager log contains the following stanza:
```
W1108 22:04:17.191809       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.FlowSchema: the server could not find the requested resource
E1108 22:04:17.191842       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.FlowSchema: failed to list *v1.FlowSchema: the server could not find the requested resource" logger="UnhandledError"
W1108 22:04:23.165653       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.PriorityLevelConfiguration: the server could not find the requested resource
E1108 22:04:23.165688       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.PriorityLevelConfiguration: failed to list *v1.PriorityLevelConfiguration: the server could not find the requested resource" logger="UnhandledError"
W1108 22:04:23.370784       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource
E1108 22:04:23.370836       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicyBinding: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource" logger="UnhandledError"
W1108 22:04:52.216220       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource
E1108 22:04:52.216261       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicy: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource" logger="UnhandledError"
W1108 22:04:58.002480       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.PriorityLevelConfiguration: the server could not find the requested resource
E1108 22:04:58.002507       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.PriorityLevelConfiguration: failed to list *v1.PriorityLevelConfiguration: the server could not find the requested resource" logger="UnhandledError"
W1108 22:05:02.844004       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource
E1108 22:05:02.844044       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicyBinding: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource" logger="UnhandledError"
```

**What you expected to happen**:

I do not expect to see error logs when running Kueue 0.9.0 on Kubernetes 1.27.  This is a regression vs. Kueue 0.8.3.

**How to reproduce it (as minimally and precisely as possible)**:

Create 1.27 cluster with kind.
```
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.9.0/manifests.yaml
```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.17
- Kueue version (use `git describe --tags --dirty --always`): 0.9.0
- Cloud provider or hardware configuration: MacOS (arm64)

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-09T13:50:12Z

1.27 is out of support in open source. Kueue 0.9.0 was probably built with 1.31 apis so I’m not sure the skew will even be supporting at this point.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-11T18:45:44Z

On Kubernetes 1.29 (which I believe is still in support until 2025-02-28), I get a reduced set of repeating error messages but there is still a problem:

```
W1111 18:40:52.560632       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource
E1111 18:40:52.560667       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicy: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource" logger="UnhandledError"
W1111 18:41:35.548617       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource
E1111 18:41:35.548652       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicy: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource" logger="UnhandledError"
W1111 18:41:36.038435       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource
E1111 18:41:36.038474       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicyBinding: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource" logger="UnhandledError"
W1111 18:42:11.505717       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource
E1111 18:42:11.505754       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicy: failed to list *v1.ValidatingAdmissionPolicy: the server could not find the requested resource" logger="UnhandledError"
W1111 18:42:15.087195       1 reflector.go:561] k8s.io/client-go/informers/factory.go:160: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource
E1111 18:42:15.087231       1 reflector.go:158] "Unhandled Error" err="k8s.io/client-go/informers/factory.go:160: Failed to watch *v1.ValidatingAdmissionPolicyBinding: failed to list *v1.ValidatingAdmissionPolicyBinding: the server could not find the requested resource" logger="UnhandledError"
```

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-11T19:07:51Z

I verified that on Kubernetes 1.30 there are no error messages in the log.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-11T19:17:51Z

retitled issue to only mention supported Kubernetes version (1.29).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-12T06:13:10Z

As I can see here https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/, `ValidatingAdmissionPolicy` is stable starting from version v1.30. Kueue v0.9 build with v1.31 apis. That's why we have this error on 1.29.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-12T07:59:05Z

@mbobrovskyi do you know if this is just a weird logging, or `ValidatingAdmissionPolicy` does not work in Kueue in 1.29? 
I would suppose it should still work even while in Beta, but then it is still surprising to see this error.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-13T20:35:49Z

A quick glance at the 1.29 documentation seems to imply that although VAP was in Beta in 1.29, the feature gate still defaulted to false.

https://v1-29.docs.kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-14T00:11:37Z

Are you able to see this with just kind?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-11-14T02:07:20Z

I was just using kind.  (kind 0.25 with --image v1.29.10@sha256:3b2d8c31753e6c8069d4fc4517264cd20e86fd36220671fb7d0a5855103aa84b).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-14T08:33:50Z

> A quick glance at the 1.29 documentation seems to imply that although VAP was in Beta in 1.29, the feature gate still defaulted to false.

So, the question if you can enable it on 1.29 to mitigate the issue. 
Another question would be if Kueue can do something to stop logging or make it less often - I don't know for now.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-11-14T15:02:11Z

I reached out to @benluddy about this issue. This seems like an upstream issue and not really related to Kueue at the moment.

### Comment by [@benluddy](https://github.com/benluddy) — 2024-11-14T15:27:04Z

Looks like kueue-controller-manager has started informers for the v1 VAP APIs, which did not exist in 1.27.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-12-07T20:35:30Z

@benluddy 

Searching through kueue, the only place where I see VAP is [here](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/cert/cert.go#L41).

It looks like we set some rbac for roles but I didn't see any usage of it on a quick search.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T08:42:01Z

I believe https://github.com/kubernetes-sigs/kueue/pull/3908 addressed the issue (based on the discussion and the `Fixes: #3496` in the description - not sure why it didn't auto-close the issue).

I also don't see the errors logged now in our e2e tests against 1.29, checked [this log](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1879642995276386304/artifacts/run-test-e2e-1.29.4/kind-worker/pods/kueue-system_kueue-controller-manager-79b94dcc76-n4q65_cbc35885-d61d-47af-95d9-226c730655b6/manager/0.log) and [this](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1879642995276386304/artifacts/run-test-e2e-1.29.4/kind-worker2/pods/kueue-system_kueue-controller-manager-79b94dcc76-l48ct_4a56f4bd-dbc6-4ec6-8b19-ac6dabb4efa1/manager/0.log).

/close   
(feel free to re-open if the issue still occurs)

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-16T08:42:06Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3496#issuecomment-2594876179):

>I believe https://github.com/kubernetes-sigs/kueue/pull/3908 addressed the issue (based on the discussion and the `Fixes: #3496` in the description - not sure why it didn't auto-close the issue).
>
>I also don't see the errors logged now in our e2e tests against 1.29, checked [this log](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1879642995276386304/artifacts/run-test-e2e-1.29.4/kind-worker/pods/kueue-system_kueue-controller-manager-79b94dcc76-n4q65_cbc35885-d61d-47af-95d9-226c730655b6/manager/0.log) and [this](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1879642995276386304/artifacts/run-test-e2e-1.29.4/kind-worker2/pods/kueue-system_kueue-controller-manager-79b94dcc76-l48ct_4a56f4bd-dbc6-4ec6-8b19-ac6dabb4efa1/manager/0.log).
>
>/close   
>(feel free to re-open if the issue still occurs)


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
