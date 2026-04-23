# Issue #9032: MultiKueue: re-organize and cleanup the page for setup

**Summary**: MultiKueue: re-organize and cleanup the page for setup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9032

**Last updated**: 2026-02-16T10:45:45Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T15:12:29Z
- **Updated**: 2026-02-16T10:45:45Z
- **Closed**: —
- **Labels**: `kind/documentation`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template for documentation-related issues -->

**What would you like to be documented or improved**:

Re-organize the landing page for MultiKueue setup so that it is more user-friendly and less scary for new users.

This was raised in a PR review: https://github.com/kubernetes-sigs/kueue/pull/9018/changes#r2774503335

**Location** (URL, file path, or section if applicable):

https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T15:12:45Z

cc @kannon92 @olekzabl @kshalot

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-06T15:18:46Z

Yea I think things like ClusterProfiles/ClusterInventor may need to move to MultiKueue concepts.

Seems that it is becoming a more important functionality for MK.

Plus we may want to think through how to link to cloud provider setup for MK (gcp / OCM/ etc).

### Comment by [@kshalot](https://github.com/kshalot) — 2026-02-06T16:45:39Z

Fully agree. 

> One way to achieve that on a Kind cluster, and I think super easy is to use E2E_MODE=dev make kind-image-build test-multikueue-e2e, and voila :)

I made some **very simple** efforts to surface the quickest ways to set up MultiKueue in https://github.com/kubernetes-sigs/kueue/pull/8660, which includes the `E2E_MODE=dev` approach, but the overall structure of the docs is still all over the place. For example there is ["setup multikueue environment"](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_multikueue/) and ["setup multikueue development environment"](https://kueue.sigs.k8s.io/docs/tasks/dev/setup_multikueue_development_environment/). There's a lot of overlap between them.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-12T09:16:59Z

FTR, I'm feeling 2 kinds of rearrangement would make these docs more useful:

- Keep long Bash scripts (most notably, `create-multikueue-kubeconfig.sh`) out of the main page. (I mean, just leave a link).
  They clutter the doc, while I'd guess most reader won't need to see them, at least not right away.

- Clearly separate between:
  
  - (A) the MultiKueue technical setup (kubeconfigs, MultiKueueConfigs etc.)
  - (B) Kueue test resources (ClusterQueues, LocalQuotas, Flavors etc.)
  - (C) the tiny bit connecting the two (i.e. the MultiKueue AdmissionCheck applied to ClusterQueue(s))
  
  Because I think (or is it just me?) that manually playing with Kueue typically involves keeping (A+C) unchanged while tweaking (B) in various ways.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-12T09:20:47Z

Also, for simplest journeys, I'd add a step to disable "non-core" integrations in Kueue config, at least on the manager side.

(Otherwise, just installing Kueue on the workers leads to a non-working MultiKueue setup - because MultiKueue expects every integration enabled on the manager to be _fully operational_ on workers, which requires installing additional stuff. For simplest experimenting, it's an unnecessary hassle).

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:45:42Z

/area multikueue
