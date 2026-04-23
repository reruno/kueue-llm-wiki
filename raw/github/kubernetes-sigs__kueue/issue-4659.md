# Issue #4659: Allowed values of integrations

**Summary**: Allowed values of integrations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4659

**Last updated**: 2025-07-16T17:04:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-03-17T16:10:04Z
- **Updated**: 2025-07-16T17:04:40Z
- **Closed**: 2025-07-16T17:04:40Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 26

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Trying to find the allowed values for `Integrations` is actually quite difficult.

The comments seem to have most of the fields but I think it is missing a few integrations.

**Why is this needed**:

I can't find a list of supported integrations in the code and the website documentation / config documentation is incomplete on integrations.

For example, is MXJob an allowed integration even though it is not specified in the comment on the configuration object?

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:12:50Z

Actually, MXJob is probably dropped for 0.11 as kubeflow does not support it any longer: https://github.com/kubernetes-sigs/kueue/issues/1429

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:14:33Z

Found it: https://github.com/kubernetes-sigs/kueue/pull/4077

AFAIK  all other integrations should be covered in comments.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-17T16:16:37Z

Would you be up for making this integration validation more explicit in the configuration?

a list of allowed enums?

I would like to know on each release of Kueue what values are supported and how to validate that.

But it seems the comments are best effort as I can imagine we may have an issue where someone forgets to update that comment but adds an integration.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-17T16:17:03Z

ah, I saw some docs around MXJob so I was confused.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:24:54Z

> Would you be up for making this integration validation more explicit in the configuration?

I'm not sure how this would work TBH, maybe if you provide more details.

I think what you are looking for mostly is single place which defines all the supported frameworks as their names are currently scattered: https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20FrameworkName&type=code

So, maybe just a single file Which lists all of them like a list of enums indeed.

Alternatively, we could log the list of supported frameworks on startup of Kueue, and mark (say with word enabled) those which are enabled.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-17T16:31:18Z

https://github.com/openshift/api/blob/32c2fac8206e78350d19c0fa975a345fdab3de83/operator/v1alpha1/types_kueue.go#L79

So I'm building an operator to configuration the installation of Kueue based on requested frameworks.

I am mainly going on good faith that those comments were the allowed frameworks. But I know they can change over time so I'm not entirely sure where to look to see if a new framework was added.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-17T16:32:54Z

I tried to look at the validation code but it was opaque to find what the allowed values are.

So in my operator we wanted to make it a list of enums.

I could propose a similar idea to our configuration doc that at least makes it more explicit that these integrations are really a list of enums that must match a certain form.

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-17T17:38:14Z

