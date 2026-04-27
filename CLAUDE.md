# LLM Wiki


A personal knowledge base maintained by Claude Code.
Based on Andrej Karpathy's LLM Wiki pattern.


## Purpose


Kueue is a Kubernetes-native job queueing system that manages quotas and how jobs consume them. It decides when a job should wait, when it should be admitted to start (i.e. Pods can be created), and when it should be preempted (i.e. active Pods should be deleted).

Kueue does not replace existing controllers or the kube-scheduler. It gates when workloads become visible to them by toggling `.spec.suspend`, leaving actual Pod scheduling to Kubernetes — making it a lightweight add-on rather than a parallel system.

Core problems it solves:

- Batch workload scheduling on Kubernetes, treating jobs (not Pods) as the unit of quota and priority
- Multi-tenant resource sharing via hierarchical ClusterQueues, LocalQueues, and Cohorts with borrowing/lending
- Heterogeneous workload support: batch/v1 Jobs, JobSet, Kubeflow training jobs, RayJob/RayCluster, Argo Workflows, AppWrapper, plain Pods
- Gang scheduling and preemption for all-or-nothing workloads
- Topology-aware scheduling for bandwidth-sensitive jobs (e.g. ML training across nodes/racks/zones)

Primary users: platform teams running shared Kubernetes clusters for ML/AI training, HPC, data processing, or CI — particularly where fair-share quota enforcement across teams on expensive accelerators (GPUs, TPUs) matters.

Home: `kubernetes-sigs/kueue`, a Kubernetes SIG-Scheduling subproject.


## Folder structure


```
raw/          -- source documents (immutable -- never modify these)
wiki/         -- markdown pages maintained by Claude
wiki/index.md -- table of contents for the entire wiki
wiki/log.md   -- append-only record of all operations
```


## Ingest workflow


When the user adds a new source to `raw/` and asks you to ingest it:


1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add wiki-links ([[page-name]]) to connect related pages
6. Update `wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `wiki/log.md` with the date, source name, what changed, and the git commit hash of the `[data-collection]` commit this analysis was based on (run `git log --oneline --grep='\[data-collection\]' -1` to find it)


A single source may touch 10-15 wiki pages. That is normal.


## Page format


Every wiki page should follow this structure:


```markdown
# Page Title


**Summary**: One to two sentences describing this page.


**Sources**: List of raw source files this page draws from.


**Last updated**: Date of most recent update.


---


Main content goes here. Use clear headings and short paragraphs.


Link to related concepts using [[wiki-links]] throughout the text.


## Related pages


- [[related-concept-1]]
- [[related-concept-2]]
```


## Citation rules


- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification


## Question answering


When the user asks a question:


1. Read `wiki/index.md` first to find relevant pages
2. Read those pages and synthesize an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page


Good answers should be filed back into the wiki so they compound over time.


## Lint


When the user asks you to lint or audit the wiki:


- Check for contradictions between pages
- Find orphan pages (no inbound links from other pages)
- Identify concepts mentioned in pages that lack their own page
- Flag claims that may be outdated based on newer sources
- Check that all pages follow the page format above
- Report findings as a numbered list with suggested fixes


## Rules


- Never modify anything in the `raw/` folder
- Always update `wiki/index.md` and `wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `machine-learning.md`)
- Write in clear, plain language
- When uncertain about how to categorize something, ask the user
