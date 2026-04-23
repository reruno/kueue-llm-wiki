# Issue #961: MPI job example cannot find /home/mpiuser/.ssh

**Summary**: MPI job example cannot find /home/mpiuser/.ssh

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/961

**Last updated**: 2023-07-26T17:26:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@vsoch](https://github.com/vsoch)
- **Created**: 2023-07-07T19:35:57Z
- **Updated**: 2023-07-26T17:26:24Z
- **Closed**: 2023-07-26T17:26:24Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 16

## Description

I'm trying to reproduce the example here: https://github.com/kubernetes-sigs/kueue/blob/main/site/static/examples/sample-mpijob.yaml

And first I was doing it from Python, but have reproduced the same applying that YAML file. Basically, it isn't able to find the directory for the .ssh at `/home/mpiuser/.ssh`

```console
Events:
  Type     Reason     Age   From               Message
  ----     ------     ----  ----               -------
  Normal   Scheduled  3s    default-scheduler  Successfully assigned default/pi-launcher-kg2jp to kind-control-plane
  Normal   Pulled     3s    kubelet            Container image "mpioperator/mpi-pi:openmpi" already present on machine
  Warning  Failed     3s    kubelet            Error: cannot find volume "ssh-auth" to mount into container "mpi-launcher"
```
And as a result the launchers seem to terminate and then generate again, ad-infinitum! I am testing using Kind, and perhaps that might be related? Or it could be that a change to the MPI operator is out of sync with the example here. When I can get this working, I have a full example of doing this in Python to contribute here. Thank you!

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-07T19:45:37Z

How did you install the MPI operator?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-07T19:50:09Z

Maybe @tenzen-y has some clue

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-07T19:51:14Z

> How did you install the MPI operator?

I am writing docs for kueue, so I used the latest in development (so it wouldn't present an old version we need to update):

```bash
kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v2beta1/mpi-operator.yaml
```
But that's a good idea - let me try the release instead.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-07T19:51:47Z

_When your user docs become true..._

![image](https://github.com/kubernetes-sigs/kueue/assets/814322/22170454-3095-4480-b932-cd47f80a9a9e)

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-07T19:55:35Z

Ah, didn't seem to make a difference:

```
Events:
  Type     Reason     Age   From               Message
  ----     ------     ----  ----               -------
  Normal   Scheduled  1s    default-scheduler  Successfully assigned default/pi-launcher-rqzwz to kind-control-plane
  Normal   Pulled     1s    kubelet            Container image "mpioperator/mpi-pi:openmpi" already present on machine
  Warning  Failed     1s    kubelet            Error: cannot find volume "ssh-auth" to mount into container "mpi-launcher"
```
Going to look at the mpi-operator source code to see what `ssh-auth` is.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-07T19:59:03Z

okay looks like it might be a secret? https://github.com/kubeflow/mpi-operator/blob/0994cfd98407e8a87f7ac7c4c38c277f5a95beff/pkg/controller/mpi_job_controller.go#L1634-L1637

```yaml
$ kubectl describe  secret pi-ssh
Name:         pi-ssh
Namespace:    default
Labels:       app=pi
Annotations:  <none>


Type:  kubernetes.io/ssh-auth

Data
====
ssh-privatekey:  365 bytes
ssh-publickey:   253 bytes
```
I'm jumping into a meeting - will continue investigating and report back.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-07T20:12:31Z

Should it be mounted with rw? Why does it need write?

```
    Mounts:
      /etc/mpi from mpi-job-config (rw)
      /home/mpiuser/.ssh from ssh-auth (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-jq6wr (ro)
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-08T08:34:58Z

@vsoch I could not reproduce the `Error: cannot find volume "ssh-auth" to mount into container "mpi-launcher"` error...

Can you re-run the following commands in the new cluster?

```shell
$ kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v2beta1/mpi-operator.yaml
$ kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.4.0/manifests.yaml
$ kubectl apply -f https://github.com/kubernetes-sigs/kueue/blob/main/examples/single-clusterqueue-setup.yaml
$ kubectl apply -f https://github.com/kubernetes-sigs/kueue/blob/d40c3b8380ae2ce8314a7d232338261849eef18f/examples/sample-mpijob.yaml
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-08T08:45:00Z

> Should it be mounted with rw? Why does it need write?
> 
> ```
>     Mounts:
>       /etc/mpi from mpi-job-config (rw)
>       /home/mpiuser/.ssh from ssh-auth (rw)
>       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-jq6wr (ro)
> ```

IIUC, the launcher container doesn't need the write permission for the ssh-auth, although I have never tried to set the `ro` mode to ssh-auth in the launcher container.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-08T08:45:19Z

>  will continue investigating and report back.

Thanks!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-10T14:07:25Z

@vsoch can you share the launcher pod yaml?

It looks like mpi-operator failed to add the Volume into the Pod spec. Although I don't see how that would happen, unless some webhook is blocking it.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-22T01:04:20Z

okay looks like that older config works!

![image](https://github.com/kubernetes-sigs/kueue/assets/814322/ade759e7-74ee-46a2-8563-c3b64c3a24d8)

Now debugging - trying the same setup with the latest sample-mpijob.yaml - also works!

![image](https://github.com/kubernetes-sigs/kueue/assets/814322/dd8fb8af-bd25-4f0e-9075-35cbea749a9d)

Now I'm trying reversing the order of things - creating kueue first:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.4.0/manifests.yaml
# pause here to wait for it to come online
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/kueue/main/site/static/examples/single-clusterqueue-setup.yaml
kubectl apply -f https://raw.githubusercontent.com/kubeflow/mpi-operator/master/deploy/v2beta1/mpi-operator.yaml
kubectl apply -f site/static/examples/sample-mpijob.yaml
```
Ah! That reproduced it! Launcher are created infinitum and the job isn't run. 
```bash
$ kubectl logs pods/pi-
pods/pi-launcher-crhl5  pods/pi-launcher-xf7lv  pods/pi-worker-0        
pods/pi-launcher-smcsf  pods/pi-launcher-xjrlg  pods/pi-worker-1 
```
So this appears to be an order of operations thing - the MPI operator needs to be installed before Kueue. Any ideas why that might be? I'm going to try and reproduce this in Python again too. Worst case we can have a note about that.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-24T08:18:32Z

IIUC, the kueue-manager only launches controllers for CRDs (such as MPIJob) pre-installed in the cluster.

https://github.com/kubernetes-sigs/kueue/blob/b2e8c9d0632c25c75b3ee8dfeecdce2bb6037464/main.go#L323-L334

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-24T08:19:21Z

So, we need to install MPIJob CRD before deploying the kueue.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-24T13:53:42Z

> So, we need to install MPIJob CRD before deploying the kueue.

Yes, exactly! OR tweak the logic so the install is not dependent on the CRD.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-26T14:49:56Z

That's interesting. If Kueue is installed first, my intuition is that MPIJobs are simply skipped by Kueue (they just run without checking quota). Not sure how that would affect actual runtime.
