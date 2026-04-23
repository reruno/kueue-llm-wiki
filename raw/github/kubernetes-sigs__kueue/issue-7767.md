# Issue #7767: v1beta2: Ignore "enable: true" in the configMap for FairSharing and WaitForPodsReady

**Summary**: v1beta2: Ignore "enable: true" in the configMap for FairSharing and WaitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7767

**Last updated**: 2025-11-27T18:50:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-19T16:08:11Z
- **Updated**: 2025-11-27T18:50:58Z
- **Closed**: 2025-11-27T18:44:38Z
- **Labels**: _none_
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 13

## Description

For v1beta2 we have removed the enable field for FairSharing and WaitForPodsReady in the PRs:
- https://github.com/kubernetes-sigs/kueue/pull/7628
- https://github.com/kubernetes-sigs/kueue/pull/7583

as part of https://github.com/kubernetes-sigs/kueue/issues/7113

However, this means that users may experience a complication on upgrade if they forget to remove "enable: true" it will not get parsed.

I would like to parse the configMap, but specifically ignore "enable: true" for the features without error. We could just log a warning.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T16:08:52Z

This is inspired by discussion with @mwielgus 
cc @PBundyra  @tenzen-y 

/assign @mbobrovskyi 
who I know is already looking into that

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T16:10:07Z

cc @kannon92

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-19T16:14:32Z

@mimowo I'm wondering if we should keep the enable field as I mentioned in https://github.com/kubernetes-sigs/kueue/pull/7628.
The primary reason is that the way to enable waitForPodsReady and FairSharing with the default value is `waitForPodsReady: {}` / `fairSharing: {}`.

For `waitForPodsReady`, we can just re add enable field, but for `fairSharing`, we probably should revisit object structure to avoid confusion when they want to enable fairSharing and AFS.

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T16:20:34Z

tbh I dont see any difference between waitForPodsRady and fairSharing in that regard. So I would propose:
1. find a way to ignore enable as mentioned in the Issue for both features
2. rollback the PRs for both features

I dont have a strong view. As I synced with @mwielgus his opinion was also to do one of the two

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T06:47:32Z

We discussed this yesterday at wg-batch, and the sentiment was that (1.) was great, but there was no objection about the change anyway. 

So, seems like we wouldn't need to rollback the change even if we don't find a solution for (1.).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-26T09:21:35Z

> We discussed this yesterday at wg-batch, and the sentiment was that (1.) was great, but there was no objection about the change anyway.

@mimowo I was offline at the beginning of the meeting. So, I'm still wondering if we should re introduce `enabled` field to `waitForPodsReady`, `fairSharing`, and `asmissionFairSharing` for enabling those features with default parameters.

```yaml
waitForPodsReady:
  enabled: true
...
fairSharing:
  enabled: true
...
admissionFairSharing:
  enabled: true
...
```

In the current v1beta2, users need to have a wierd value `{}` for enabling functionalities with default parameters:


```yaml
waitForPodsReady: {}
...
fairSharing: {}
...
admissionFairSharing: {}
...
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T12:45:09Z

> So, I'm still wondering if we should re introduce enabled field to waitForPodsReady, fairSharing, and asmissionFairSharing for enabling those features with default parameters.

The fields used to be named "enable", so I wouldn't rename to "enabled", because this still means complications on upgrade.

> In the current v1beta2, users need to have a wierd value {} for enabling functionalities with default parameters:

I don't think this is a real issue though. In my practice I haven't seen a deployment like 
```yaml
waitForPodsReady:
  enable: true
```
relying just on defaults. In all cases I've seen people would uncomment https://github.com/kubernetes-sigs/kueue/blob/main/config/components/manager/controller_manager_config.yaml#L26-L34, and tweak some values.

I for users how really want use defaults, we could also just add a comment to use  `waitForPodsReady: {}`, but I think such users are really limited. Admins usually need to tweak the values anyway.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T15:02:35Z

Also note that we have many other features like: `DeviceClassMappings`, `MultiKueue`, `WorkloadRetentionPolicy` etc. which don't use `enable(d)` field, but potentially could.  So I think it is more consistent to drop the `enable` field all together for all features.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T11:28:39Z

I discussed these fields with @mimowo offline.
As a conclusion, we decided to make `.waitForPodsReady.timeout` and `.fairSharing.preemptionStrategies` required fields.

- https://github.com/kubernetes-sigs/kueue/blob/8878f881dedf6bf74ddc1d68770438a5884f34fb/apis/config/v1beta2/configuration_types.go#L224
- https://github.com/kubernetes-sigs/kueue/blob/8878f881dedf6bf74ddc1d68770438a5884f34fb/apis/config/v1beta2/configuration_types.go#L515

The `waitForPodsReady` and `fairSharing` fields represent how to enable those features and their optional parameters. (Mixed Responsibility)
But the `multiKueue` is responsible only for representing their optional parameters. (Single Responsibility)

So, I argued to introduce the `enabled` fields to `waitForPodsReady` and `fairSharing`.
But, as opposed to adding `enabled` fields, if we can make one field required, the field could be `Single Responsibility` since it will represent only their parameters, which could eliminate the possibility for `waitForPodsReady: {}` and `fairSharing: {}` when enabling those features.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-27T11:30:03Z

^ cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-27T11:31:05Z

SGTM

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T18:44:33Z

/close
completed as mentioned above in the referenced PRs

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-27T18:44:39Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7767#issuecomment-3587023671):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
