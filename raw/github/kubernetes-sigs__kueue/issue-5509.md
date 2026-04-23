# Issue #5509: webhook mutation failure

**Summary**: webhook mutation failure

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5509

**Last updated**: 2025-06-08T13:52:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@likku123](https://github.com/likku123)
- **Created**: 2025-06-05T04:29:25Z
- **Updated**: 2025-06-08T13:52:56Z
- **Closed**: 2025-06-08T13:52:56Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

Tried testing in 0.12.1 and 0.12.2

In helm chart when enabled

enableCertManager: True

I get the below failure.

Error from server (InternalError): error when creating "0-resource-flavour.yaml": Internal error occurred: failed calling webhook "mresourceflavor.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-kueue-x-k8s-io-v1beta1-resourceflavor?timeout=10s": tls: failed to verify certificate: x509: certificate signed by unknown authority


When tried with internalCertManagement: true. It works perfect.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T04:56:22Z

Thank you for reporting.

afaik we have E2e tests for cert manager so I would assume it is a configuration issue (and there are some manual steps involved). 

Did you try following the steps on https://kueue.sigs.k8s.io/docs/tasks/manage/productization/cert_manager/?

cc @kannon92

### Comment by [@likku123](https://github.com/likku123) — 2025-06-05T09:09:40Z

Yes, I have followed exact steps.

In my initial installation it worked fine but after the multiple uninstall and deployment of Kueue web hook mutation starts failing when I tried to create the Kueue resources (resource-flavour,cluster queues)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-05T09:15:09Z

Is the Kueue deployment itself available ? Maybe check `kubectl describe  deploy -nkueue-system` and `kubectl describe pods -nkueue-system`.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-05T11:19:13Z

Do you update the config map in the helm chart to not use internalCertManager?

https://github.com/kubernetes-sigs/kueue/blob/9515191febbcbc2017ed39b514caddea9240abcb/charts/kueue/values.yaml#L102

You have to uncomment that and set it it to false.

### Comment by [@likku123](https://github.com/likku123) — 2025-06-08T13:52:56Z

That did the trick . Thank you !
