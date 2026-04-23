# Issue #745: Add helm-chart-releaser workflow

**Summary**: Add helm-chart-releaser workflow

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/745

**Last updated**: 2023-07-07T13:27:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Gekko0114](https://github.com/Gekko0114)
- **Created**: 2023-05-04T23:47:55Z
- **Updated**: 2023-07-07T13:27:06Z
- **Closed**: 2023-07-07T13:27:06Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 14

## Description

**What would you like to be added**:
A Helm-chart-releaser workflow
**Why is this needed**:
We want to automatically create a Helm chart when releasing a new version of Kueue.

**Completion requirements**:
Add helm-chart-releaser and verify it works correctly.
This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

Related to https://github.com/kubernetes-sigs/kueue/pull/664, https://github.com/kubernetes-sigs/kueue/pull/744

## Discussion

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-05-04T23:53:33Z

When I have free time, I will work on it.
However, if anyone else is interested in this issue, they are welcome to take it on.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-05T12:16:30Z

Do we need this? Can't we include the artifacts in the same release as the yamls? Like this 
![image](https://user-images.githubusercontent.com/1299064/236455312-f03b872d-8067-446e-913e-2e43883cdb1f.png)

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-05-06T05:27:17Z

I see. I agree with you.
Since artifacts already include helm charts, we don't need to do additional tasks for this.
Maybe we need to update helm chart's README.md file.

### Comment by [@rptaylor](https://github.com/rptaylor) — 2023-06-21T21:37:39Z

How could publishing the helm chart as an asset file in the github release would work?
In order to install from a traditional (https) Helm repo there has to also be an index.yaml file, and the repo should include all the releases in one place. Actually you can do this with github-pages by just copying the chart directory into place, running `helm package  chartdir/` to create the tarballs and update index.yaml, and then push.

For publishing charts in the OCI format I think there still has to be an index.yaml file, and in any case the URL must be of the form `oci://registry/namespace/chart-name`

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T12:10:11Z

We have a site in https://kueue.sigs.k8s.io

Are you saying that we could publish the index in `https://kueue.sigs.k8s.io/index.yaml`?

### Comment by [@rptaylor](https://github.com/rptaylor) — 2023-06-22T19:10:37Z

> Are you saying that we could publish the index in `https://kueue.sigs.k8s.io/index.yaml`?

The index and the tarballs, sure. Probably it should be more like https://kueue.sigs.k8s.io/helm/repo/index.yaml  or something like that but yeah.  My very simple and basic way of publishing a repo that hardly anyone uses with github pages is:

https://rptaylor.github.io/kapel/

https://github.com/rptaylor/kapel/tree/gh-pages

You might want something that can automatically publish charts via git actions or something but I don't know about that github stuff, I mostly use gitlab.

### Comment by [@rptaylor](https://github.com/rptaylor) — 2023-06-22T19:26:06Z

Probably https://github.com/marketplace/actions/helm-chart-releaser  would be useful?
Or with the new OCI format of Helm charts you can store them in a OCI registry , like container images.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T20:25:18Z

We don't use github pages, so they wouldn't work for us.

But we can probably copy the files into the /site assets somehow.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-22T20:29:10Z

we could also use our registry `registry.k8s.io/kueue/`, maybe using cloudbuild https://github.com/kubernetes-sigs/kueue/blob/main/cloudbuild.yaml

In any case, I'm happy to review a PR along these lines.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-04T17:34:39Z

I think we should go the path of OCI and publish in registry.k8s.io. I'm asking sig-release on Slack whether there is a documented process for this. But I suspect we might be able to follow the general process for images https://github.com/kubernetes/k8s.io/tree/main/registry.k8s.io

### Comment by [@Borrelhapje](https://github.com/Borrelhapje) — 2023-07-05T07:02:41Z

I've noted that the release of a helm chart usually happens more often than a new release of the actual application, especially when the chart is quite new. Helm supports this using the Chart.Version (for the chart itself) and Chart.AppVersion (often used as a default image tag).

You could consider a workflow that allows releasing the chart by itself, without releasing a new version of the Kueue image.

### Comment by [@Gekko0114](https://github.com/Gekko0114) — 2023-07-05T10:14:52Z

I am not familiar with helm chart's normal release process, 
so it would be great if you create good release process 😀

### Comment by [@trasc](https://github.com/trasc) — 2023-07-07T09:08:35Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-07-07T09:16:13Z

#956 adds the generation of the helm package along with the rest of the artifacts.
For now this should be sufficient since helm should be able to  install a chart (.tgz) by it's absolute path or URL.

Ye can look into adding a repo (index.yaml) in the website that points to the release artifact url, but we need to host the chart there first.