Looking at the list of integrations so far, it appears that the validation that would suit is a [qualified name](https://github.com/kubernetes/apimachinery/blob/6ce776c88d38a77a31e2afc871e74c57f6a3c03b/pkg/util/validation/validation.go#L41), which is a [label](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names) optionally prefixed by a [subdomain](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names) and separated with a forward slash

You could use the validation linked above when validating the registration to make sure all of the frameworks follow the same pattern going forward, and then anyone building an abstraction on Kueue can be at least semi confident in their ability to validate the names without having to maintain a list of valid frameworks, the user gets at least some early feedback

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T06:43:48Z

The validation for the format sounds reasonable. It can provide a quick feedback loop when configuring kueue.

However, there are exceptions for the K8s built in types. 

OTaoH now I think kueue knows all the framework names so could validate based on the registered integrations, as this list is non extensible by users.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T06:59:43Z

> The validation for the format sounds reasonable. It can provide a quick feedback loop when configuring kueue.
> 
> However, there are exceptions for the K8s built in types.
> 
> OTaoH now I think kueue knows all the framework names so could validate based on the registered integrations, as this list is non extensible by users.

+1
We can add such validations to https://github.com/kubernetes-sigs/kueue/blob/69a9538f234aaeed55d825ac04e8c1338e62c5a7/pkg/controller/jobframework/setup.go#L57

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-18T09:04:42Z

> However, there are exceptions for the K8s built in types.

Based on https://github.com/kubernetes-sigs/kueue/blob/c8ae4c0e5f792d5a6a29b5bfbc4b1b334d6bacc2/apis/config/v1beta1/configuration_types.go#L354-L367, I see no exceptions. The built-ins do not have the optional prefix, but they would still validate correctly as a qualified name

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T09:13:58Z

> The built-ins do not have the optional prefix, but they would still validate correctly as a qualified name

Yes, I meant exceptions that don't have the prefix, but you already said "optional". I somehow missed that. In any case, I think Kueue could validate the list more precisely as it knows all the registered integrations.

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-18T09:21:48Z

> In any case, I think Kueue could validate the list more precisely as it knows all the registered integrations.

I agree. I still think it would be useful to set a standard for the names. Other projects building APIs on top of Kueue, exposing some of this configuration to their users, will want to be able to validate as early as possible that the configuration is valid, to the best of their ability.

Validating an enum is easy for Kueue, as the code is integrated here. Maintaining an enum for a third party API is harder. I would expect third party APIs to validate a pattern "this looks like it could be correct" rather than necessarily validating "this matches my pre-defined list", else there's toil and an API change every time Kueue supports a new integration, and the third party maintainer may not realise that their enum list has become stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T09:33:28Z

By third party you mean an extended Kueue fork or something else? It would be good to be on the same page when designing this. 

Actually, the last idea is not enum, but a check if every integration on the list is present among the registered integrations with the `framework.RegisterIntegration` call, [example](https://github.com/kubernetes-sigs/kueue/blob/17a48d55071576e8dc2ae34b0dd490b9ebaa2cf7/pkg/controller/jobs/job/job_controller.go#L61C32-L61C51). So, this would not require any extra maintaincence on the fork owners, but still I don't want to make any guarantees on this mechanism, and developers who fork Kueue to extend it are "on their own".

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-18T09:36:59Z

Specifically here I'm talking about someone building an operator to run Kueue. Operators are a common pattern across the Kube ecosystem, and often they build APIs that allow configuration of the operand. I'm not talking about forking Kueue.

From the end user experience perspective.

* User installs Kueue Operator
* User creates KueueConfiguration.mykueueoperator.example.com custom resource
* In the `spec` of the KueueConfiguration, the user configures a list of Frameworks they would like enabled
* The operator converts their desired configuration into the right input for Kueue and creates the deployment/webhooks/etc

It's this API which I'm talking about in my previous comment

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T10:21:30Z

Kueue does not know which integrations are enabled before starting. So, it's challenging to prepare a fixed enum list for all available integrations. Hence, I would propose exposing the util function to expose the registered integrations.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T10:38:33Z

This would work, but then one needs to make sure they compile the operator against exactly the same version as used at runtime.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T10:41:09Z

> This would work, but then one needs to make sure they compile the operator against exactly the same version as used at runtime.

I assumed that the operator uses Kueue as a Go library.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T10:48:19Z

Right, but it still imposes extra work on the admin to make sure the Kueue library version is the same as used at runtime. If they diverge there might be failures when the library claims something is not supported, but it is supported at runtime in fact.

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-18T11:23:38Z

I would suggest avoiding the operator requiring Kueue as a library apart from for particular API types (which should have minimal imports), as importing large parts of the codebase can lock dependencies and make it difficult for the operator developer. eg they want to move their deps up to a new version of controller-runtime, but Kueue hasn't cut a release with that version yet, so they can't

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:29:22Z

Ok, but still I think Kueue, when running, could validate the integrations list exactly, based on the registered ones, as suggested in https://github.com/kubernetes-sigs/kueue/issues/4659#issuecomment-2732301613.

Now, when it comes to the external controller, options I see:
1. as suggested by Yuki to use Kueue as a library, but it has drawbacks
2. add the format validation in the 3rd-party controller itself

I would be welcome the PR to Kueue for strict validation, but would probably be leaning to (2.) for the 3rd party controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T11:29:36Z

> I would suggest avoiding the operator requiring Kueue as a library apart from for particular API types (which should have minimal imports), as importing large parts of the codebase can lock dependencies and make it difficult for the operator developer. eg they want to move their deps up to a new version of controller-runtime, but Kueue hasn't cut a release with that version yet, so they can't

if we double manage the Enum list in this repository, the operator need to use Kueue as a library since they need to obtain the Enum list from Kueue codes. Or do you indicate the HTTP endpoint else to obtain the integrations list?

### Comment by [@JoelSpeed](https://github.com/JoelSpeed) — 2025-03-18T12:01:18Z

I agree that 2 is the approach for a third party controller. I think the important part is that Kueue should enforce the restriction on newly registered integrations, to ensure that if a third party controller adds the qualified name based validation (for immediate feedback), that future integrations continue to meet the same format

The main goal here is not to provide perfect feedback, that comes with a lot of toil, but to weed out obviously incorrect issues, eg Pod instead of pod

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-18T15:32:47Z

So I opened up https://github.com/kubernetes-sigs/kueue/pull/4676 as an option.

It ended up being kinda of a large change to enforce the use of these integrations as they are used in a lot of places.

I think my PR makes it clear but I'm open if we want to reduce the scope to only be a quick validation.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-16T15:49:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-16T16:43:42Z

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
