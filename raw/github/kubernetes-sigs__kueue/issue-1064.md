# Issue #1064: [website] Deduplicate code samples

**Summary**: [website] Deduplicate code samples

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1064

**Last updated**: 2023-09-19T13:47:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-08-16T19:49:56Z
- **Updated**: 2023-09-19T13:47:09Z
- **Closed**: 2023-09-19T13:47:09Z
- **Labels**: `good first issue`, `kind/cleanup`
- **Assignees**: [@EchoGroot](https://github.com/EchoGroot)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We have a shortcode in the website to include file contents in tutorials.
However, we still have code directly added to the markdown in some files (for example):

https://github.com/kubernetes-sigs/kueue/blob/c7e7df8ec36fcc1e8a2f837af5db075c26567a14/site/content/en/docs/tasks/run_jobs.md?plain=1#L61

Since we will be adding a lot of new files, it might be useful to divide the files in /site/examples in folders, like so:
- admin (for ClusterQueues, LocalQueues, etc).
- jobs
- python (for python code)

**Why is this needed**:

- Avoid copies of the same contents that can become out-of-sync.
- Allow users to download the contents as a file.

## Discussion

### Comment by [@EchoGroot](https://github.com/EchoGroot) — 2023-08-23T01:43:37Z

Hi @alculquicondor , In addition to classifying the files under the /site/examples folder, do I also need to delete the shortcode in markdown? Because these shortcode may forget to update

### Comment by [@EchoGroot](https://github.com/EchoGroot) — 2023-08-23T01:44:15Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-23T01:48:37Z

> do I also need to delete the shortcode in markdown?

@EchoGroot Yes. You can refer to the following sample:

> For the next example, let's start with a cluster with Kueue installed, and first create our queues:
> 
> {{% include "python/sample-job.py" "python" %}}

https://github.com/kubernetes-sigs/kueue/blob/c7e7df8ec36fcc1e8a2f837af5db075c26567a14/site/content/en/docs/tasks/run_python_jobs.md#sample-job

### Comment by [@EchoGroot](https://github.com/EchoGroot) — 2023-08-23T01:52:12Z

> > do I also need to delete the shortcode in markdown?
> 
> @EchoGroot Yes. You can refer to the following sample:
> 
> > For the next example, let's start with a cluster with Kueue installed, and first create our queues:
> > {{% include "python/sample-job.py" "python" %}}
> 
> https://github.com/kubernetes-sigs/kueue/blob/c7e7df8ec36fcc1e8a2f837af5db075c26567a14/site/content/en/docs/tasks/run_python_jobs.md#sample-job

thanks, i see

### Comment by [@EchoGroot](https://github.com/EchoGroot) — 2023-08-23T15:03:50Z

May I ask how to test whether the display of the webpage is normal? I modified the shortcode in the webpage.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-23T15:06:37Z

> May I ask how to test whether the display of the webpage is normal? I modified the shortcode in the webpage.

@EchoGroot You can verify the page by the creating draft PR like this: https://github.com/kubernetes-sigs/kueue/pull/1063#issuecomment-1681174740

### Comment by [@EchoGroot](https://github.com/EchoGroot) — 2023-08-23T15:17:10Z

> > May I ask how to test whether the display of the webpage is normal? I modified the shortcode in the webpage.
> 
> @EchoGroot You can verify the page by the creating draft PR like this: [#1063 (comment)](https://github.com/kubernetes-sigs/kueue/pull/1063#issuecomment-1681174740)

thanks

### Comment by [@FZhg](https://github.com/FZhg) — 2023-09-14T18:33:38Z

> May I ask how to test whether the display of the webpage is normal? I modified the shortcode in the webpage.

If you want to preview the change locally, you need first use the correct node version and hugo version specified in `netlifly.toml` file

 you can run the following cmd in the `site` directory
```bash
npm install
hugo server
```
