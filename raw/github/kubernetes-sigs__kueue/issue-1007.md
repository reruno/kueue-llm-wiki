# Issue #1007: Organize tasks under personas

**Summary**: Organize tasks under personas

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1007

**Last updated**: 2023-08-29T18:11:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-21T14:34:15Z
- **Updated**: 2023-08-29T18:11:23Z
- **Closed**: 2023-08-29T18:11:23Z
- **Labels**: `kind/feature`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What would you like to be added**:

/kind documentation

Organize the tasks documentation under 3 personas. Maybe this can be implemented using [hugo taxonomies](https://gohugo.io/content-management/taxonomies/)

- Application Developer (previously known as Batch User)
- Batch Ops (previously known as Batch Admin)
- Platform Developer (new)

Caveats:
- In smaller organisations, Batch Ops and Platform developer could be the same person/team.
- Some tasks might apply to more than one persona. For example, an application developer might want to run their jobs through python. Whereas the platform developer might want to develop some tools for Kueue using python as well. Here is where tags could help to list one tutorial under multiple personas.

**Why is this needed**:

As the number of tasks grows, it's useful to have some separation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-21T14:34:43Z

cc @moficodes @alizaidis
