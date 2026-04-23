# Issue #9289: MultiKueue development setup relies on `MultiKueueAllowInsecureKubeconfigs`

**Summary**: MultiKueue development setup relies on `MultiKueueAllowInsecureKubeconfigs`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9289

**Last updated**: 2026-02-17T12:45:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2026-02-16T13:38:14Z
- **Updated**: 2026-02-17T12:45:06Z
- **Closed**: 2026-02-17T12:45:06Z
- **Labels**: `priority/important-soon`, `kind/cleanup`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be cleaned**:

The MultiKueue development configuration seems to rely on the `MultiKueueAllowInsecureKubeconfigs` feature gate being active. This is because the generated Kubeconfig is using `insecure-skip-verify-tls`:
https://github.com/kubernetes-sigs/kueue/blob/79fcc7335cc48b19caa0eb77626f30e002f93afd/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh#L163

The removal of this flag would break this setup.

I'm not sure whether the e2e tests for MultiKueue rely on this configuration option. Either they need to be aligned as well or they can serve as an example of how to set up the TLS for the Kind deployment.

**Why is this needed**:

The `MultiKueueAllowInsecureKubeconfigs` feature gate is set to be removed in `0.17.0`:
https://github.com/kubernetes-sigs/kueue/blob/79fcc7335cc48b19caa0eb77626f30e002f93afd/pkg/features/kube_features.go#L191

## Discussion

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-16T13:38:24Z

/priority important-soon
/area multikueue

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:45:45Z

Thank you for reporting that. 

> I'm not sure whether the e2e tests for MultiKueue rely on this configuration option. Either they need to be aligned as well or they can serve as an example of how to set up the TLS for the Kind deployment.

Yeah, I cannot recall why MultiKueue e2e tests use this flag - we should not need to do that. Maybe @mszadkow can recall that? I suppose it might be because for tests we self-sign the certificates, and maybe this is considered insecure? I think this is something where we could consider relaxing our expectations / verification.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T13:46:58Z

For now this effectively blocks dropping the FG which is anti-pattern.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-16T15:01:47Z

> Yeah, I cannot recall why MultiKueue e2e tests use this flag - we should not need to do that.

I don't think this flag is used in e2e tests (I did a [quick search](https://github.com/search?q=repo%3Akubernetes-sigs%2Fkueue%20MultiKueueAllowInsecureKubeconfigs&type=code)). From what I can see, the kubeconfigs generated for the e2e tests do not have `insecure-skip-verify-tls`:
https://github.com/kubernetes-sigs/kueue/blob/afe666df7d41600f8c6e8a939c225bae3bd5a510/test/util/multikueue.go#L168-L171

The dev setup is not setting the CA data at all so tweaking this **could** solve the issue:
https://github.com/kubernetes-sigs/kueue/blob/79fcc7335cc48b19caa0eb77626f30e002f93afd/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh#L161-L165

So potentially this wouldn't block the removal of the gate, if it's a simple fix.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-02-16T16:18:54Z

Yes, this is not being used in e2e tests, I also checked.
We did that one for backward-compatibility for user that didn't adapt their config yet.
However we recommend to use this for MultiKueue and TAS setup  - https://github.com/kubernetes-sigs/kueue/blob/main/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh
But I believe it's just to simplify the configuration, we might want to update that with TLS and we can drop this flag completely.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-02-16T16:26:09Z

/cc @IrvingMg is that correct?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T16:34:48Z

I guess the best path forward is for someone to try making the changes (prototype) and we will see if we are missing something or not.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T16:49:03Z

I think the key question is: are the KubeConfigs we generate for MultiKueue dev setup passing validation when `MultiKueueAllowInsecureKubeconfigs=false`. 

If they pass the validation, then I'm pretty sure dropping the FG should be easy, we just need to tweak the conditions under which we set `insecure-skip-tls-verify: true` so that it does not depend directly on the  `MultiKueueAllowInsecureKubeconfigs` FG

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-02-16T16:56:07Z

> /cc [@IrvingMg](https://github.com/IrvingMg) is that correct?

Yes, the script https://github.com/kubernetes-sigs/kueue/blob/main/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh focuses on demonstrating the Multikueue + TAS setup and was added in https://github.com/kubernetes-sigs/kueue/pull/7712 as a guide for developers. It was not intended to exemplify a production-ready setup.

Still, if we want to remove `MultiKueueAllowInsecureKubeconfigs`, I guess we can use the same script to validate that it still works.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-02-16T17:02:45Z

> I think the key question is: are the KubeConfigs we generate for MultiKueue dev setup passing validation when `MultiKueueAllowInsecureKubeconfigs=false`.
> 
> If they pass the validation, then I'm pretty sure dropping the FG should be easy, we just need to tweak the conditions under which we set `insecure-skip-tls-verify: true` so that it does not depend directly on the `MultiKueueAllowInsecureKubeconfigs` FG

Yes, they pass.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-16T17:54:47Z

https://github.com/kubernetes-sigs/kueue/pull/9297#issuecomment-3909618032

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-17T09:12:57Z

> Yes, they pass.

But doesn't this script explicitly set `insecure-skip-verify-tls`?
https://github.com/kubernetes-sigs/kueue/blob/e9c6db2352724382ec52240778ca5327fd731d30/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh#L163

I don't think this will pass validation:

https://github.com/kubernetes-sigs/kueue/blob/e9c6db2352724382ec52240778ca5327fd731d30/pkg/controller/admissionchecks/multikueue/multikueuecluster.go#L523-L526

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-17T10:22:32Z

Unless you meant that they pass if we remove `insecure-skip-tls-verify`, I'm not fully following the conversation.

Anyways, PTAL at #9312. I was running MultiKueue locally anyway, so I tested out my fix. Seems to have worked.
