# Issue #226: Rename image to registry.k8s.io/kueue/kueue

**Summary**: Rename image to registry.k8s.io/kueue/kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/226

**Last updated**: 2022-05-09T19:44:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-04-20T15:01:27Z
- **Updated**: 2022-05-09T19:44:34Z
- **Closed**: 2022-05-09T19:44:34Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 3

## Description

**What would you like to be cleaned**:

Rename images from `k8s.gcr.io/kueue/kueue` to `registry.k8s.io/kueue/kueue` for the next release.

**Why is this needed**:

https://groups.google.com/a/kubernetes.io/g/dev/c/DYZYNQ_A6_c/m/oD9_Q8Q9AAAJ?utm_medium=email&utm_source=footer

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-07T17:23:29Z

/assign @ArangoGutierrez 

Eduardo, do you want to take this one?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-05-09T13:58:03Z

Hey sure, an easy one to return after a long PTO

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-05-09T14:41:55Z

Step 1, verify:

```bash
[eduardo@fedora-workstation k8s.io]$ skopeo list-tags docker://k8s.gcr.io/kueue/kueue
{
    "Repository": "k8s.gcr.io/kueue/kueue",
    "Tags": [
        "sha256-430bb4d26a05e4de56e3e10d8bc5ebb8de28f77d575d99a4cacc8edadcf7567b.sig",
        "v0.1",
        "v0.1.0"
    ]
}
[eduardo@fedora-workstation k8s.io]$ skopeo list-tags docker://registry.k8s.io/kueue/kueue
{
    "Repository": "registry.k8s.io/kueue/kueue",
    "Tags": [
        "sha256-430bb4d26a05e4de56e3e10d8bc5ebb8de28f77d575d99a4cacc8edadcf7567b.sig",
        "v0.1",
        "v0.1.0"
    ]
}
```
