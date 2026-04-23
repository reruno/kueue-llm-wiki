# Issue #7119: v1beta2: Enable more stringent kube-api-linter checks

**Summary**: v1beta2: Enable more stringent kube-api-linter checks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7119

**Last updated**: 2025-11-06T07:49:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-10-01T13:22:07Z
- **Updated**: 2025-11-06T07:49:58Z
- **Closed**: 2025-11-05T20:32:31Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 25

## Description

As we added kal linter, we had to disable linters that could potentially break the API.

@mimowo @tenzen-y should we apply a few apis for v1beta2?

  - "maxlength" # Ensure all strings and arrays have maximum lengths/maximum items.
  - "nobools" # Bools do not evolve over time, should use enums instead.
  - "nomaps" # Ensure maps are not used.
  - "optionalfields" # Ensure that all fields marked as optional adhere to being pointers and
                                 # having the `omitempty` value in their `json` tag where appropriate.
  - "optionalorrequired" # Every field should be marked as `+optional` or `+required`.
  - "requiredfields" # Required fields should not be pointers, and should not have `omitempty`.
  - "ssatags" # Ensure array fields have the appropriate listType markers

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:27:40Z

@kannon92 could you maybe do some short summary  of examples where our current API is not  conformant to those?

It is hard to assess the  impact of enabling those without experiment.

Also, are these settings "hard" requirement on k8s core APIs,  or "soft" recommendations?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T14:21:13Z

At a quick glance, at least `"statussubresource"` could not be enabled. The Topology and WorkloadPriorityClass does not provide status.

So, I think that we should extract the rules.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T14:49:14Z

Maybe we could consider empty status for the resources, we are probably going to need them in the future, wdyt @tenzen-y ?

OTOH I'm good to keep it lean and minimal for now, and just diable the checks. 

Also, maybe there are some inlined comments that could make the linter enabled, but just skipped on specific API objects, is there such an option @kannon92 ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T14:56:02Z

> Maybe we could consider empty status for the resources, we are probably going to need them in the future, wdyt @tenzen-y ?
> 
> OTOH I'm good to keep it lean and minimal for now, and just diable the checks. 
> 
> Also, maybe there are some inlined comments that could make the linter enabled, but just skipped on specific API objects, is there such an option @kannon92 ?

For Topology, we can add an empty status, but for WorkloadPriorityClass, I don’t think so which aligned with priorityClass and does not have even spec field.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-01T15:04:31Z

# Max Length
Ensure all strings and arrays have maximum lengths/maximum items.

This means that all strings and arrays need to have a max length. This could be breaking but I think it is a good change.

# Nobools

This is a more opioned but kubernetes api but no bools are allowed in APIs fields. So anything with bool would fail the linter and we would require conversion to an enum. I'll leave this open to you all for enabling it. Bools don't age well in my experience so I think this is a good rule but its always controverisal.

# nodurations

@everettraven I'm not entirely sure the motivation on this one. But this would forbid any use of time.Duration.

# nofloats

Make sure floats are not used

# integers

Make sure only int32 or int64 are used instead of int.
# no maps

The only allowed type for a map is map[string]string and every other map is forbidden. 

## changing tags on types

These are the ones that may become hard to enforce on an existing API. I tried to enable these on JobSet but some of our defaulting logic interferes with these.

### optionalfields
This one may became breaking as optional fields must be marked as a pointer. 

### optionalorrequired
Every field must be +optional or +required

### requiredfields
Required files should not be pointers and should not have `omitempty`

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-01T15:48:51Z

Some of these were simply to enable.

https://github.com/kubernetes-sigs/kueue/pull/7124

- [x] integers
- [x] statusoptional
- [x] statussubresource
- [x] floats
- [x] nodurations

### Comment by [@everettraven](https://github.com/everettraven) — 2025-10-01T15:57:59Z

`nodurations` is in place because Kubernetes APIs try to avoid the usage of `time.Duration` because it forces all clients to use Go-compatible duration parsing. See: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#units

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T16:02:48Z

> `nodurations` is in place because Kubernetes APIs try to avoid the usage of `time.Duration` because it forces all clients to use Go-compatible duration parsing. See: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#units

That makes sense. Thank you for expanding that here.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T16:06:44Z

In that case iiiuc the configMap API seems safe to use Duration, because iiiuc it is not meant for editing with API clients, but admins manually or with specialized tools.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-03T13:51:51Z

As I mentioned in https://github.com/kubernetes-sigs/kueue/pull/7124#discussion_r2401939239, I would propose introducing KAL to Config API as well so that we can apply the "almost" same rule to an entire API.

But, we should ignore "duration" rule only for Config API as mentioned in @mimowo .

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-14T15:26:55Z

Updated this to reflect the current state. I am going to work on seeing how much effort it would take to apply the following rules:

- [x] "maxlength" # Ensure all strings and arrays have maximum lengths/maximum items.
- [ ] "nobools" # Bools do not evolve over time, should use enums instead.
- [ ] "nomaps" # Ensure maps are not used.
- [ ] "optionalfields" # Ensure that all fields marked as optional adhere to being pointers and
- [ ] "optionalorrequired" # Every field should be marked as +optional or +required.
- [ ] "requiredfields" # Required fields should not be pointers, and should not have omitempty.
- [x] "ssatags" # Ensure array fields have the appropriate listType markers

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-15T20:17:28Z

