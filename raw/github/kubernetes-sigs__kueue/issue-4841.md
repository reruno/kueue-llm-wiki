# Issue #4841: Enable to get metrics via HTTP

**Summary**: Enable to get metrics via HTTP

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4841

**Last updated**: 2025-09-08T19:49:57Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@highpon](https://github.com/highpon)
- **Created**: 2025-03-31T16:07:20Z
- **Updated**: 2025-09-08T19:49:57Z
- **Closed**: 2025-09-08T19:49:56Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@highpon](https://github.com/highpon)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add an option to allow metrics to be retrieved via HTTP

**Why is this needed**:
We want to retrieve metrics without HTTPS or TLS authentication.
In a closed network, it may be better not to have them.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@highpon](https://github.com/highpon) — 2025-03-31T16:07:29Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-31T16:26:22Z

we offer metrics via https using internal certs, ootb. can you describe what is the use case for plain http? Is it improving startup time?

### Comment by [@highpon](https://github.com/highpon) — 2025-03-31T16:46:23Z

@mimowo 
Thanks for your reply!

> we offer metrics via https using internal certs, ootb. can you describe what is the use case for plain http? Is it improving startup time?

I did not intend to speed up the startup time.

I proposed this feature because I believe that Kueue users can obtain metrics in a simple configuration by supporting the ability to obtain metrics via HTTP, assuming an environment that does not require authentication, authorization, or encryption.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-31T16:54:27Z

thabks for your reply. I see, TLS is not needed in many internal networks, but wondering what is the benefit to the end users since TLS using internal certs is the default. 

Maybe even if this wasn't the original motivation it is still good for users as it reduces the amount of resources needed to generate the certs and thus the start up time.

We actually discussed this before with @tenzen-y and @kannon92 and we thought we don't need to support plain http, but I'm ok to revisit it.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-31T17:26:37Z

Reading this, we are saying that it is okay to disable this because there are admins who don't want any kind of protections on their metrics endpoints?

This seems to be a security vulnerability imo and we should very clearly mark that this is not recommended. 

Right now, we require that people that access the metrics endpoint must have access to the serviceAccount. But if you want to relax this, then you could say anyone can view metrics of Kueue.

### Comment by [@highpon](https://github.com/highpon) — 2025-04-01T02:45:45Z

@kannon92 
Thanks for your reply!

Surely the documentation should clearly state that it should not be recommended.
I believe that if the documentation describes the risks of enabling the option, there will be no cases of misuse by users who want to connect with TLS enabled.

However, I think there are security risks involved.
I assume that the Kueue Configuration API is used to enable/disable this functionality.
The Kueue Configuration API is managed using ConfigMap, and I think the relative risk is higher because if you can even manipulate ConfigMap, you can expose metrics information without certificate authentication/authorization.

### Comment by [@atosatto](https://github.com/atosatto) — 2025-04-01T10:18:48Z

> Right now, we require that people that access the metrics endpoint must have access to the serviceAccount. But if you want to relax this, then you could say anyone can view metrics of Kueue.

I am currently running Kueue with `internalCertManagement.enabled = false` to provide Kueue with custom certificates for the webhooks. The current implementation of secured metrics is enabling AuthN/AuthZ via tokenreviews and subjectaccessreviews in addition to HTTPs. I think this is amazing for most of the users however it lacks some flexibility that might be required by others.

I think it would be nice to relax this constraint and allow users to configure mTLS to secure metrics scraping without adding the dependency on the Kubernetes API or allow users to meet these bespoke authN/authZ requirements via a sidecar. For example `node-exporter` allows to enable mTLS via 

```yaml
tls_server_config:
  # Certificate and key files for server to use to authenticate to client.
  cert_file: "/etc/node_exporter/server.crt"
  key_file: "/etc/node_exporter/server.key"
  # Enforce mutual TLS.
  # For more detail on clientAuth options: https://golang.org/pkg/crypto/tls/#ClientAuthType
  client_auth_type: "RequireAndVerifyClientCert"
  # CA certificate for client certificate authentication to the server.
  client_ca_file: "/etc/node_exporter/root_ca.crt"
```

### Comment by [@jenniferlai43](https://github.com/jenniferlai43) — 2025-04-11T18:03:18Z

I am running into the same issue, and it would be really difficult to set up certs for our internal metrics scraper (as a workaround) - let me know how I can help to get this into the next release!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-11T18:06:44Z

Ideally someone adds a small KEP and implements the solution. Seeing the interest Im ok to move it forward with appropriate warning message. cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-11T18:22:20Z

> Ideally someone adds a small KEP and implements the solution. Seeing the interest Im ok to move it forward with appropriate warning message. cc [@tenzen-y](https://github.com/tenzen-y)

+1 on a small KEP. Especially, we want to clarify the assuming use cases and solutions (whether or not we should disable it by default or enable it by default)

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-10T18:45:48Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-09T19:39:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T19:49:51Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-08T19:49:57Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4841#issuecomment-3267716880):

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
