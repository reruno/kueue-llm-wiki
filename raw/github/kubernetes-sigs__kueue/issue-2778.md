# Issue #2778: Decide if we release kjobctl as part of Kueue

**Summary**: Decide if we release kjobctl as part of Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2778

**Last updated**: 2024-12-03T18:59:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-06T07:34:20Z
- **Updated**: 2024-12-03T18:59:01Z
- **Closed**: 2024-12-03T18:59:01Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 19

## Description

We started to develop kjobctl inside Kueue ([cmd/experimental/kjobctl](https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental/kjobctl)) to get quickly off the ground. 

This lets us develop quickly, and may be handy for a while yet.

However, in the long run we discussed that the plan is to move it at some point to a dedicated kubernetes-sigs subproject. 

Until that happens - should we release it as part of Kueue release process (exposing the artifacts)?

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-06T07:35:19Z

/cc @alculquicondor @mwielgus @tenzen-y 
I open this as a follow up to https://github.com/kubernetes-sigs/kueue/pull/2642.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-14T16:19:22Z

TBH, I'm ok with either approach. But, I'm wondering if we can create separate repository since I'm not familiar with criterion for new repositories in the k-sigs org.

I just want to say that we should commonize all duplicated scripts as root scripts when we decide to we manage kjobctl in this repository.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-10T13:38:52Z

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-10T16:15:54Z

We can split after we have the MVP, to avoid disrupting the developer flow.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:18:22Z

FYI I asked around and it seems if we want to move it to separate repo the next step would be to create an issue analogus to [this one for Jobset](https://github.com/kubernetes/org/issues/4137). 

Let me yet confirm the decision with @mwysokin and @mwielgus

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-11-06T09:18:07Z

SGTM 🖖

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:34:28Z

> FYI I asked around and it seems if we want to move it to separate repo the next step would be to create an issue analogus to [this one for Jobset](https://github.com/kubernetes/org/issues/4137).
> 
> Let me yet confirm the decision with @mwysokin and @mwielgus

Which SIGs sponsor kjobctl? I guess sig-apps? In that case, I guess that we need to negotiate with the SIG lead in advance.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T09:40:50Z

> Which SIGs sponsor kjobctl? I guess sig-apps?

This seems the most natural fit.

> I guess that we need to negotiate with the SIG lead in advance.

I see, so we should bring this topic to agenda for sig-apps meeting?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T09:42:20Z

Or alternatively, do you think we could move the project under umbrella of being sponsored by wg-batch?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:43:40Z

> > Which SIGs sponsor kjobctl? I guess sig-apps?
> 
> This seems the most natural fit.
> 
> > I guess that we need to negotiate with the SIG lead in advance.
> 
> I see, so we should bring this topic to agenda for sig-apps meeting?

I think so too. I know that SIG sometimes recommends outside of Kube org.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:44:10Z

> Or alternatively, do you think we could move the project under umbrella of being sponsored by wg-batch?

It is not available. All subprojects must be sponsored by SIG, not WG.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:46:42Z

> > Or alternatively, do you think we could move the project under umbrella of being sponsored by wg-batch?
> 
> It is not available. All subprojects must be sponsored by SIG, not WG.

https://github.com/kubernetes/community/blob/master/governance.md

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T09:46:57Z

The next sig-apps meeting will probably be after KubeCon, so Nov 25, we can raise it then.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T09:49:56Z

FYI we are already presenting the kjobctl as an idea at the [wg-batch meeting Jun 6th, 2024](https://docs.google.com/document/d/1XOeUN-K0aKmJJNq7H07r74n-mGgSFyiEDQ3ecwsGhec).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T09:54:11Z

> FYI we are already presenting the kjobctl as an idea at the [wg-batch meeting Jun 6th, 2024](https://docs.google.com/document/d/1XOeUN-K0aKmJJNq7H07r74n-mGgSFyiEDQ3ecwsGhec).

Yeah, I attended that. IIRC, Maciej represented some concerns about the kjobctl templating mechanism.
Anyway, we need to negotiate in the next sig-apps.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T10:10:43Z

cc @soltysh as sig-apps lead to also align on the next steps here.

### Comment by [@soltysh](https://github.com/soltysh) — 2024-11-06T12:26:56Z

Based on my understanding kjobctl is tightly coupled with kueue, and reading through comments that also holds on the code level. What exactly a separate repository provides you that can't be achieve when releasing kjobctl together with kueue? I can't speak of the maturity of the command itself, so I'll leave that to be answered by the maintainers. Did you finished the MVP mentioned earlier? 

I don't have any strong objections, but I'd like to better understand where you are and what the plan for the future are before making the decision to add another repository.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T12:50:29Z

> Based on my understanding kjobctl is tightly coupled with kueue, and reading through comments that also holds on the code level. 

I think this is not correct, kjobctl is a CLI which is aware of Kueue, but can be used to create Jobs without Kueue.

Currently it lives in ["cmd/experimental" folder](https://github.com/kubernetes-sigs/kueue/tree/main/cmd/experimental/kjobctl ). Yes, it has a dependency to Kueue, but only to make it aware of Kueue and to use Kueue for testing. AFAIK we only use the dependency at the API level for constants. 

Actually, but keeping it longer in Kueue we risk for kjobctl to become tightly coupled, but for now it is part of Kueue repo just to kickoff the project faster.

> Did you finished the MVP mentioned earlier?

I think so, here we have a [documented list of supported commands](https://github.com/kubernetes-sigs/kueue/blob/main/cmd/experimental/kjobctl/docs/commands/kjobctl.md). And we also support the [slurm mode](https://github.com/kubernetes-sigs/kueue/blob/main/cmd/experimental/kjobctl/docs/run_slurm.md).

Let me check if @mwysokin or @mwielgus something is still missing to call the MVP complete.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-03T13:13:09Z

FYI: we have the new and shiny repo: https://github.com/kubernetes-sigs/kjob. The code is perfectly clean :)
