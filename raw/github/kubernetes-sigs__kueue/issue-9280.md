# Issue #9280: MultiKueue SA tokens expire after 24 hours in a local development environment

**Summary**: MultiKueue SA tokens expire after 24 hours in a local development environment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9280

**Last updated**: 2026-03-03T17:41:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kshalot](https://github.com/kshalot)
- **Created**: 2026-02-16T10:37:02Z
- **Updated**: 2026-03-03T17:41:29Z
- **Closed**: 2026-03-03T17:41:29Z
- **Labels**: `kind/cleanup`, `area/multikueue`
- **Assignees**: [@polinasand](https://github.com/polinasand)
- **Comments**: 16

## Description

**What would you like to be cleaned**:
When using the [`setup-kind-multikueue-tas.sh`](https://github.com/kubernetes-sigs/kueue/blob/9fd2597755e55160dc976866b1f2254f37d0c8bf/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh) script from the site docs, MultiKueue stops working after 24 hours. This is due to the service account token being generated for 24 hours:
https://github.com/kubernetes-sigs/kueue/blob/9fd2597755e55160dc976866b1f2254f37d0c8bf/site/static/examples/multikueue/dev/setup-kind-multikueue-tas.sh#L155

The token's lifespan cannot be arbitrarily increased since it seems to be capped at 48 hours:
```sh
Warning: requested expiration of 2592000 seconds shortened to 172800 seconds
```

The token can be easily rotated with a script. It should be explicitly mentioned in the documentation that the token needs to be rotated.

**Why is this needed**:
1. To make the development experience simpler.
2. To make sure users that are testing out the capabilities of MultiKueue don't get discouraged by seemingly random failures.

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:40:18Z

I'd also add a well-spottable ASCII call-out printed at the bottom from the main script.
Sth like "remember to rotate your tokens with [script-name] every 24h".

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T10:50:58Z

Nice finding, since this is just for Kind testing development I see no risk for extending period. 

I would probably set a week - 7*24h, wdyt?

> The token can be easily rotated with a script.

If we need to rotate the token then we should add the script under the ./hack directory and mention which one to use, or what command to use. Otherwise most people will just re-create the cluster.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:52:23Z

> I would probably set a week - 7*24h, wdyt?

It's capped to 172800 seconds = 48h by the system (as the error message posted by @kshalot above says)

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:53:18Z

/area multikueue

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-16T10:54:49Z

> It's capped to 172800 seconds = 48h by the system (as the error message posted by @kshalot above says)

In that case I would suggest:
1. set it 48h by default
2. print out some info that it is going to expire, and the command to re-generate the tokens

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-24T09:51:03Z

Actually, maybe there's a way to create a long-lived token:
https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#manually-create-a-long-lived-api-token-for-a-serviceaccount

Sth like:
```sh
cat <<EOF | kubectl --context "kind-${cluster}" apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: multikueue-sa-token
  namespace: kueue-system
  annotations:
    kubernetes.io/service-account.name: "multikueue-sa"
type: kubernetes.io/service-account-token
EOF

TOKEN=$(kubectl --context "kind-${cluster}" get secret multikueue-sa-token -n kueue-system -o jsonpath='{.data.token}' | base64 --decode)
```

I think this one won't ever expire. It might require a `sleep N` after the `kubectl apply` to populate the secret properly though.

This way we don't need to rotate it.

/assign polinasand

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-24T09:51:06Z

@kshalot: GitHub didn't allow me to assign the following users: polinasand.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9280#issuecomment-3950435391):

>Actually, maybe there's a way to create a long-lived token:
>https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#manually-create-a-long-lived-api-token-for-a-serviceaccount
>
>Sth like:
>```sh
>cat <<EOF | kubectl --context "kind-${cluster}" apply -f -
>apiVersion: v1
>kind: Secret
>metadata:
>  name: multikueue-sa-token
>  namespace: kueue-system
>  annotations:
>    kubernetes.io/service-account.name: "multikueue-sa"
>type: kubernetes.io/service-account-token
>EOF
>
>TOKEN=$(kubectl --context "kind-${cluster}" get secret multikueue-sa-token -n kueue-system -o jsonpath='{.data.token}' | base64 --decode)
>```
>
>I think this one won't ever expire. It might require a `sleep N` after the `kubectl apply` to populate the secret properly though.
>
>This way we don't need to rotate it.
>
>/assign polinasand


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@polinasand](https://github.com/polinasand) — 2026-02-24T09:52:32Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-24T09:59:45Z

Thank you @kshalot and @polinasand for moving this forward.

Both expiring after 48h. "Never expiring" is ok-ish for our test environments on Kind, but I'm a bit hesitant because maybe some folks will just copy-paste our test setup as their prod setup. 

So, maybe we could figure out setting 1 month- it will give developers more than enough time to work on a feature, while mitigate the risk of some users blindly copy-pasting the setup. 

Alternatively we could use "never expire", and just add a warning in the file.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-24T10:08:22Z

Valid point @mimowo.

I also found [this](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/):
> **--service-account-max-token-expiration duration**
The maximum validity duration of a token created by the service account token issuer. If an otherwise valid TokenRequest with a validity duration larger than this value is requested, a token will be issued with a validity duration of this value.

Maybe using [kubeadm patches in kind](https://kind.sigs.k8s.io/docs/user/configuration/#kubeadm-config-patches) we could extend the max lifespan of the token? Then the script remains exactly the same (just increase 24h to sth larger) and the main change is in the `kind` config that is applied, so it's localized to dev setups only. Something like:
```
kubeadmConfigPatches:
- kind: ClusterConfiguration
  apiServer:
    extraArgs:
      service-account-max-token-expiration: "100000h"
```

### Comment by [@polinasand](https://github.com/polinasand) — 2026-02-25T11:08:12Z

I would proceed with using kubeadm patch in `kind` to extend max token expiration to `7d`, and setting duration for `TOKEN` to `7d` as well. Another question is should the docs be updated accordingly: https://kueue.sigs.k8s.io/docs/tasks/dev/setup_multikueue_development_environment/

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-25T11:26:41Z

Two points about the token expiry/docs:

1. Since this would be scoped to a development setup quite clearly, maybe we could make it even longer than 7 days? I'm not sure how long do people keep their kind clusters around.
2. Unless we set the expiry date to something that's pretty much "never expire" (like a year), there might still be risk that the token expires, so it could be worth mentioning it in the docs, especially if we set it to 7 days like proposed. Then we might need a rotation script as well.
---
But there's another angle here - we shipped `E2E_MODE=dev` as a way to conveniently keep the cluster around between E2E test runs. I think this might be affected as well:

The token is set to 1 hour:
https://github.com/kubernetes-sigs/kueue/blob/85957d4ab8e4c2bdd1de40b4bfb3d72cfec0933f/test/util/multikueue.go#L155-L160

If the secret already exists, it will ignore the "AlreadyExists" error so the secret with the new token won't be created I think:
https://github.com/kubernetes-sigs/kueue/blob/85957d4ab8e4c2bdd1de40b4bfb3d72cfec0933f/test/util/multikueue.go#L213-L220

So the `E2E_MODE=dev` setup might also stop working after an hour. cc @vladikkuzn @mimowo

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-25T11:32:25Z

>I would proceed with using kubeadm patch in kind to extend max token expiration to 7d, and setting duration for TOKEN to 7d as well.

@polinasand Regardless of my previous comment, I'd definitely proceed with that for the `setup-kind-multikueue-tas.sh` since it's independent from the `E2E_MODE`. We can decide upon the expiry time later as well, but it would be good to confirm that this approach will work.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T11:35:39Z

> Since this would be scoped to a development setup quite clearly, maybe we could make it even longer than 7 days? I'm not sure how long do people keep their kind clusters around.

TBH I would keep them only for 1 day, max two. It is so cheap to provision a new one, when I have issues with the old cluster I just provision a new one :) 

> Unless we set the expiry date to something that's pretty much "never expire" (like a year), there might still be risk that the token expires, so it could be worth mentioning it in the docs, especially if we set it to 7 days like proposed. Then we might need a rotation script as well.

I'm ok with a value greater than 7 days, as long as we add a clear comment with a warning before copy-pasting to production setups. 

> If the secret already exists, it will ignore the "AlreadyExists" error so the secret with the new token won't be created I think:

Good spot 👍 I think we should just update the code to extend ExpirationSeconds to match the secret lifetime, or re-create it here. I think for the dev setup we have full freedom. Seems like extending the ExpirationSeconds is easier.

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-25T12:05:38Z

> TBH I would keep them only for 1 day, max two. It is so cheap to provision a new one, when I have issues with the old cluster I just provision a new one :)

I was thinking that since this will be enabled via a kind configuration, it would be less likely for people to replicate in their "real" clusters. But it just hit me that unless they are using the `ClusterProfile` integration they will need rotation as well so it might be  easy to just patch kubeadm like we do and make it last super long, so your are making a good point. For a second I thought that this `kubeadmConfigPatches` in kind would scream "development" but since we do not document this anywhere it might be too suggestive.

**But** right now our [docs](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/) propose creating a secret-based token which is **long-lived** ([k8s docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#manually-create-a-long-lived-api-token-for-a-serviceaccount)). So @mimowo we already have the problem you mentioned. I think this should be addressed (#9032). Relevant snippet in the docs:
```md
...
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: ${MULTIKUEUE_SA}
  namespace: ${NAMESPACE}
  annotations:
    kubernetes.io/service-account.name: "${MULTIKUEUE_SA}"
EOF
...
```

I'd propose the following action points:
1. `setup-kind-multikueue-tas.sh`:
    1. Make the token expire in 48h (the default max).
    2. Introduce a script that will rotate the token.
    3. Document the rotation in the [dev docs](https://kueue.sigs.k8s.io/docs/tasks/dev/setup_multikueue_development_environment/).
2. Documentation:
    1. Explicitly document the kubeconfig based authentication with token + rotation and an "unsafe" long-lived secret.
3. `E2E_MODE=dev`:
    1. Extend `service-account-max-token-expiration` for the workers and create a token that lives longer. Or migrate to the long-lived secret.


@polinasand I think point 1 and 3 could be done as part of this issue, to avoid having to re-create the cluster.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T12:20:35Z

> But right now our [docs](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/) propose creating a secret-based token which is long-lived ([k8s docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#manually-create-a-long-lived-api-token-for-a-serviceaccount)). So @mimowo we already have the problem you mentioned.

Yeah, I remember that now, and I'm pretty sure some folks already copied that into their prod/non-dev setups. 

That is ok, we don't need to solve everything in one go. Still, in the long run I would suggest promoting secret / token promotion in documentation. Or at least adding a warning.

> I'd propose the following action points:

(1.) and (3.) sound good to me, actionable here.

For (2.) I agree - we might re-visit the documentation. I think it would be good to show how to configure expiring secrets and tokens, and what is our recommendation. the defaults we put are less relevant.