Opened up https://github.com/kubernetes-sigs/kueue/pull/7283 for MaxLength.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-21T20:02:22Z

Opened up https://github.com/kubernetes-sigs/kueue/pull/7339 for ssatags.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T08:35:36Z

/retitle v1beta2: Enable more stringent kube-api-linter checks

To emphasize it is part of the v1beta2 effort.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T13:15:32Z

@kannon92 please follow up with PRs wrt the remaining points in https://github.com/kubernetes-sigs/kueue/issues/7119#issuecomment-3402422789, or let us know which are problematic.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-31T13:24:17Z

The others one are a lot more involved and potentially break a lot of things.

For example, nomaps, points out that our use of resourceLists (in CQ or workloads) as being in violation. I think changing that is quite involved.

I'm happy to do it but it would require changing our useage of resourceLists from k8s.

Required/Optional is going to be a lot of changing fields from pointers to structs if the defaulting logic allows it. I tried to address them but we had over 500 violations of these rules and I got overwhelmed trying to fix all of them.

If you or @tenzen-y want to take a look at some of those we can see if they are worth applying or just keeping these off.

They are a bit more opinionated.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-31T13:25:44Z

And same for nobools, I like the rule but this is not yet a established k8s rule. I think the goal is to phase out the usage of bools as API fields in kubernetes but that rule has not yet been enabled.

@JoelSpeed @everettraven do we know if we had a discussion with sig-architecture about enabling nobool?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T13:34:06Z

I think I'm ok to skip some changes which would require heavy refactor of the API. 

However, it may still be good to enable the checks, and all the violations just mark //nolint. This way we would get notification going forward at least. wdyt?

Also, I'm not clear from your description how involving it would be to enable "nobools", how many violations? Maybe it would help to open a PR per each rule, then it we would be able to see the list of violations and decide?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-31T15:33:20Z

Okay, I opened up https://github.com/kubernetes-sigs/kueue/pull/7488 to atleast show all the failures without any changes.

### Comment by [@everettraven](https://github.com/everettraven) — 2025-11-03T13:42:08Z

@kannon92 I don't believe we had a discussion with SIG folks about enabling the `nobools` in k/k but being cautious with the use of boolean values for a field is a thing that is explicitly mentioned in the Kubernetes API Conventions (https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#primitive-types): 

> Think twice about bool fields. Many ideas start as boolean but eventually trend towards a small set of mutually exclusive options. Plan for future expansions by describing the policy options explicitly as a string type alias (e.g. TerminationMessagePolicy).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T17:08:35Z

Latest, update.
- [x] "maxlength" # Ensure all strings and arrays have maximum lengths/maximum items.
- [x] "nobools" # Bools do not evolve over time, should use enums instead.
- [x] "nomaps" # Ensure maps are not used.
- [ ] "optionalfields" # Ensure that all fields marked as optional adhere to being pointers and
- [ ] "optionalorrequired" # Every field should be marked as +optional or +required.
- [ ] "requiredfields" # Required fields should not be pointers, and should not have omitempty.
- [x] "ssatags" # Ensure array fields have the appropriate listType markers

 It would be great to also enable `optionalfields, optionalorrequired, requiredfields`. I see pending PR https://github.com/kubernetes-sigs/kueue/pull/7488 which requires rebase and tests fixing.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T20:32:26Z

Latest, update after https://github.com/kubernetes-sigs/kueue/pull/7488.
- [x] "maxlength" # Ensure all strings and arrays have maximum lengths/maximum items.
- [x] "nobools" # Bools do not evolve over time, should use enums instead.
- [x] "nomaps" # Ensure maps are not used.
- [x] "optionalfields" # Ensure that all fields marked as optional adhere to being pointers and
- [x] "optionalorrequired" # Every field should be marked as +optional or +required.
- [x] "requiredfields" # Required fields should not be pointers, and should not have omitempty.
- [x] "ssatags" # Ensure array fields have the appropriate listType markers

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-05T20:32:32Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7119#issuecomment-3493260639):

>Latest, update after https://github.com/kubernetes-sigs/kueue/pull/7488.
>- [x] "maxlength" # Ensure all strings and arrays have maximum lengths/maximum items.
>- [x] "nobools" # Bools do not evolve over time, should use enums instead.
>- [x] "nomaps" # Ensure maps are not used.
>- [x] "optionalfields" # Ensure that all fields marked as optional adhere to being pointers and
>- [x] "optionalorrequired" # Every field should be marked as +optional or +required.
>- [x] "requiredfields" # Required fields should not be pointers, and should not have omitempty.
>- [x] "ssatags" # Ensure array fields have the appropriate listType markers
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-05T20:34:41Z

I have one follow up that @JoelSpeed brought up.

We should avoid using //nolint as it disables the entire linter on those fields.

I would like to follow the pattern that Kubernetes has where we add exclusion list based on regularexpressions.

See [example](https://github.com/kubernetes/kubernetes/blob/master/hack/kube-api-linter/exceptions.yaml).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-06T07:49:58Z

awesome, to keep track of the remaining work I opened: https://github.com/kubernetes-sigs/kueue/issues/7547
