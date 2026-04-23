# Issue #5637: Generate the Helm chart documentation using the helm-docs tool

**Summary**: Generate the Helm chart documentation using the helm-docs tool

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5637

**Last updated**: 2025-06-13T17:04:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kaisoz](https://github.com/kaisoz)
- **Created**: 2025-06-12T19:50:01Z
- **Updated**: 2025-06-13T17:04:57Z
- **Closed**: 2025-06-13T17:04:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Use the [helm-docs](https://github.com/norwoodj/helm-docs/) tool to generate the helm chart documentation

**Why is this needed**:
Currently, the Helm chart `README` file needs to be updated manually on each chart change. The [helm-docs](https://github.com/norwoodj/helm-docs/) tool would automate this by generating the`README.md` file out of a combination of a gotemplate and a comments in the `values.yaml` file.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-13T11:16:07Z

/assign
