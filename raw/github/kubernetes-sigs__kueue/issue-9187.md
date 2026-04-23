# Issue #9187: Use replacements instead of vars in config/default

**Summary**: Use replacements instead of vars in config/default

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9187

**Last updated**: 2026-02-21T11:29:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-02-12T17:56:38Z
- **Updated**: 2026-02-21T11:29:39Z
- **Closed**: 2026-02-21T11:29:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@TapanManu](https://github.com/TapanManu)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

When running `kustomize build config/default/` with CertManager enabled, we see the following warning:

```
# Warning: 'vars' is deprecated. Please use 'replacements' instead. [EXPERIMENTAL] Run 'kustomize edit fix' to update your Kustomization automatically.
2026/02/12 19:48:34 well-defined vars that were never replaced: VISIBILITY_CERTIFICATE_NAMESPACE,CERTIFICATE_NAME,CERTIFICATE_NAMESPACE,VISIBILITY_CERTIFICATE_NAME
```

**Why is this needed**:

To avoid using a deprecated feature, and as mentioned [here](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/vars/), it will not be included in the kustomize.config.k8s.io/v1 Kustomization API.

**How to reproduce it (as minimally and precisely as possible)**:

1. config/default/kustomization.yaml: uncomment certmanager resource, prometheus resource, and the vars: block
2. config/components/prometheus/kustomization.yaml: uncomment the patches: block

```
kustomize build config/default/
```

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-12T17:57:13Z

/cc @TapanManu @IrvingMg

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-13T17:02:43Z

+1

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-14T05:19:28Z

@mimowo @mbobrovskyi let me take a look at this 👍🏻 , could you assign this issue to me ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-14T09:33:11Z

You can assign yourself – just use the /assign command.

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-14T09:35:06Z

Thanks @mbobrovskyi

### Comment by [@TapanManu](https://github.com/TapanManu) — 2026-02-14T09:35:15Z

/assign
