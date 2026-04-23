# Issue #7220: Support larger workloads in TAS

**Summary**: Support larger workloads in TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7220

**Last updated**: 2025-11-17T11:13:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-09T17:27:45Z
- **Updated**: 2025-11-17T11:13:42Z
- **Closed**: 2025-11-17T11:13:42Z
- **Labels**: `kind/feature`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 19

## Description

**What would you like to be added**:

I would like to revisit the API used to represent the TopologyAssignment to allow more nodes.

Currently, the entire assignment is stored in the Workload object, and looks like this (in pretty print), see [API](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/kueue/v1beta1/workload_types.go#L264-L280): 

```yaml
"topologyAssignment": {
    "domains": [
        {
            "count": 1,
            "values": [
                "node-name-example-value" # Example value
            ]
        },
        ...
    ]
}
```
This is very verbose, but the cap from ETCD on the Workload object size is 1.5Mi (1572864 bytes). IIUC ETCD stores CRDs JSONs.

The overhead per node is  `{"count": 1,"values": [""]},` is 28 bytes

Under assumptions:
- we can devote 1500000 bytes for the assignment, leaving 72k for the spec
- nodeName length is 30 characters (possible for users optimizing the clusterName, and node pool name, for example on GKE is possible: `gke-` + `clusterName + `-` + `nodepoolName` + `-991aff16-xyza` (so 19 chars of fixed overhead + 11 spare for clusterName and nodepoolName).

Then we currently can have assignment using 1500000/(28+30)=25k nodes.

Some ideas worth considering:
- when Topology is specified at the NodeName level (kubernetes.io/hostname), then using the following API we can get much smaller sizes:

"topologyAssignment": {
    "nodeNames": ["node-name-example-value1","node-name-example-value2"],
    "counts": ["3","2"]
}

In this representation the overhead per node is just `"",` - 3 characters. So, we can squeeze up to 1500000/(3+30)=45k nodes. In case when all counts equal "1" (typical) we could assume it is just a table of 1s.

Surely, in order to support even larger workloads we will need to split the assignment into "slices", similarly as Endpoint is split into EndpointSlices. However, this requires significant refactoring, whilst the structure can be optimized a lot.

One consideration is also that if the lowest topology domain is not `kubernetes.io/hostname`, then we need to support "deep" structure for domains. So, we may consider "incremental" API change for introducing the new fields: "nodeNames", and "counts" for the  `kubernetes.io/hostname` case, but keep the previous structure for the generic case.

**Why is this needed**:

To support workloads spanning 40k+ nodes.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T17:28:01Z

cc @mwysokin @mwielgus @olekzabl @tenzen-y

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-09T21:15:19Z

This looks great!

Three naive questions, if I may:

1. Whichever format of `topologyAssignment` we pick, we could then theoretically improve by storing a GZIPped string. \
  I'm guessing that's not preferred - but I'm curious to learn why? \
  Would the concern here be readability for the end user? Performance of decoding? Sth else?

2. More seriously - assuming node name structure described above, `perNodePoolPrefix`-`properNodeName`, how about this:
   ```
   "topologyAssignment": [
     {
       "nodeNamePrefix": "cluster1-pool1-",
       "nodeNames": ["some-name","another-name"],
       "counts": ["3","2"],
     },
     {
       "nodeNamePrefix": "cluster1-pool2-",
       ...
     }
   ]
   ```

   In GKE, the maximum number of node pools existing simultaneously in a single cluster (in last 30 days) is ~2300. \
   Taking the earlier assumptions (1500000 B available; 13 chars for proper node name; 17 chars for prefix), we get that:

   * the overhead per node pool is `{"nodeNamePrefix":"abcdefghijklmnopq","nodeNames":[],"counts":[]},` -> 67 bytes
   * the _full_ overhead per node, assuming 1-digit counts, is `"abcdefghijklm","1",` -> 20 bytes
   * thus we can fit around (1500000 - 67 * 2300) / 20 ~= **67.3k** nodes

   While for the original proposal (also assuming 1-digit counts) we'd get 1500000 / (3 + 30 + 4) ~= 40.5k nodes.

   And even if we just want 40k for now - then this "per-prefix" approach **does not require** users to "optimize" their cluster & node pools names.

   I understand the prefix length may be vendor-dependent; I'm hoping it should be acceptably easy to discover it automatically in Kueue code.

   Could that be worth doing, or is this a wrong direction?

3. Can the counts be stored as numbers, unquoted? \
    (That'd be a minor gain, but still, +2.3k nodes in the original proposal, and +7.5k in the "per-prefix" variant)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T05:57:04Z

> Whichever format of topologyAssignment we pick, we could then theoretically improve by storing a GZIPped string.
> I'm guessing that's not preferred - but I'm curious to learn why?
> Would the concern here be readability for the end user? Performance of decoding? Sth else?

I like this out of the box idea. I would say the main aspects that we want structured API:
1. readability of human user
2. easy parsing for integration code by users
3. performance of serialization and deserialization
4. unpredictible boundaries on the limit, hard to tell what is worst case scenario

Also, you may consider reading the EndpointSlice KEP, where we decided in the core k8s to split Endpoint into the EndpointSlice CRs, but I think the motivation there was slightly different: https://github.com/kubernetes/enhancements/tree/master/keps/sig-network/0752-endpointslices

However, none of that is "deal breaker" IMO. Especially I don't worry about (3.) because the structure is seldom adjusted. Especially, at the scale of >10k nodes you would have other bottlenecks for sure.

Also, (1.) we could mitigate by using this structure only for workload spanning more than 10k nodes, and old more readable API for small workloads.

I guess (2.) might be the pain. Imagine we introduce a format using "nodeName:<pod_count>,nodeName2:<pod_count2>, ...", and GZIP on top of that. Plus, only use the format for workloads >10k nodes. This creates friction if users would want to write automation parsing that. 

Still, this idea is worth interesting, because the alternative - use TopologyAssignmentSlice CRD is not tempting either. Also, the alternative would not be easy to consume by external tooling.

Personally, I find (4.) tricky, can we reliably say we support "60k" then? It is really hard to say what we support then. I know in practice we may reach 100k probably even. Worth exploring if GZIP or other compression formats could provide some boundaries on the "worst case scanerio for compression".

> I understand the prefix length may be vendor-dependent; I'm hoping it should be acceptably easy to discover it automatically in Kueue code.

This idea is worth exploring too. However, the code in Kueue is vendor neutral, and we cannot really create a switch statement for the format of every vendor. On top of that you have on-prem clusters where the node names might be of any form and shape.

What we could do maybe is to have a generic mechanism like "longestCommonNodeNamePrefix". You may check how 

> Can the counts be stored as numbers, unquoted?

I don't think they can, we don't control the serialization scheme between kube-apiserver and ETCd.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-10T08:27:54Z

> > I understand the prefix length may be vendor-dependent; I'm hoping it should be acceptably easy to discover it automatically in Kueue code.
> 
> This idea is worth exploring too. However, the code in Kueue is vendor neutral, and we cannot really create a switch statement for the format of every vendor. 

A `switch` was not my intent. I rather imagined a "smart & automated" detection - _for example_:

1. For every N between 1 and max(len(nodeName)), count distinct prefixes of length N of all the given node names.
2. Then:

    * Pick largest N for which the set had size <5000.
    
    Or (more accurate but a bit more complex):

    * For every N calculate _just the bytesize_ of the node-names representation when taken "per-N-prefix", \
      and pick N to minimize that.
    
    Or sth else.

> On top of that you have on-prem clusters where the node names might be of any form and shape.
> 
> What we could do maybe is to have a generic mechanism like "longestCommonNodeNamePrefix". You may check how

Yes, more like this. (Did you imagine sth like I described above, or sth different?)

> > Can the counts be stored as numbers, unquoted?
> 
> I don't think they can, we don't control the serialization scheme between kube-apiserver and ETCd.

Hmm, aren't they unquoted in the current representation? \
`Count` is [officially](https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/apis/kueue/v1beta1/workload_types.go#L298) an int32. \
And in your initial example (of the current format), there is `"count": 1`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T08:36:41Z

> Yes, more like this. (Did you imagine sth like I described above, or sth different?)

I imagined the simple "longestCommonNodeNamePrefix" across all nodeNames, inspired by your proposal. I can see you are extending the idea to find the optimal prefix. It makes sense to me.

> Hmm, aren't they unquoted in the current representation?

Oh, I think they are indeed unquoted, and this is my mistake in the original issue description, when I wrote `"counts": ["3","2"]`. However, this is what I **think**, and I might be wrong (haven't checked). To be absolutely sure it would be good to try to see the actual traffic by increasing the log level to 10 for API server and etcd. IIRC this should log the entire requests.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-10T08:45:02Z

For now, I checked that `kubectl get workload xxxxx -o json` returns `"count": 1` there. \
But if you say that's not enough to check, I'll trust you.

In fact, I guess we'd anyway define the new `Counts` field to be `[]int32`, and then an actual verification whether these internally end up quoted or unquoted won't be very urgent.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-10T08:54:43Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T08:56:08Z

Yes, checking the counts is not urgent, it is not a deal breaker for any of the approaches anyway.

Let me quickly summarize the options we considered so far:
1. as in the issue description, simple pair of fields: `NodeNames` + `Counts`, another variant would be `NodeUIDs` + `Counts`
2. gzip for the list of nodes
3. auto-detection of the "most efficient" common prefix for the nodes
4. full blown TopologyAssignentSlices

I think for 0.15 (4.) is really out of question as too involving. Also, I would question using TopologyAssignmentSlices is simpler to the API clients than decode with gzip. Ensuring that clients see consistent state of the world in (4.) is very hard too.

In (2.) it seems the node names would compress really really well. Maybe you could perform and experiment where we would test the size of the string assuming say 100k nodes, with the naming scheme as in the description.

As for (3.) I think it is realistically, more likely, for the largest clusters that the most efficient prefix is just the "clusterName", because multiple nodePools can be in use. So, it wouldn't give much compared to (1.) for users who are determined to push boundaries and name their clusters just one letter :).

EDIT: at the moment I'm mostly hesitant between (1.) and (2.)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T09:00:56Z

Importantly, for the context, in the k8s workload using string format for representation of arrays isn't unheard of, For example k8s Job is using string compact representation for indexes: https://github.com/kubernetes/kubernetes/blob/ee1ff4866e30ac3685da3e007979b0e9ab7651a6/pkg/apis/batch/types.go#L275-L289

The motivation is very similar: compact format to avoid using "slices" and to push boundaries on the size of supported number of indexes.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-10T09:01:51Z

> As for (3.) I think it is realistically, more likely, for the largest clusters that the most efficient prefix is just the "clusterName", because multiple nodePools can be in use. So, it wouldn't give much compared to (1.) for users who are determined to push boundaries and name their clusters just one letter :).

Please note that my proposal [here](https://github.com/kubernetes-sigs/kueue/issues/7220#issuecomment-3387511988) goes beyond "one common prefix", to "multiple common prefixes". \
That way, it can noticeably help even when a user has multiple node pools (e.g. I considered 2300 node pools in my example calculations), _and_ 1-character cluster names. \
(And then, it'd help even more if they have less node pools, or longer cluster names).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T09:15:59Z

> Please note that my proposal https://github.com/kubernetes-sigs/kueue/issues/7220#issuecomment-3387511988 goes beyond "one common prefix", to "multiple common prefixes".

Ah I see, clever. 

While we cannot check all vendors, and on-prem naming strategies, if we choose this approach we should check other strategies outside of gke, so that we don't over-optimize for a specific vendor.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-10-13T07:55:42Z

I tried to check this quickly for AWS & Azure.

* For Azure, [this post](https://discuss.kubernetes.io/t/naming-individual-nodes-of-node-pool/23107/4) suggests that they have common per-node-pool prefixes, even longer than GKE (e.g. `aks-npl1-66531061-vmss00...`).
* For AWS, I found [this](https://repost.aws/questions/QUj2NZJzF-T6eCWlbSVslqvw/why-are-my-eks-cluster-nodes-having-different-name-scheme) & [this](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/understanding-ec2-instance-hostnames-domains.html) - which suggests a short common prefix (`ip-`) and longer common suffixes (e.g. `.us-west-2.compute.internal`).

Moreover, in both these cases (unlike in GKE), the optimal prefix/suffix lengths may vary across node pools.

So the approach still seems to generally make sense - but I'd need to think how to adjust in detail.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T07:59:42Z

Yes, if we go this way we should rather be optimizing both prefixes and suffixes, but there is also a trade off between complexity of the solution and the size of supported workloads. Once we explore all the options more, another summary would be helpful.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2025-10-13T11:55:21Z

In V1 the structure should support arbitrary large workloads. As we agreed to pass official Kuberntes review for V1, the API should rather avoid temporary hacks or be incompatible with standard Kuberentes tools. GZIP or anything like that should rather be used as a last resort. I wouldn't completely rule out TopologyAssignentSlices. TBH, they are the cleanest, but I understand that this option may require more work.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T15:04:41Z

It might be good to advise a k8s API reviewer on that one. 

Ok let's not rule out TopologyAssignmentSlices, but they still have drawbacks to discuss:
- any updates to them are no longer atomic and so: a) we need to make sure the structures are properly managed on workload admission and eviction, b) they will add significant complexity for multi node hot swap
- for external APIclients fetching all slices belonging to a particular workload and consolidating lists may actually be harder than doing couple of lines to decompress
- they will require more QPS on admission and eviction

Finally, since they increase complexity if we are to finish for 0.15 we need to prioritize that strongly. Doing them will bring some risk of breaking functionality, so we should leave some testing time before release to be comfortable

EDIT: If TAS needs to support arbitrarily large workloads say 100k nodes then slices seem the only viable option. Still maybe that could come in V1 as an incremental addition as extraTopologySlices and for now we could push boundaries to 40k nodes or so within the single Workload

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-13T15:45:35Z

For context, this KEP may help a little bit with the current API https://github.com/kubernetes/enhancements/tree/master/keps/sig-api-machinery/4222-cbor-serializer, by reducing the overhead size, I'm not totally sure what is the impact though "in practice", one would need to perform an experiment.

### Comment by [@OguzPastirmaci](https://github.com/OguzPastirmaci) — 2025-10-16T22:11:47Z

To add a data point from Oracle Cloud for prefixes, here's how it works with managed node pools: https://docs.oracle.com/en-us/iaas/Content/ContEng/Reference/contenggeneratednodenames.htm

We also have self-managed node pools, though. And for those it's up to the customer to decide how they want to name the nodes.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-17T10:20:51Z

For clarity, let me
/reopen
this until #7697 is merged.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T10:20:57Z

@olekzabl: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7220#issuecomment-3540983291):

>For clarity, let me
>/reopen
>this until #7697 is merged.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
