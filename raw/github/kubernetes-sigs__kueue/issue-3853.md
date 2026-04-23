# Issue #3853: Add kueue-viz templates in helm charts

**Summary**: Add kueue-viz templates in helm charts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3853

**Last updated**: 2025-02-25T12:44:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@akram](https://github.com/akram)
- **Created**: 2024-12-16T08:25:03Z
- **Updated**: 2025-02-25T12:44:31Z
- **Closed**: 2025-02-25T12:44:31Z
- **Labels**: `kind/feature`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Installation of kueue-viz dashboard using kueue

**Why is this needed**:
Improve user experience by making installation of kueue-viz simple

**Completion requirements**:
Having the helm charts that allows installation of kueue-viz using helm; charts should allow to:
- select images to be used for frontend and backend
- set the number of replicas for each one
- enable use of tls required by the ingresses exposing backend and frontend

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@akram](https://github.com/akram) — 2024-12-16T08:27:07Z

Hi @mimowo and @mbobrovskyi 

I have created this issue just after the draft PR #3852 to discuss the requirements for the chart.
I have set a non comprehensive list of features that should be implemented by the chart. Maybe we can add some other basic ones here.

Also I wanted to discuss the location of the charts: should it be placed under `kueue` charts or under `cmd/experimental/kueue-viz` directory?

wdyt ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-16T08:44:47Z

Thanks @akram . 
1. is the dashboard to be running as a separate Pod or a container in Kueue? What are the pros and cons?
2. I would like to see the kueue-viz config [here](https://github.com/kubernetes-sigs/kueue/tree/main/config) first, then derive the helm charts based on the configs (this is the approach we do for prometheus or visibility API)
3. I'm fine either dedicated charts or opt-in under kueue - we are going to move the project eventually out of experimental anyway, so the question is how it is easier to develop. We can say in the charts that the opt-in flag enables an experimental feature.

### Comment by [@akram](https://github.com/akram) — 2024-12-16T17:33:31Z

@mimowo 

1. the dashboard is being run as a separate pod right now. the pros are: responsibility separation, ability to scale the backend pod independently. The frontend being quite lightweight, it can help to leave it live its life. The cons, are 2 deployments to manage. I don't foresee technical limitations in having the 2 containers in the same pod and deployment.  I was thinking about having an oauth-proxy in the future to have some authentication. The frontend will anyway use the ingress or route to get access from the backend. So, I am ok with both approaches.
2. ok, noted; I didn't see it; I will follow that path then to have the same approach as for prometheus.
3. let's keep it here then and have an opt-in flag.

### Comment by [@akram](https://github.com/akram) — 2024-12-18T12:47:14Z

> @mimowo
> 
> 1. the dashboard is being run as a separate pod right now. the pros are: responsibility separation, ability to scale the backend pod independently. The frontend being quite lightweight, it can help to leave it live its life. The cons, are 2 deployments to manage. I don't foresee technical limitations in having the 2 containers in the same pod and deployment.  I was thinking about having an oauth-proxy in the future to have some authentication. The frontend will anyway use the ingress or route to get access from the backend. So, I am ok with both approaches.
> 2. ok, noted; I didn't see it; I will follow that path then to have the same approach as for prometheus.
> 3. let's keep it here then and have an opt-in flag.

@mimowo : re-reading question 1, I think I have replied with an out of topic answer. I was focusing on the question on having 2 separate deployments for frontend and backend, and if I understand correctly, the question is about having entirely kueue-viz as (a) container(s) inside of the kueue pod. That's a possibility also, but for now, I prefer to have it separate. The cons are: given still the young age of the project, crashes or performance issues should not impact kueue main container. So, for isolation purposes, I think it is preferable to keep them separate for now.

When community adoption gets better, I think, we can work in rationalising the project by having an internal kueue api, that the backend can use efficiently rather than reimplement some features or grabbing some metrics.  At the end, the backend could be a simple websocket serving hatch that would cleanup or assemble data coming from the kueue observability api.

Regarding some other pros/cons: having them in the same pod may tighten coupling of the dashboard and core kueue. At some points, this is a pro, but in the early stages of the component, that could reduce velocity.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T12:58:57Z

@akram thank you for the deep responses!

I'm perfectly ok with separate pods for frontent and backend - separate from the main Kueue. All the argumentation sgtm.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-24T11:34:36Z

/kind dashboard
