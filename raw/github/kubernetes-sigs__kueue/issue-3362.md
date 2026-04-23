# Issue #3362: [kjobctl] Provide the name of the executed script in the "describe slurm"

**Summary**: [kjobctl] Provide the name of the executed script in the "describe slurm"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3362

**Last updated**: 2024-11-18T18:00:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@BluValor](https://github.com/BluValor)
- **Created**: 2024-10-29T15:38:52Z
- **Updated**: 2024-11-18T18:00:55Z
- **Closed**: 2024-11-18T18:00:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Add name of the source file of the script executed when creating a slurm job to the "describe slurm" output.

**Why is this needed**:
"describe slurm" currently prints out the content of the executed script, but not the name of the source file of the script.

**Completion requirements**:
The output of the "describe slurm" command should contain either:
- the name of the source file of the script
- the whole path to the source file of the script (aka the default argument of the "create slurm" command)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T15:47:10Z

Cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T15:47:22Z

Cc @mwysokin

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-11-04T11:28:31Z

@BluValor Could you give a bit more details about why you think it's needed or why this would provide an improved UX?

### Comment by [@BluValor](https://github.com/BluValor) — 2024-11-05T10:21:47Z

The motivation is:
- it makes it easier for the user to identify the work the job does without reading the script itself
- use cases in scripts using the kjob - pulling the name - also for identification purposes

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-12T12:32:11Z

Currently, we can't display this information because the Slurm builder only generates the script. Since we're using batch/Job for Slurm, I think we can use a label or annotation to provide the script name, like `kjobctl.x-k8s.io/slurm-script-name`.

@mwysokin WDYT?

### Comment by [@Horiodino](https://github.com/Horiodino) — 2024-11-12T12:42:17Z

/assign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-11-12T13:22:58Z

SGTM 🖖 but... I'm not sure if `kjobctl.x-k8s.io/slurm-script-name` is the best name for the annotation. I think the best person to make that decision would be @mwielgus.
