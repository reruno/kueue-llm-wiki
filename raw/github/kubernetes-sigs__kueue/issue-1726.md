# Issue #1726: Job gets admitted, but is never un-suspended.

**Summary**: Job gets admitted, but is never un-suspended.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1726

**Last updated**: 2024-02-23T15:14:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@xmolitann](https://github.com/xmolitann)
- **Created**: 2024-02-13T13:26:29Z
- **Updated**: 2024-02-23T15:14:03Z
- **Closed**: 2024-02-23T15:14:03Z
- **Labels**: `kind/bug`, `triage/needs-information`
- **Assignees**: _none_
- **Comments**: 40

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

Job submitted, workload got created and admitted that job. Job was never un-suspended. I tried to patch Job to `suspend: false`, but it immediately got suspended again.

There are multiple identical errors from kueue:

```json
{
  "level": "error",
  "ts": "2024-02-12T08:30:42.026624587Z",
  "caller": "jobframework/reconciler.go:335",
  "msg": "Handling job with no workload",
  "controller": "job",
  "controllerGroup": "batch",
  "controllerKind": "Job",
  "Job": {
    "name": "ml-job-annotator-gt-webface-gpu",
    "namespace": "pgrunt"
  },
  "namespace": "pgrunt",
  "name": "ml-job-annotator-gt-webface-gpu",
  "reconcileID": "edba044d-1ece-4364-8c6a-c0dc66907553",
  "job": "pgrunt/ml-job-annotator-gt-webface-gpu",
  "gvk": "batch/v1, Kind=Job",
  "error": "workloads.kueue.x-k8s.io \"job-ml-job-annotator-gt-webface-gpu-ff6d8\" already exists",
  "stacktrace": "sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:335\nsigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile\n\t/workspace/pkg/controller/jobframework/reconciler.go:1007\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:119\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.0/pkg/internal/controller/controller.go:227"
}
```

Cluster, local queue

```yaml
NapiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"kueue.x-k8s.io/v1beta1","kind":"ClusterQueue","metadata":{"annotations":{},"name":"cq-all-resources"},"spec":{"flavorFungibility":{"whenCanBorrow":"Borrow","whenCanPreempt":"TryNextFlavor"},"namespaceSelector":{},"preemption":{"reclaimWithinCohort":"Never","withinClusterQueue":"Never"},"queueingStrategy":"StrictFIFO","resourceGroups":[{"coveredResources":["nvidia.com/gpu"],"flavors":[{"name":"gpu-a40","resources":[{"name":"nvidia.com/gpu","nominalQuota":8}]},{"name":"gpu-a100","resources":[{"name":"nvidia.com/gpu","nominalQuota":4}]}]},{"coveredResources":["cpu","memory","ephemeral-storage","github.com/fuse","pods"],"flavors":[{"name":"default-flavor","resources":[{"name":"cpu","nominalQuota":256},{"name":"memory","nominalQuota":"2Ti"},{"name":"ephemeral-storage","nominalQuota":"2Ti"},{"name":"github.com/fuse","nominalQuota":"10k"},{"name":"pods","nominalQuota":220}]}]}]}}
  creationTimestamp: "2024-02-07T14:30:12Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 4
  name: cq-all-resources
  resourceVersion: "336378666"
  uid: cb3e70ae-714d-4aa4-8edc-0b76041d24b9
spec:
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector: {}
  preemption:
    borrowWithinCohort:
      policy: Never
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  queueingStrategy: StrictFIFO
  resourceGroups:
  - coveredResources:
    - nvidia.com/gpu
    flavors:
    - name: gpu-a40
      resources:
      - name: nvidia.com/gpu
        nominalQuota: 8
    - name: gpu-a100
      resources:
      - name: nvidia.com/gpu
        nominalQuota: 4
  - coveredResources:
    - cpu
    - memory
    - ephemeral-storage
    - github.com/fuse
    - pods
    flavors:
    - name: default-flavor
      resources:
      - name: cpu
        nominalQuota: 256
      - name: memory
        nominalQuota: 2Ti
      - name: ephemeral-storage
        nominalQuota: 2Ti
      - name: github.com/fuse
        nominalQuota: 10k
      - name: pods
        nominalQuota: 220
  stopPolicy: None
status:
  admittedWorkloads: 1
  conditions:
  - lastTransitionTime: "2024-02-07T14:31:07Z"
    message: Can admit new workloads
    reason: Ready
    status: "True"
    type: Active
  flavorsReservation:
  - name: gpu-a40
    resources:
    - borrowed: "0"
      name: nvidia.com/gpu
      total: "2"
  - name: gpu-a100
    resources:
    - borrowed: "0"
      name: nvidia.com/gpu
      total: "0"
  - name: default-flavor
    resources:
    - borrowed: "0"
      name: cpu
      total: "10"
    - borrowed: "0"
      name: ephemeral-storage
      total: 12Gi
    - borrowed: "0"
      name: github.com/fuse
      total: "0"
    - borrowed: "0"
      name: memory
      total: 45Gi
    - borrowed: "0"
      name: pods
      total: "1"
  flavorsUsage:
  - name: gpu-a40
    resources:
    - borrowed: "0"
      name: nvidia.com/gpu
      total: "2"
  - name: gpu-a100
    resources:
    - borrowed: "0"
      name: nvidia.com/gpu
      total: "0"
  - name: default-flavor
    resources:
    - borrowed: "0"
      name: cpu
      total: "10"
    - borrowed: "0"
      name: ephemeral-storage
      total: 12Gi
    - borrowed: "0"
      name: github.com/fuse
      total: "0"
    - borrowed: "0"
      name: memory
      total: 45Gi
    - borrowed: "0"
      name: pods
      total: "1"
  pendingWorkloads: 0
  reservingWorkloads: 1
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  creationTimestamp: "2024-02-07T14:33:08Z"
  generation: 1
  name: lq-all-resources
  namespace: pgrunt
  resourceVersion: "336378665"
  uid: 7f52812a-6752-4363-8eee-4789bb2d6358
spec:
  clusterQueue: cq-all-resources
status:
  admittedWorkloads: 1
  conditions:
  - lastTransitionTime: "2024-02-07T14:33:08Z"
    message: Can submit new workloads to clusterQueue
    reason: Ready
    status: "True"
    type: Active
  flavorUsage:
  - name: gpu-a40
    resources:
    - name: nvidia.com/gpu
      total: "2"
  - name: gpu-a100
    resources:
    - name: nvidia.com/gpu
      total: "0"
  - name: default-flavor
    resources:
    - name: cpu
      total: "10"
    - name: ephemeral-storage
      total: 12Gi
    - name: github.com/fuse
      total: "0"
    - name: memory
      total: 45Gi
    - name: pods
      total: "1"
  flavorsReservation:
  - name: gpu-a40
    resources:
    - name: nvidia.com/gpu
      total: "2"
  - name: gpu-a100
    resources:
    - name: nvidia.com/gpu
      total: "0"
  - name: default-flavor
    resources:
    - name: cpu
      total: "10"
    - name: ephemeral-storage
      total: 12Gi
    - name: github.com/fuse
      total: "0"
    - name: memory
      total: 45Gi
    - name: pods
      total: "1"
  pendingWorkloads: 0
  reservingWorkloads: 1
```

Job.yaml

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app: ml-job
    kueue.x-k8s.io/queue-name: lq-all-resources
    kueue.x-k8s.io/priority-class: ml-low
  name: ml-job-webface-mapping-this_is_placeholder
spec:
  backoffLimit: 0
  suspend: true
  template:
    metadata:
      name: ml-job
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/hostname
                operator: In
                values:
                - hawking
      containers:
      - command:
        - bash
        - -c
        - |
          export PATH="/opt/venv/bin/:${PATH}" &&
          cd /data/workspace/facekit &&
          pip install -e . &&
          facekit face_annotator multiface ${WORKLOAD_ARGS} --processes 30
        env:
        - name: GIT_REPO
          value: "redacted"
        - name: GIT_CHECKOUT_BRANCH
          value: "redacted"
        - name: WORKLOAD_ARGS
          value: ""
        - name: OMP_NUM_THREADS
          value: "1"
        - name: NUMEXPR_NUM_THREADS
          value: "1"
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              key: AWS_ACCESS_KEY_ID
              name: user-credentials
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              key: AWS_SECRET_ACCESS_KEY
              name: user-credentials
        - name: CLEARML_API_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              key: CLEARML_API_ACCESS_KEY
              name: user-credentials
        - name: CLEARML_API_SECRET_KEY
          valueFrom:
            secretKeyRef:
              key: CLEARML_API_SECRET_KEY
              name: user-credentials
        image: "redacted"
        imagePullPolicy: Always
        name: ml-main
        resources:
          limits:
            cpu: 100
            ephemeral-storage: 120Gi
            memory: 80Gi
            nvidia.com/gpu: "2"
          requests:
            cpu: 30
            ephemeral-storage: 120Gi
            memory: 45Gi
        securityContext:
          privileged: true
        volumeMounts:
        - mountPath: /data/user
          name: user-configuration
        - mountPath: /data/workspace
          name: workspace
        - mountPath: /srv/dvc_cache/
          name: dvc-cache
        - mountPath: /mnt/nas.brno/
          name: nas-brno
        - mountPath: /etc/redacted/
          name: iengine-lic
        - mountPath: /dev/shm
          name: dev-shm
        - mountPath: /mnt/data/downloader
          name: downloader
        - mountPath: /encrypted/INC-12499
          name: wiki-hdd
        - mountPath: /root
          name: user-home-dev-pod-0
        workingDir: /data/workspace
      imagePullSecrets:
      - name: registry-credentials
      initContainers:
      - command:
        - bash
        - -c
        - |
          if [[ ! -d "/root/.ssh" ]]; then
            mkdir ~/.ssh &&
            mkdir ~/.kube &&
            cp /data/user/id_* ~/.ssh &&
            cp /data/user/.git* ~/ &&
            cp /data/user/kubeconfig ~/.kube/config &&
            ssh-keyscan -p 7999 -t rsa redacted > ~/.ssh/known_hosts &&
            cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys &&
            chmod 600 ~/.ssh/id_rsa &&
            git clone $GIT_REPO &&
            cd "$(basename "$GIT_REPO" .git)" &&
            git checkout $GIT_CHECKOUT_BRANCH
          fi
        env:
        - name: GIT_REPO
          value: "redacted"
        - name: GIT_CHECKOUT_BRANCH
          value: "redacted"
        image: bitnami/git:latest
        name: init-git-repo
        resources:
          limits:
            cpu: 250m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 512Mi
        volumeMounts:
        - mountPath: /data/user
          name: user-configuration
        - mountPath: /data/workspace
          name: workspace
        workingDir: /data/workspace
      priorityClassName: ml-low
      restartPolicy: Never
      runtimeClassName: nvidia
      volumes:
      - name: user-configuration
        projected:
          sources:
          - secret:
              items:
              - key: id_rsa
                path: id_rsa
              - key: id_rsa.pub
                path: id_rsa.pub
              - key: .git-credentials
                path: .git-credentials
              - key: kubeconfig
                path: kubeconfig
              name: user-credentials
          - configMap:
              items:
              - key: .gitconfig
                path: .gitconfig
              name: gitconfig
          - configMap:
              items:
              - key: clearml.conf
                path: clearml.conf
              name: clearml.conf
      - hostPath:
          path: /srv/dvc_cache/
        name: dvc-cache
      - emptyDir: {}
        name: workspace
      - hostPath:
          path: /mnt/nas.brno
        name: nas-brno
      - configMap:
          name: iengine.lic
        name: iengine-lic
      - emptyDir:
          medium: Memory
          sizeLimit: 1Gi
        name: dev-shm
      - hostPath:
          path: /mnt/data/downloader
        name: downloader
      - hostPath:
          path: /encrypted/INC-12499
        name: wiki-hdd
      - name: user-home-dev-pod-0
        persistentVolumeClaim:
          claimName: user-home-dev-pod-0
  ttlSecondsAfterFinished: 1200

```

The Worklaod object has status:

```yaml
Conditions:
Last Transition Time: 2024-02-11T10:42:40Z
Message: Quota reserved in ClusterQueue cq-all-resources
Reason: QuotaReserved
Status: True
Type: QuotaReserved
Last Transition Time: 2024-02-11T10:42:40Z
Message: The workload is admitted
Reason: Admitted Status: True
Type: Admitted
```

**What you expected to happen**:

Job gets un-suspended, Pod is created and running.

**How to reproduce it (as minimally and precisely as possible)**:

Create cluster+local queue and try submitting job mentioned above.

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cq-all-resources
spec:
  preemption:
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  queueingStrategy: StrictFIFO
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: gpu-a40
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 8
        - name: gpu-a100
          resources:
            - name: "nvidia.com/gpu"
              nominalQuota: 4
    - coveredResources: ["cpu", "memory", "ephemeral-storage", "github.com/fuse", "pods"]
      flavors:
      - name: "default-flavor"
        resources:
        - name: "cpu"
          nominalQuota: 256
        - name: "memory"
          nominalQuota: 2Ti
        - name: "ephemeral-storage"
          nominalQuota: 2Ti
        - name: "github.com/fuse"
          nominalQuota: 10k
        - name: "pods"
          nominalQuota: 220
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: pgrunt
  name: lq-all-resources
spec:
  clusterQueue: cq-all-resources
```

**Anything else we need to know?**:

I guess that's all, let me know if you need some more information and I will happily provide.

**Environment**:

- Kubernetes version (use `kubectl version`): Server Version: v1.26.10+rke2r2
- Kueue version (use `git describe --tags --dirty --always`): 0.5.2 installed via 0.1.0 Helm chart
- Cloud provider or hardware configuration: on-prem, 8x NVIDIA-A40, AMD EPYC 7502, 1TB RAM
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.3 LTS
- Kernel (e.g. `uname -a`): 5.15.0-79-generic
- Install tools: Helm v3.11.2, Kustomize v5.0.4-0.20230601165947-6ce0bf390ce3

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T14:07:04Z

cc @mimowo @trasc 
for ideas

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T14:10:48Z

Can you tell me how many characters did the job name have?
I wonder if it's something related to that.

EDIT:
I suppose it's `ml-job-annotator-gt-webface-gpu`, which is 31 characters.
This is pretty low, compared to the size limit of 63 for CRD names.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T14:13:36Z

`ml-job-annotator-gt-webface-gpu` which is 31

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-13T14:14:00Z

Also, it might be helpful if you could show as the output for 
`kubectl describe workloads/<workload_name>` and  `kubectl describe jobs/<job_name>`
EDIT; as this commands will also give us events

### Comment by [@trasc](https://github.com/trasc) — 2024-02-13T14:14:49Z

> Also, it might be helpful if you could show as the output for `kubectl describe workloads/<workload_name>` and `kubectl describe jobs/<job_name>`

Maybe the full yaml of the workload is better

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-13T14:15:43Z

> Maybe the full yaml of the workload is better

this can be handy as well `kubectl get workloads/<workload_name> -oyaml`

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T14:17:43Z

Heres the workload, but unfortunately, I no longer have the job and our cluster is fully booked atm. :(

```yaml
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta1
  kind: Workload
  metadata:
    creationTimestamp: "2024-02-11T10:42:40Z"
    generation: 3
    labels:
      kueue.x-k8s.io/job-uid: a6f3d317-9ab2-44ee-917e-690fd4d29668
    name: job-ml-job-annotator-gt-webface-gpu-ff6d8
    namespace: pgrunt
    resourceVersion: "336381385"
    uid: feb1af8b-abe6-4b35-a6f2-29a808a3416f
  spec:
    active: true
    podSets:
    - count: 1
      name: main
      template:
        metadata:
          name: ml-job-annotator-gt-webface-gpu
        spec:
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: kubernetes.io/hostname
                    operator: In
                    values:
                    - hawking
          containers:
          - command:
            - bash
            - -c
            - |
              export PATH="/opt/venv/bin/:${PATH}" &&
              cd /data/workspace/facekit &&
              pip install -e . &&
              facekit face_annotator multiface ${WORKLOAD_ARGS} --processes 20
            env:
            - name: GIT_REPO
              value: "redacted"
            - name: GIT_CHECKOUT_BRANCH
              value: "redacted"
            - name: WORKLOAD_ARGS
              value: ' --input-path /mnt/data/downloader/wikidata/crawled_identities/gt_images.h5
                --output-path /mnt/data/downloader/wikidata/crawled_identities/gt_images_annotated_webface.h5 '
            - name: OMP_NUM_THREADS
              value: "1"
            - name: NUMEXPR_NUM_THREADS
              value: "1"
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  key: AWS_ACCESS_KEY_ID
                  name: user-credentials
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  key: AWS_SECRET_ACCESS_KEY
                  name: user-credentials
            - name: CLEARML_API_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  key: CLEARML_API_ACCESS_KEY
                  name: user-credentials
            - name: CLEARML_API_SECRET_KEY
              valueFrom:
                secretKeyRef:
                  key: CLEARML_API_SECRET_KEY
                  name: user-credentials
            image: "redacted"
            imagePullPolicy: Always
            name: ml-main
            resources:
              limits:
                cpu: "20"
                ephemeral-storage: 12Gi
                memory: 80Gi
                nvidia.com/gpu: "2"
              requests:
                cpu: "10"
                ephemeral-storage: 12Gi
                memory: 45Gi
            securityContext:
              privileged: true
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /data/user
              name: user-configuration
            - mountPath: /data/workspace
              name: workspace
            - mountPath: /srv/dvc_cache/
              name: dvc-cache
            - mountPath: /mnt/nas.brno/
              name: nas-brno
            - mountPath: /dev/shm
              name: dev-shm
            - mountPath: /mnt/data/downloader
              name: downloader
            - mountPath: /encrypted/INC-12499
              name: wiki-hdd
            workingDir: /data/workspace
          dnsPolicy: ClusterFirst
          imagePullSecrets:
          - name: registry-credentials
          initContainers:
          - command:
            - bash
            - -c
            - |
              if [[ ! -d "/root/.ssh" ]]; then
                mkdir ~/.ssh &&
                mkdir ~/.kube &&
                cp /data/user/id_* ~/.ssh &&
                cp /data/user/.git* ~/ &&
                cp /data/user/kubeconfig ~/.kube/config &&
                ssh-keyscan -p 7999 -t rsa "redacted" > ~/.ssh/known_hosts &&
                cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys &&
                chmod 600 ~/.ssh/id_rsa &&
                git clone $GIT_REPO &&
                cd "$(basename "$GIT_REPO" .git)" &&
                git checkout $GIT_CHECKOUT_BRANCH
              fi
            env:
            - name: GIT_REPO
              value: "redacted"
            - name: GIT_CHECKOUT_BRANCH
              value: "redacted"
            image: bitnami/git:latest
            imagePullPolicy: Always
            name: init-git-repo
            resources:
              limits:
                cpu: 250m
                memory: 512Mi
              requests:
                cpu: 100m
                memory: 512Mi
            terminationMessagePath: /dev/termination-log
            terminationMessagePolicy: File
            volumeMounts:
            - mountPath: /data/user
              name: user-configuration
            - mountPath: /data/workspace
              name: workspace
            workingDir: /data/workspace
          priorityClassName: ml-low
          restartPolicy: Never
          runtimeClassName: nvidia
          schedulerName: default-scheduler
          securityContext: {}
          terminationGracePeriodSeconds: 30
          volumes:
          - name: user-configuration
            projected:
              defaultMode: 420
              sources:
              - secret:
                  items:
                  - key: id_rsa
                    path: id_rsa
                  - key: id_rsa.pub
                    path: id_rsa.pub
                  - key: .git-credentials
                    path: .git-credentials
                  - key: kubeconfig
                    path: kubeconfig
                  name: user-credentials
              - configMap:
                  items:
                  - key: .gitconfig
                    path: .gitconfig
                  name: gitconfig
              - configMap:
                  items:
                  - key: clearml.conf
                    path: clearml.conf
                  name: clearml.conf
          - hostPath:
              path: /srv/dvc_cache/
              type: ""
            name: dvc-cache
          - emptyDir: {}
            name: workspace
          - hostPath:
              path: /mnt/nas.brno
              type: ""
            name: nas-brno
          - configMap:
              defaultMode: 420
              name: iengine.lic
            name: iengine-lic
          - emptyDir:
              medium: Memory
              sizeLimit: 1Gi
            name: dev-shm
          - hostPath:
              path: /mnt/data/downloader
              type: ""
            name: downloader
          - hostPath:
              path: /encrypted/INC-12499
              type: ""
            name: wiki-hdd
    priority: 10
    priorityClassName: ml-low
    priorityClassSource: kueue.x-k8s.io/workloadpriorityclass
    queueName: lq-all-resources
  status:
    admission:
      clusterQueue: cq-all-resources
      podSetAssignments:
      - count: 1
        flavors:
          cpu: default-flavor
          ephemeral-storage: default-flavor
          memory: default-flavor
          nvidia.com/gpu: gpu-a40
          pods: default-flavor
        name: main
        resourceUsage:
          cpu: "10"
          ephemeral-storage: 12Gi
          memory: 45Gi
          nvidia.com/gpu: "2"
          pods: "1"
    conditions:
    - lastTransitionTime: "2024-02-11T10:42:40Z"
      message: Quota reserved in ClusterQueue cq-all-resources
      reason: QuotaReserved
      status: "True"
      type: QuotaReserved
    - lastTransitionTime: "2024-02-11T10:42:40Z"
      message: The workload is admitted
      reason: Admitted
      status: "True"
      type: Admitted
kind: List
metadata:
  resourceVersion: ""
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-13T14:27:01Z

The pod template in the workload differs from the pod template for the job, for example in this line `facekit face_annotator multiface ${WORKLOAD_ARGS} --processes` (20 vs 30).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T14:30:16Z

But Kueue should be deleting those unmatching Workloads and create a new one. There is no deletion timestamp in the shared yaml (assuming it's the latest state).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T14:33:51Z

The Workload does not have a finalizer, meaning that Kueue removed it, but it somehow didn't call Delete? Or it did and it failed?

Do you see any log lines like: `deleting not matching workload` or `Deleted not matching workload`?

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T14:36:36Z

> The pod template in the workload differs from the pod template for the job, for example in this line `facekit face_annotator multiface ${WORKLOAD_ARGS} --processes` (20 vs 30).

Sorry, there were some edits afterwards from the developer, but nothing major shouldn't have changed

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T14:38:46Z

> The Workload does not have a finalizer, meaning that Kueue removed it, but it somehow didn't call Delete? Or it did and it failed?
> 
> Do you see any log lines like: `deleting not matching workload` or `Deleted not matching workload`?

No logs containing `not matching`

### Comment by [@trasc](https://github.com/trasc) — 2024-02-13T14:41:57Z

Indeed the workload is not matching the job and it should be deleted  but is not since it has no owner ref pointing to the job... , maybe the workload is left over from an older job with the same name potentially deleted wit `--cascade=orphan`.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T14:43:35Z

I will reply with fresh job+workload definitions, so they are 100% matching. Sorry if I caused any confusion so far.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T15:06:54Z

Unfortunately, if you don't specify a cascade option for Job, `orphan` is the default :(
Which could lead to this situation.

I wonder if we should just delete orphan Workloads... or is it user error to orphan a Workload and we shouldn't remove the object because the user has not chosen to delete it (by not using a different cascade).

But let's leave this investigation for now.

/triage needs-information

### Comment by [@trasc](https://github.com/trasc) — 2024-02-13T15:13:04Z

> Unfortunately, if you don't specify a cascade option for Job, `orphan` is the default :(

I think it should be background.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T15:29:33Z

Job is the only k8s API that uses orphan as default, instead of background... I know, pretty bad, but we can't change it, because of backwards compatibility.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-13T16:23:30Z

`kubectl delete` uses `background` by default. How did you (or your user) delete the old Job?

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-13T16:26:05Z

via `k9s` `ctrl+d` which defaults to `Background`. I will post the new job+workload tomorrow, sorry for the delay.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T08:01:51Z

> I will reply with fresh job+workload definitions, so they are 100% matching. Sorry if I caused any confusion so far.

Thanks, this will be great. IIUC the current hypothesis is that the job got deleted, the workload stayed, and the job was recreated by the user with a slightly different pod spec, causing the issue. It would be good to confirm the scenario.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T11:00:49Z

I got slack confirmation from @trasc that deleting a job with `--cascade=orphan` and recreating (I assume with slightly different spec) leads to the observed behavior. In that case I'm wondering if as a fix we could detect this situation (the target workload has a non-existing job owner) and recreate the workload.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T14:10:08Z

@xmolitann Could you confirm if that happened? And if so, what was the motivation to use `--cascade=orphan`? We are not sure what the correct behavior should be. Options are:
1. Create a new workload with a new name, to avoid the collision
2. Inherit the existing workload. this would have the effect that the job would preserve its place in the queue, or be directly unsuspended, if the workload is admitted.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T14:27:35Z

How about not inheriting but recreating the workload, so that there is still maintain equivalence between the job and the workload

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-02-14T16:08:16Z

> I got slack confirmation from @trasc that deleting a job with `--cascade=orphan` and recreating (I assume with slightly different spec) leads to the observed behavior. In that case I'm wondering if as a fix we could detect this situation (the target workload has a non-existing job owner) and recreate the workload.

I can confirm this, because when I delete the job with `background`, the workloads gets deleted as well, I can then re-submit the jobs and pod gets admitted. When I delete it with `orphan`, what you are mentioning happens. So this is rather user error than bug, sorry for confusion. What to do with this behavior I will leave up to you. I guess more verbose error message would be fine.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T16:42:39Z

In case I wasn't clear I think the issue is rather narrow scope, as this is the following scenario:
1. job is created and the workload is created by Kueue
2. job is deleted by the user with `cascade=orphan`
3. job template is modified by the user, and re-created with the same name
4. Issue: the attempt to create a workload fails, because one orphaned workload already exists.

My proposal is to fix it in a least intrusive manner: when we get "Already exists error" (step 4.), then fetch the workload, and verify if the workload is orphaned. If the workload is orphaned, then delete it, which will allow the new workload to be recreated in its place. This does not entail inheriting an existing workload necessarily. As a performance optimization we **could** inherit such an orphan workload, but I think only if we detect the job template is still equivalent with the workload.

### Comment by [@trasc](https://github.com/trasc) — 2024-02-14T16:53:26Z

In my opinion a workload should be dedicated to a job (k8s object). 
By deleting and creating a new job with the same name you get another object.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T16:56:10Z

I kind of like the idea of just using the UID. However @trasc can you verify what happens when you upgrade kueue? Do we make assumptions about the workload name?

The other point is that if the orphan Workload is not deleted and is not finished, it's consuming quota on the kueue. So maybe that's an argument for garbage collecting it. Or at least marking it Finished.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T16:56:45Z

> By deleting and creating a new job with the same name you get another object.

The proposal https://github.com/kubernetes-sigs/kueue/issues/1726#issuecomment-1944206289 is compatible with this. We don't reuse the workload, but recreate.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T16:57:20Z

I agree that it's compatible, but it's more steps.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T16:58:51Z

I'm also hesitant about using UIDs because it makes the workload names virtually random. Having predictable workload names is a nice feature which can be useful for some users, even for us when documenting features.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T16:59:14Z

> I agree that it's compatible, but it's more steps.

Yes, but it is more steps only in this situation, which should be rare anyway.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-14T17:06:13Z

> The other point is that if the orphan Workload is not deleted and is not finished, it's consuming quota on the kueue. So maybe that's an argument for garbage collecting it. Or at least marking it Finished.

Yes, I like the idea of marking orphan workloads as finished (or even deleting), by some form of garbage collection, The fix for leftiever orphan workloads is needed regardless if we go with UIDs or workload recreation solutions.

### Comment by [@trasc](https://github.com/trasc) — 2024-02-14T17:51:49Z

In my opinion the fist step is 

- #1732 

then add a garbage collection scheme.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T18:55:11Z

> I'm also hesitant about using UIDs because it makes the workload names virtually random

We already add a hash at the end of the name, so it's not immediately obvious how to get from the job name to the workload name.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-15T07:29:29Z

> We already add a hash at the end of the name, so it's not immediately obvious how to get from the job name to the workload name.

Right, but if you repeat some script multiple times it is enough to check once the workload name. For example in Kueue periodic tests we can find the same workload names when comparing different runs.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-15T07:40:08Z

I think the following concerns are still valid:
1. ~this will cause all running jobs to stop as the workloads will not match during upgrade, all pending jobs are requeued~
2. the random workload names might be an inconvenience for some users, for example those who periodically run cronjob and want to compare logs
3. this does not really solve the issue, just makes it less likely given 5-character name, this is 1/16mln, but at scale some users may still hit it, then repro and figuring out the cause will be very difficult

Thus I think it is reasonable to rethink if there are alternatives. I admit in the other approach we need 3 requests (one to detect conflict, one to fetch the new workload, one to check there is no owner reference in the workload), so not ideal either. 

How about just deleting a workload from `workload_controller` in reaction to removed `metadata.ownerReference` (by kube garbage-collector) which removes it in the "orphan" mode? I think this would also solve the issue. One downside I see is that we would still delete even though "--cascade=orphan" is used.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-02-15T08:11:47Z

> this will cause all running jobs to stop as the workloads will not match during upgrade, all pending jobs are requeued

Actually, I'm not sure about this (didn't test). Now I think there actually may not be impact here, because the workload with the old scheme can still support the job, based on the ownerReference. Sorry for confusing, in that case the remaining two points aren't that relevant probably. 

EDIT: I now tested by changing the workload name scheme, and upgraded in-place. The old job continues to run. Once again sorry for confusing. Given that (2.) and (3.) and not big concerns, I ok with https://github.com/kubernetes-sigs/kueue/issues/1726#issuecomment-1944319301.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-15T08:26:39Z

> However @trasc can you verify what happens when you upgrade kueue? Do we make assumptions about the workload name?

@trasc This is my main concern against generating a hash with UID. If the workload is recreated and the readmission or termination against existing Jobs happens, including uid in has would be barriers for updating the kueue version.

### Comment by [@trasc](https://github.com/trasc) — 2024-02-15T11:39:09Z

> > However @trasc can you verify what happens when you upgrade kueue? Do we make assumptions about the workload name?
> 
> @trasc This is my main concern against generating a hash with UID. If the workload is recreated and the readmission or termination against existing Jobs happens, including uid in has would be barriers for updating the kueue version.

The name is only used when creating the workload, after that we only use the owner references to "connect" the wl to its job. In case of kueue upgrade, the old wl will be paired with the jobs based on owner refs (regardless of names), newer workloads are created using the new naming method.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-15T13:30:59Z

> > > However @trasc can you verify what happens when you upgrade kueue? Do we make assumptions about the workload name?
> > 
> > 
> > @trasc This is my main concern against generating a hash with UID. If the workload is recreated and the readmission or termination against existing Jobs happens, including uid in has would be barriers for updating the kueue version.
> 
> The name is only used when creating the workload, after that we only use the owner references to "connect" the wl to its job. In case of kueue upgrade, the old wl will be paired with the jobs based on owner refs (regardless of names), newer workloads are created using the new naming method.

That makes sense. I'm fine with including a UID in the hash.
