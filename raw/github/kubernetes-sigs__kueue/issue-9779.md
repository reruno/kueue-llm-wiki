# Issue #9779: Visibility server returns 500 Internal Server Error when lacking SubjectAccessReview permissions

**Summary**: Visibility server returns 500 Internal Server Error when lacking SubjectAccessReview permissions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9779

**Last updated**: 2026-03-31T15:43:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Nilsachy](https://github.com/Nilsachy)
- **Created**: 2026-03-10T10:46:57Z
- **Updated**: 2026-03-31T15:43:14Z
- **Closed**: 2026-03-31T15:43:13Z
- **Labels**: `kind/bug`
- **Assignees**: [@MatteoFari](https://github.com/MatteoFari)
- **Comments**: 7

## Description

**What happened**:

When the Kueue visibility server is configured with a custom kubeconfig and the associated identity lacks the `system:auth-delegator` ClusterRole (which grants permission to create `SubjectAccessReview` resources), requests to visibility endpoints result in an `Internal Server Error (500)`.

The error message emitted is: 

```
"Internal Server Error: \"/apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/test-kubeconfig-cq/pendingworkloads\": subjectaccessreviews.authorization.k8s.io is forbidden: User \"system:serviceaccount:kueue-system:visibility-test-sa\" cannot create resource \"subjectaccessreviews\" in API group \"authorization.k8s.io\" at the cluster scope"
```

**What you expected to happen**:

The visibility server should handle the case where it cannot perform delegated authorization and return a `Forbidden (403)` or `Unauthorized (401)` error to the client, rather than a `500 Internal Server Error`.

**How to reproduce it (as minimally and precisely as possible)**:

1. Start Kueue with the visibility server enabled.
2. Configure the visibility server to use a custom ServiceAccount via a kubeconfig.
3. Ensure the custom ServiceAccount does not have the `system:auth-delegator` ClusterRole.
4. Attempt to access a visibility API endpoint (e.g., `/apis/visibility.kueue.x-k8s.io/v1beta2/clusterqueues/<name>/pendingworkloads`).
5. Observe the 500 error response.

**Anything else we need to know?**:

This behavior was identified during E2E testing of the RBAC identity delegation in the visibility server (see `test/e2e/customconfigs/visibility_kubeconfig_test.go`). Ideally, the authorization delegation logic should be configured to map these "forbidden to check" errors to a 403 response.

## Discussion

### Comment by [@MatteoFari](https://github.com/MatteoFari) — 2026-03-23T09:35:20Z

/assign

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-24T16:45:35Z

I'll move the discussion into the issue itself because it's not related to the implementation PR.

As I stated [here](https://github.com/kubernetes-sigs/kueue/pull/10081#pullrequestreview-3998052180), 500 looks like the semantically correct error code for this, since it's the server itself that's lacking permissions, not the user making a request.

But this begs the question why we are handling 4 different errors here:
https://github.com/kubernetes-sigs/kueue/blob/6163e91e5a62befbdd421097fe0ec38b37d406e0/test/e2e/customconfigs/visibility_server_test.go#L194-L199

Since we now know we are expecting a 500, can't we just handle `IsInternalError`, maybe with a comment or `ginkgo.By` explaining why we expect that error code?
@Nilsachy @MatteoFari

### Comment by [@MatteoFari](https://github.com/MatteoFari) — 2026-03-25T09:06:35Z

Makes sense.

The e2e setup is already tightened in this PR so the test isolates delegated authorization from delegated authentication.

If others agree, I can remove the wrapper and make the negative case expect only `IsInternalError`, with a short comment explaining that the server itself cannot complete delegated authorization in this case.

### Comment by [@Nilsachy](https://github.com/Nilsachy) — 2026-03-25T09:12:51Z

I initially added all the error types to investigate in this bug which one should be thrown to adhere to the semantics. If that's ok with you, we can scope it down to expect only `IsInternalError` (as is the error right now).

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-25T09:32:11Z

I see. IMO we should stick to the error codes that we are expecting in practice, this way the test might catch some other unrelated errors.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-31T15:43:06Z

Since https://github.com/kubernetes-sigs/kueue/pull/10081 is merged and we are in agreement about the scope, I think we can close this.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-31T15:43:14Z

@kshalot: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9779#issuecomment-4163600569):

>Since https://github.com/kubernetes-sigs/kueue/pull/10081 is merged and we are in agreement about the scope, I think we can close this.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
