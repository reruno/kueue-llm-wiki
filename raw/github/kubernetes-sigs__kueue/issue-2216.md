# Issue #2216: Limit the retry period length in waitForPodsReady

**Summary**: Limit the retry period length in waitForPodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2216

**Last updated**: 2024-05-24T08:22:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2024-05-17T12:05:48Z
- **Updated**: 2024-05-24T08:22:12Z
- **Closed**: 2024-05-24T08:22:12Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 14

## Description

**What would you like to be added**:

An additional field in waitForPodsReady.requeuingStrategy to limit the length of retry period to, say, 30 minutes-1hour. 

**Why is this needed**:

Currently the retry period length grows exponentially. If the workload could not start for 2 days, the next retry will be in 2 days (more or less).  That basically means that the user has to recreate the workload to make it admitted in a reasonable time. 
It might not be a problem with 1 workload, but it may be a challenge with 500 workloads that were failing over weekend due to a silly config error.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

cc: @mimowo @tenzen-y

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T13:49:19Z

Sounds good to me.
@mwielgus @mimowo How about the `.waitForPodsReady.requeuingStrategy.maxRequeuingPeriod`?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-17T14:19:00Z

Maybe by analogy to 'backoffBaseSeconds' we can have 'backoffMaxSeconds'?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T14:20:46Z

> Maybe by analogy to 'backoffBaseSeconds' we can have 'backoffMaxSeconds'?

But isn't this parameter nonrelated to backoff?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-17T14:47:01Z

> Maybe by analogy to 'backoffBaseSeconds' we can have 'backoffMaxSeconds'?

I synced about this offline with @mimowo. In conclusion, I agreed with the `backoffMaxSeconds` since once the workload exceeds, the `backoffMaxSeconds` keeps to be re-queueing with the `backoffMaxSeconds.`

### Comment by [@Kavinraja-G](https://github.com/Kavinraja-G) — 2024-05-19T14:16:45Z

@tenzen-y I would like to work on this, probably my first contribution in this project :) lmk, thanks!

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-20T08:13:47Z

@Kavinraja-G sgtm, 

One question remains open if this param should be defaulted (to say 1h), or left as an opt-in knob. Any opinions?

### Comment by [@Kavinraja-G](https://github.com/Kavinraja-G) — 2024-05-20T17:57:49Z

I think we can default the value to `1h` and set it as safer threshold.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-21T08:33:05Z

sgtm, feel free to submit the PR. @mwielgus @tenzen-y let us know if you have some additional perspective.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-21T18:30:12Z

1h still sounds short, given how long it might take to obtain a GPU these days. Maybe 24h?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-21T20:41:02Z

@Kavinraja-G Yeah, feel free to take this issue.

> 1h still sounds short, given how long it might take to obtain a GPU these days. Maybe 24h?

I agree that 1h is still shorter, but I'm not convinced which default value is better since the value deeply depends on the Job types in the cluster like long running Jobs vs short term Jobs.

I believe that we should consider the objective of the default value. For example, the default value is for a. mitigating errors by invalid configuring credentials and image names or b. reducing the nonvaluable re-poping due to insufficient computing.

If we assume situation a, it would be better to set the default shorter time within a single business time, if we assume situation b, selecting 24h would be better.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-21T21:00:42Z

> For example, the default value is for a. mitigating errors by invalid configuring credentials and image names

Ok, so here we are assuming that the user didn't notice the multiple run attempts, and then they notice, they fix the image name (for example). So now we don't want them to wait 24h to run again.

In that case, 1h sounds ok. Maybe it's also acceptable from an insufficient computing perspective.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-05-22T13:10:54Z

@Kavinraja-G have you started this already? Otherwise, I can take it

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T14:06:32Z

I think you can @Kavinraja-G has taken #2204 for now.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-05-22T14:13:22Z

/assign
