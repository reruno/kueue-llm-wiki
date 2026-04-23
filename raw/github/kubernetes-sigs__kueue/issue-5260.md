# Issue #5260: Opt-in namespace approach for Kueue for all workloads

**Summary**: Opt-in namespace approach for Kueue for all workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5260

**Last updated**: 2025-08-03T19:20:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-05-15T16:25:37Z
- **Updated**: 2025-08-03T19:20:22Z
- **Closed**: 2025-08-03T19:20:22Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Provide a way for opt-in namespace approach for Kueue.

Expand `managedJobsNamespaceSelector` for all workloads.

**Why is this needed**:

For our openshift deployment of Kueue, we found that the only "safe" way to enable Kueue is only allow Kueue to manage resources in labeled namespaces for Kueue.

We find that there are admin namespaces and user namespaces. An admin namespace may be deploying operators/CRDs/Jobs and we do not want Kueue interfering with these resources. Namespaces are also dynamic.

For Openshift AI and MLBatch (IBM based Openshift AI) we find it is difficult to enable the Job integration. Many projects use batch jobs and these can be critical services like NFD or GPUOperator and we want to exclude kueue management from those.

In these projects we had to disable the batchJob integration as there is not a way to safely exclude batch jobs if you enable kueue to manage all batch jobs.

**Existing Issues**:

- https://github.com/kubernetes-sigs/kueue/issues/5244
- https://github.com/kubernetes-sigs/kueue/issues/4141

**Proposal**
I think this should be defined in a KEP but I wanted to sketch the idea here.

Expand `managedJobsNamespaceSelector` for all workloads.

It is true that if a user does not set `ManagedJobsWithoutQueueName=true`, then there will be a label present on a workload. This could be used in the webhook labelSelector but this does not help thouse who want kueue to manage all batch jobs.

Kueue has a clear idea how to do this via pod based integrations (namespaceSelector with `managedJobsWithoutNamespaceSelector`).

So our following setup:

a) Kueue based namespaces get labeled with a `managed-by-kueue: true` (naming TBD).
b) We set the `namespaceSelector` on all webhooks.
c) Webhooks only operate on namespaces with this label.


**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T16:26:53Z

cc @varshaprasad96 @dgrove-oss

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T17:00:58Z

> So our following setup:
> a) Kueue based namespaces get labeled with a managed-by-kueue: true (naming TBD).
> b) We set the namespaceSelector on all webhooks.
> c) Webhooks only operate on namespaces with this label.

It is not clear to me what is missing in this setup and what you want to change by "Expand managedJobsNamespaceSelector for all workloads.". 

I would be reluctant to further complicate the logic of determining if a job is managed by Kueue or not. The logic already getting quite complex, and requires exhaustive testing.

Be aware we graduate the LocalQueueDefaulting in 0.12. Maybe you could rely more on this?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T17:15:43Z

Right now, webhooks for suspend based workloads do not use a namespaceSelector for the webhook.

So I can probably experiment with this on my internal operator and I will have to do this.

Right now, the problem I have is that if I use a Job, kueue will manage any job that has the KueueName label. And even if a Job does not have the label, Kueue's webhooks are still used. 

For example, deployments webhook manifest:

```yaml
  - admissionReviewVersions:
      - v1
    clientConfig:
      service:
        name: '{{ include "kueue.fullname" . }}-webhook-service'
        namespace: '{{ .Release.Namespace }}'
        path: /mutate-apps-v1-deployment
    name: mdeployment.kb.io
    {{- if has "deployment" $integrationsConfig.frameworks }}
    failurePolicy: Fail
    {{- else }}
    failurePolicy: Ignore
    {{- end }}
    namespaceSelector:
      {{- if (hasKey $managerConfig "managedJobsNamespaceSelector") -}}
        {{- toYaml $managerConfig.managedJobsNamespaceSelector | nindent 6 -}}
      {{- else }}
      matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: NotIn
          values:
            - kube-system
            - '{{ .Release.Namespace }}'
      {{- end }}
    rules:
      - apiGroups:
          - apps
        apiVersions:
          - v1
        operations:
          - CREATE
          - UPDATE
        resources:
          - deployments
    sideEffects: None
    reinvocationPolicy: '{{ .Values.mutatingWebhook.reinvocationPolicy }}'
```

While suspend based (jobs, kubeflow, JobSet, etc):

```yaml
  - admissionReviewVersions:
      - v1
    clientConfig:
      service:
        name: '{{ include "kueue.fullname" . }}-webhook-service'
        namespace: '{{ .Release.Namespace }}'
        path: /mutate-batch-v1-job
    failurePolicy: Fail
    name: mjob.kb.io
    rules:
      - apiGroups:
          - batch
        apiVersions:
          - v1
        operations:
          - CREATE
        resources:
          - jobs
    sideEffects: None
    reinvocationPolicy: '{{ .Values.mutatingWebhook.reinvocationPolicy }}'
```

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T17:17:43Z

https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/#webhook-limit-scope

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-05-15T17:43:09Z

I think @kannon92 point is that we patch the webhooks for pods, deployments, and statefulsets to have a namespace selector [here](https://github.com/kubernetes-sigs/kueue/blob/6cbeab98c6c31b27e5a5093f91fcfded43282886/config/components/webhook/kustomization.yaml#L8-L38).
But we don't do that to the webhook for other kinds.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T18:06:31Z

It may also be a bit more than that because I see that PodWebhooks actually use `ManagedJobNamespaceSelector` while Job does not at all.

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_webhook.go#L77

### Comment by [@mtparet](https://github.com/mtparet) — 2025-05-23T12:20:43Z

https://github.com/kubernetes-sigs/kueue/pull/5323

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-30T18:23:39Z

There is still some work needed here to achieve what I want.

/reopen

We limit webhooks but the job reconcile will still unspend workloads if there is a label regardless of namespace.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-30T18:23:44Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5260#issuecomment-2923100869):

>There is still some work needed here to achieve what I want.
>
>/reopen
>
>We limit webhooks but the job reconcile will still unspend workloads if there is a label regardless of namespace.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-25T17:12:05Z

I tentatively add the issue to nice-to-haves for 0.13: https://github.com/kubernetes-sigs/kueue/issues/5713

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T19:20:22Z

Nice job @PannagaRao!

KEP and implementation are merged. Other than tracking this for beta, I don't think we need to keep this open.

/close
