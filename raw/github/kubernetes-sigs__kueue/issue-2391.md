# Issue #2391: Workloads are not admitted when there are 3 or more Workloads in ClusterQueue

**Summary**: Workloads are not admitted when there are 3 or more Workloads in ClusterQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2391

**Last updated**: 2024-06-20T10:37:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@xmolitann](https://github.com/xmolitann)
- **Created**: 2024-06-10T14:29:33Z
- **Updated**: 2024-06-20T10:37:14Z
- **Closed**: 2024-06-19T08:18:43Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 19

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Sometimes, when there are 3+ Workloads waiting in ClusterQueue and they would fit in the quota, they are not admitted. They don't have any status or events. Reservation in quota doesn't happen. 

I increased `zap-log-level` to 6 and I can see this in logs, repeated over and over every ~2 seconds, even though it says 15 seconds in logs.:
![image](https://github.com/kubernetes-sigs/kueue/assets/43967691/0e5cac21-ca87-4627-8985-d1cece38b7d7)

It essentially schedules the workload, but it can take from X minutes to N hours...

Here's my configuration. I increased clientConnection.qps and burst to big values, but that didn't change anything. I also tried giving the deployment `kueue-controller-manager` unlimited resources, but it's barely using anything: ~20m CPU and ~100Mi memory.
```  controller_manager_config.yaml: |-
    apiVersion: config.kueue.x-k8s.io/v1beta1
    kind: Configuration
    health:
      healthProbeBindAddress: :8081
    metrics:
      bindAddress: :8080
    # enableClusterQueueResources: true
    webhook:
      port: 9443
    leaderElection:
      leaderElect: true
      resourceName: c1f6bfd2.kueue.x-k8s.io
    controller:
      groupKindConcurrency:
        Job.batch: 5
        Pod: 5
        Workload.kueue.x-k8s.io: 5
        LocalQueue.kueue.x-k8s.io: 1
        ClusterQueue.kueue.x-k8s.io: 1
        ResourceFlavor.kueue.x-k8s.io: 1
    clientConnection:
      qps: 5000
      burst: 20000
    #pprofBindAddress: :8082
    #waitForPodsReady:
    #  enable: true
    #manageJobsWithoutQueueName: true
    #internalCertManagement:
    #  enable: false
    #  webhookServiceName: ""
    #  webhookSecretName: ""
    integrations:
      frameworks:
      - "batch/job"
      - "pod"
      podOptions:
        namespaceSelector:
          matchExpressions:
            - key: kubernetes.io/metadata.name
              operator: NotIn
              values: [ "cattle-system", "calico-system", "cattle-monitoring-system", "cattle-logging-system", "cattle-provisioning-capi-system", "cattle-fleet-local-system", "cattle-fleet-system", "cattle-resources-system", "cattle", "calico", "nvidia", "tigera-operator", "label-studio", "postgres-ha", "minio-operator", "minio-tenant", "kube-system", "dlf", "directpv", "cert-manager", "longhorn-system", "postgresql-ha", "labelstudio", "coder", "harbor", "kueue-system", "kueue", "kyverno", "argocd" ]
        podSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values: [ "coder-workspace" ]
```

Values (I cut the configMap as it's posted here above):
```enablePrometheus: true
controllerManager:
  replicas: 3
  featureGates:
    - name: QueueVisibility
      enabled: true
    - name: VisibilityOnDemand
      enabled: true
```

ClusterQueue:
```apiVersion: kueue.x-k8s.io/v1beta1
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
  queueingStrategy: BestEffortFIFO
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory", "ephemeral-storage", "github.com/fuse", "pods", "nvidia.com/gpu"]
      flavors:
      - name: "hawking"
        resources:
        - name: "cpu"
          nominalQuota: 125
        - name: "memory"
          nominalQuota: 980Gi
        - name: "ephemeral-storage"
          nominalQuota: 9.85Ti
        - name: "github.com/fuse"
          nominalQuota: 5k
        - name: "pods"
          nominalQuota: 110
        - name: "nvidia.com/gpu"
          nominalQuota: 8
      - name: "euler"
        resources:
        - name: "cpu"
          nominalQuota: 61
        - name: "memory"
          nominalQuota: 488Gi
        - name: "ephemeral-storage"
          nominalQuota: 14Ti
        - name: "github.com/fuse"
          nominalQuota: 5k
        - name: "pods"
          nominalQuota: 110
        - name: "nvidia.com/gpu"
          nominalQuota: 9
      - name: "newton"
        resources:
        - name: "cpu"
          nominalQuota: 125
        - name: "memory"
          nominalQuota: 991Gi
        - name: "ephemeral-storage"
          nominalQuota: 19.7Ti
        - name: "github.com/fuse"
          nominalQuota: 5k
        - name: "pods"
          nominalQuota: 110
        - name: "nvidia.com/gpu"
          nominalQuota: 4
      - name: "godel"
        resources:
        - name: "cpu"
          nominalQuota: 253
        - name: "memory"
          nominalQuota: 980Gi
        - name: "ephemeral-storage"
          nominalQuota: 13.7Ti
        - name: "github.com/fuse"
          nominalQuota: 5k
        - name: "pods"
          nominalQuota: 110
        - name: "nvidia.com/gpu"
          nominalQuota: 8
      - name: "bayes"
        resources:
        - name: "cpu"
          nominalQuota: 125
        - name: "memory"
          nominalQuota: 991Gi
        - name: "ephemeral-storage"
          nominalQuota: 26636Gi
        - name: "github.com/fuse"
          nominalQuota: 5k
        - name: "pods"
          nominalQuota: 110
        - name: "nvidia.com/gpu"
          nominalQuota: 8
```

LocalQueue:
```apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
   namespace: rbenes
   name: lq-all-resources
spec:
   clusterQueue: cq-all-resources
```

Job:
```apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    batch.kubernetes.io/job-tracking: ""
  creationTimestamp: "2024-06-10T14:05:14Z"
  generation: 1
  labels:
    app: ml-job
    kueue.x-k8s.io/priority-class: ml-medium
    kueue.x-k8s.io/queue-name: lq-all-resources
  name: ml-job-online-filtering-6-4f6f9f6
  namespace: rbenes
  resourceVersion: "771281792"
  uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
spec:
  backoffLimit: 0
  completionMode: NonIndexed
  completions: 1
  parallelism: 1
  selector:
    matchLabels:
      batch.kubernetes.io/controller-uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
  suspend: true
  template:
    metadata:
      creationTimestamp: null
      labels:
        batch.kubernetes.io/controller-uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
        batch.kubernetes.io/job-name: ml-job-online-filtering-6-4f6f9f6
        controller-uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
        job-name: ml-job-online-filtering-6-4f6f9f6
      name: ml-job-online-filtering-6-4f6f9f6
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/hostname
                operator: NotIn
                values:
                - k8s-prod-master0
                - k8s-prod-master1
                - k8s-prod-master2
              - key: nvidia.com/gpu.memory
                operator: Gt
                values:
                - "4096"
      containers:
      - command:
        - bash
        - -c
        - |
          set -x &&
          cp /data/user/{.git*,clearml.conf} ~/ &&
          mkdir -p ~/.ssh &&
          cp /data/user/id_* ~/.ssh &&
          cp /data/user/.git* ~/ &&
          ssh-keyscan -p 7999 -t rsa foo.bar > ~/.ssh/known_hos
          cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys &&
          chmod 600 ~/.ssh/id_rsa &&
          ls -lha ~ &&
          ls -lha ~/.ssh &&
          ls -la &&
          cd iris-recognition &&
          HYDRA_FULL_ERROR=1 python train.py &&
          export tag="$(python -m solver.config.get_config_value --key tag)" &&
          export task_dir="$(python -m solver.config.get_config_value --key directories.task_dir)" &&
          export last_ckpt_path=$task_dir/trainings/$tag/ckpt/last.ckpt &&
          HYDRA_FULL_ERROR=1 python post_evaluate.py --model ${last_ckpt_path} --gpu 0 1
        env:
        - name: WORKLOAD_ARGS
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
        image: foo:bar
        imagePullPolicy: Always
        name: ml-main
        resources:
          limits:
            cpu: "30"
            ephemeral-storage: 5Gi
            memory: 70Gi
            nvidia.com/gpu: "4"
          requests:
            cpu: "30"
            ephemeral-storage: 3Gi
            memory: 70Gi
            nvidia.com/gpu: "4"
        securityContext:
          privileged: true
          runAsGroup: 6000
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /data/user/
          name: user-configuration
        - mountPath: /srv/
          name: srv
        - mountPath: /mnt/srv.remote/
          name: srv-remote
        - mountPath: /mnt/sandbox/
          name: shared-storage
        - mountPath: /data/workspace/
          name: workspace
        - mountPath: /mnt/nas.brno/
          name: nas-brno
        - mountPath: /dev/shm
          name: dev-shm
        workingDir: /data/workspace
      dnsPolicy: ClusterFirst
      imagePullSecrets:
      - name: registry-credentials
      initContainers:
      - command:
        - bash
        - -c
        - |
          mkdir ~/.ssh &&
          ssh-keyscan -p 7999 -t rsa foo > ~/.ssh/known_hosts &&
          cp /data/user/id_* ~/.ssh/ &&
          chmod 600 ~/.ssh/id_rsa &&
          git lfs install &&
          git clone $GIT_REPO &&
          cd "$(basename "$GIT_REPO" .git)"
          if ! [ -z "$GIT_CHECKOUT_REF" ]; then
            git checkout "$GIT_CHECKOUT_REF"
          elif ! [ -z "$GIT_CHECKOUT_BRANCH" ]; then
            git checkout "$GIT_CHECKOUT_BRANCH"
          else
            echo "Please set either GIT_CHECKOUT_REF or GIT_CHECKOUT_BRANCH!"
            exit 1
          fi
          git submodule update --init
        env:
        - name: GIT_REPO
          value: foo:bar
        - name: GIT_CHECKOUT_REF
          value: 4f6f9f6
        - name: GIT_CLONE_PROTECTION_ACTIVE
          value: "false"
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
      priorityClassName: ml-medium
      restartPolicy: Never
      runtimeClassName: nvidia
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      volumes:
      - emptyDir:
          medium: Memory
          sizeLimit: 2Gi
        name: dev-shm
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
          path: /srv/
          type: ""
        name: srv
      - hostPath:
          path: /mnt/sandbox/
          type: ""
        name: shared-storage
      - hostPath:
          path: /mnt/srv.remote/
          type: ""
        name: srv-remote
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
  ttlSecondsAfterFinished: 1209600
status:
  conditions:
  - lastProbeTime: "2024-06-10T14:05:14Z"
    lastTransitionTime: "2024-06-10T14:05:14Z"
    message: Job suspended
    reason: JobSuspended
    status: "True"
    type: Suspended
  ready: 0
  uncountedTerminatedPods: {}
```

Workload:
```apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2024-06-10T14:05:14Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  labels:
    kueue.x-k8s.io/job-uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
  name: job-ml-job-online-filtering-6-4f6f9f6-9a073
  namespace: rbenes
  ownerReferences:
  - apiVersion: batch/v1
    blockOwnerDeletion: true
    controller: true
    kind: Job
    name: ml-job-online-filtering-6-4f6f9f6
    uid: 2e40d4dd-48f3-48fc-9d42-577e6cbf9f12
  resourceVersion: "771281796"
  uid: c7d282a7-8deb-493d-85dc-5ff4fee05b7b
spec:
  active: true
  podSets:
  - count: 1
    name: main
    template:
      metadata:
        name: ml-job-online-filtering-6-4f6f9f6
      spec:
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname
                  operator: NotIn
                  values:
                  - k8s-prod-master0
                  - k8s-prod-master1
                  - k8s-prod-master2
                - key: nvidia.com/gpu.memory
                  operator: Gt
                  values:
                  - "4096"
        containers:
        - command:
          - bash
          - -c
          - |
            set -x &&
            cp /data/user/{.git*,clearml.conf} ~/ &&
            mkdir -p ~/.ssh &&
            cp /data/user/id_* ~/.ssh &&
            cp /data/user/.git* ~/ &&
            ssh-keyscan -p 7999 -t rsa foo > ~/.ssh/known_hos
            cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys &&
            chmod 600 ~/.ssh/id_rsa &&
            ls -lha ~ &&
            ls -lha ~/.ssh &&
            ls -la &&
            cd iris-recognition &&
            HYDRA_FULL_ERROR=1 python train.py &&
            export tag="$(python -m solver.config.get_config_value --key tag)" &&
            export task_dir="$(python -m solver.config.get_config_value --key directories.task_dir)" &&
            export last_ckpt_path=$task_dir/trainings/$tag/ckpt/last.ckpt &&
            HYDRA_FULL_ERROR=1 python post_evaluate.py --model ${last_ckpt_path} --gpu 0 1
          env:
          - name: WORKLOAD_ARGS
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
          image: foo:bar
          imagePullPolicy: Always
          name: ml-main
          resources:
            limits:
              cpu: "30"
              ephemeral-storage: 5Gi
              memory: 70Gi
              nvidia.com/gpu: "4"
            requests:
              cpu: "30"
              ephemeral-storage: 3Gi
              memory: 70Gi
              nvidia.com/gpu: "4"
          securityContext:
            privileged: true
            runAsGroup: 6000
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
          volumeMounts:
          - mountPath: /data/user/
            name: user-configuration
          - mountPath: /srv/
            name: srv
          - mountPath: /mnt/srv.remote/
            name: srv-remote
          - mountPath: /mnt/sandbox/
            name: shared-storage
          - mountPath: /data/workspace/
            name: workspace
          - mountPath: /mnt/nas.brno/
            name: nas-brno
          - mountPath: /dev/shm
            name: dev-shm
          workingDir: /data/workspace
        dnsPolicy: ClusterFirst
        imagePullSecrets:
        - name: registry-credentials
        initContainers:
        - command:
          - bash
          - -c
          - |
            mkdir ~/.ssh &&
            ssh-keyscan -p 7999 -t rsa foo > ~/.ssh/known_hosts &&
            cp /data/user/id_* ~/.ssh/ &&
            chmod 600 ~/.ssh/id_rsa &&
            git lfs install &&
            git clone $GIT_REPO &&
            cd "$(basename "$GIT_REPO" .git)"
            if ! [ -z "$GIT_CHECKOUT_REF" ]; then
              git checkout "$GIT_CHECKOUT_REF"
            elif ! [ -z "$GIT_CHECKOUT_BRANCH" ]; then
              git checkout "$GIT_CHECKOUT_BRANCH"
            else
              echo "Please set either GIT_CHECKOUT_REF or GIT_CHECKOUT_BRANCH!"
              exit 1
            fi
            git submodule update --init
          env:
          - name: GIT_REPO
            value: foo:bar
          - name: GIT_CHECKOUT_REF
            value: 4f6f9f6
          - name: GIT_CLONE_PROTECTION_ACTIVE
            value: "false"
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
        priorityClassName: ml-medium
        restartPolicy: Never
        runtimeClassName: nvidia
        schedulerName: default-scheduler
        securityContext: {}
        terminationGracePeriodSeconds: 30
        volumes:
        - emptyDir:
            medium: Memory
            sizeLimit: 2Gi
          name: dev-shm
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
            path: /srv/
            type: ""
          name: srv
        - hostPath:
            path: /mnt/sandbox/
            type: ""
          name: shared-storage
        - hostPath:
            path: /mnt/srv.remote/
            type: ""
          name: srv-remote
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
  priority: 100
  priorityClassName: ml-medium
  priorityClassSource: kueue.x-k8s.io/workloadpriorityclass
  queueName: lq-all-resources
```

This is happening for both plain Pods and Jobs. If I delete the top two waiting Workloads, the rest are admitted.

BTW this is how the ClusterQueue looks like (custom Grafana visualization):
![image](https://github.com/kubernetes-sigs/kueue/assets/43967691/245427d1-e0e8-49fe-a2bf-11f4120c4245)

**What you expected to happen**:
Workloads that fit into the quota gets admitted immediately.

**How to reproduce it (as minimally and precisely as possible)**:
Unfortunately, I wasn't able to reproduce it on out test cluster with the same configuration. It's not deterministic, as it doesn't happen everytime there are 3+ workloads in queue.

**Anything else we need to know?**:
It was also happening on versions v0.6.0/1/2/3.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.27.10+rke2r1
- Kueue version (use `git describe --tags --dirty --always`): v0.7.0
- Cloud provider or hardware configuration: onprem VMs
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.4 LTS
- Kernel (e.g. `uname -a`): 5.15.0-97-generic
- Install tools: ArgoCD
- Others:

## Discussion

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-10T14:57:13Z

Someone reported the same behavior in slack: https://kubernetes.slack.com/archives/C032ZE66A2X/p1716324774624269

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-11T09:11:01Z

Tagging @gabesaba 
![image](https://github.com/kubernetes-sigs/kueue/assets/43967691/268c30a7-322d-4a9d-b247-126afe15ce67)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-11T12:54:16Z

~~Since you're not seeing [this log line](https://github.com/kubernetes-sigs/kueue/blob/v0.7.0/pkg/controller/core/workload_controller.go#L431-L434), I suppose we are hitting [this branch](https://github.com/kubernetes-sigs/kueue/blob/v0.7.0/pkg/controller/core/workload_controller.go#L163-L170). I don't know how to reconcile that with your workloads having no status, however.. perhaps we are seeing an inconsistent state?~~ I noticed that your controller manager is configured with `controllerManager.replicas: 3`. Would it be possible for you to try running that with 1?

For reference, the controller-runtime code which is producing the logs above: https://github.com/kubernetes-sigs/controller-runtime/blob/v0.17.3/pkg/internal/controller/controller.go#L330-L338

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-11T13:09:16Z

may be a leader election issue. I found the 15 seconds you're seeing in log lines. Curious to see if the issue goes away with `replicas: 1`

https://github.com/kubernetes-sigs/kueue/blob/v0.7.0/apis/config/v1beta1/defaults.go#L38
https://github.com/kubernetes-sigs/kueue/blob/v0.7.0/pkg/controller/core/leader_aware_reconciler.go#L87

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-11T13:17:44Z

cc @astefanutti

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-11T14:04:18Z

I decreased replicas to 1, will let you know if my described problem appears again.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-11T14:36:54Z

Ok, so I scaled the replica to 1 and restarted the deployment. The workloads are still stuck in the queue with no status. However, the logs changed (no more reconciling after 15s) and then stopped (there are no more logs for this workload since the last time stamp which was ~31 minutes ago). Attaching `Explore-logs-2024-06-11 16_34_57.json`
[Explore-logs-2024-06-11 16_34_57.json](https://github.com/user-attachments/files/15789608/Explore-logs-2024-06-11.16_34_57.json)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-11T18:28:53Z

Did you filter out the logs?

I'm interested in seeing logs matching `"logger": "scheduler"` to understand if the scheduler is running at all or if it's stuck processing a particular job.

Additionally, the Workload reconciler should only have the need to reconcile a particular object repeatedly if it encountered any error while trying to reconcile. Did you see any stack trace or error from the controller?

There is another case where we use RequeueAfter for Workloads, but that's only if you use the waitForPodsReady feature, which I can see that you are not using.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-12T13:09:31Z

Yes, it's filtered for that particular workload. Here are logs matching `"logger": "scheduler"`, but it's only a minute time, since I'm hitting our Loki processing limit. Let me know if it's enough, or I will try to come up with bigger time frame
[Explore-logs-2024-06-12 15_08_34.json](https://github.com/user-attachments/files/15805576/Explore-logs-2024-06-12.15_08_34.json)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-12T16:18:39Z

From those logs, we can see that the scheduler is repeatedly trying to schedule a different Workload: `job-ml-job-face-recognition-t131-4gpu-newton-0a3c5`, which doesn't fit.

When requeueing, the scheduler should be putting this Workload back into the "inadmissible" set, and take the next Workload in the queue. But it doesn't look like it's doing that.

```
{\"level\":\"Level(-2)\",\"ts\":\"2024-06-11T12:04:39.01684286Z\",\"logger\":\"scheduler\",\"caller\":\"scheduler/scheduler.go:619\",\"msg\":\"Workload re-queued\",\"workload\":{\"name\":\"job-ml-job-face-recognition-t131-4gpu-newton-0a3c5\",\"namespace\":\"jstratil\"},\"clusterQueue\":{\"name\":\"cq-all-resources\"},\"qu
eue\":{\"name\":\"lq-all-resources\",\"namespace\":\"jstratil\"},\"requeueReason\":\"\",\"added\":true}
```

The `requeueReason` empty should be treated as immediate=false here (meaning not to retry this workload immediately):

https://github.com/kubernetes-sigs/kueue/blob/8c93b9c32d4c0b41870c75f8a8cb81adf9e2c40d/pkg/queue/cluster_queue.go#L401

Unless this condition is true:

https://github.com/kubernetes-sigs/kueue/blob/8c93b9c32d4c0b41870c75f8a8cb81adf9e2c40d/pkg/queue/cluster_queue.go#L226

In the log line for `Workload evaluated for admission`, I see the following values over three iterations:

```
"LastTriedFlavorIdx\":[{\"cpu\":2,\"ephemeral-storage\":2,\"memory\":2,\"nvidia.com/gpu\":2,\"pods\":2}]
"LastTriedFlavorIdx\":[{\"cpu\":2,\"ephemeral-storage\":2,\"memory\":2,\"nvidia.com/gpu\":2,\"pods\":2}]
{\"LastTriedFlavorIdx\":[{}]
```

at which point `wInfo.LastAssignment.PendingFlavors()` should evaluate to false, yet, it looks like it's requeueing immediately again.

Maybe we need to log a few more fields that could tell us what's causing the retry.


Importantly, you have 5 flavors, yet the `LastTriedFlavorIdx` doesn't quite go past 2. Although it looks like this Workload doesn't match some flavors' node labels.

@KunWuLuan  have you seen any problem like this before?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-12T16:56:39Z

@trasc can you have a look? At the very least, maybe see which log lines we can add to narrow down this problem.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-06-13T07:39:56Z

@alculquicondor I didn't see problems like this before. I will try to figure out what happened these days.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-06-13T08:12:26Z

I saw Mode is 1 for resources in log. This means the scheduler try to preempt for the workload in flavor "newton". But it can not find any workload to preempt.
```
  {
    "line": "{\"level\":\"Level(-2)\",\"ts\":\"2024-06-11T12:04:39.217532916Z\",\"logger\":\"scheduler\",\"caller\":\"scheduler/scheduler.go:263\",\"msg\":\"Workload requires preemption, but there are no candidate workloads allowed for preemption\",\"workload\":{\"name\":\"job-ml-job-face-recognition-t131-4gpu-newton-0a3c5\",\"namespace\":\"jstratil\"},\"clusterQueue\":{\"name\":\"cq-all-resources\"},\"preemption\":{\"reclaimWithinCohort\":\"Never\",\"borrowWithinCohort\":{\"policy\":\"Never\"},\"withinClusterQueue\":\"Never\"}}",
    "timestamp": "1718107479217620311",
    "fields": {
      "app": "kueue",
      "container": "manager",
      "filename": "/var/log/pods/kueue-system_kueue-controller-manager-748945c9c9-xtj4r_06a2a551-b935-4700-a00e-49797dab822d/manager/0.log",
      "instance": "kueue",
      "job": "kueue-system/kueue",
      "namespace": "kueue-system",
      "node_name": "k8s-prod-master1",
      "pod": "kueue-controller-manager-748945c9c9-xtj4r",
      "stream": "stderr"
    }
  },
```

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2024-06-13T08:34:17Z

So for the workload `job-ml-job-face-recognition-t131-4gpu-newton-0a3c5`. Every time when kueue try to admit it, kueue cannot find resource in "newton", which is the 3rd flavor in cluster queue, and try to preempt in newton.
The reason why lastFlavorIdx is always 2 is we only set the idx after the flavor pass the check for taints and nodeselector.
https://github.com/kubernetes-sigs/kueue/blob/8c93b9c32d4c0b41870c75f8a8cb81adf9e2c40d/pkg/scheduler/flavorassigner/flavorassigner.go#L406-L430

And this cause the requeue.
https://github.com/kubernetes-sigs/kueue/blob/8c93b9c32d4c0b41870c75f8a8cb81adf9e2c40d/pkg/workload/workload.go#L113-L126

@alculquicondor I think we have figured out what happened in this case. Maybe we should put `assignedFlavorIdx = idx` at the beginning of the function.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-13T09:49:11Z

Could you send me a dev image so I can try it after the PR is merged?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T12:25:15Z

Once the PR merges, there will be a staging image that you can try. For now, we are waiting for the author of the PR to add unit tests for this.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-19T08:34:22Z

@xmolitann `gcr.io/k8s-staging-kueue/kueue:v20240619-v0.8.0-devel-54-g81ad017a` is the first staging image containing the fix.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-19T15:17:46Z

Or `gcr.io/k8s-staging-kueue/kueue:v20240619-v0.7.0-8-gaa682c90`.

Please let us know how it goes.

### Comment by [@xmolitann](https://github.com/xmolitann) — 2024-06-20T10:37:12Z

> @xmolitann `gcr.io/k8s-staging-kueue/kueue:v20240619-v0.8.0-devel-54-g81ad017a` is the first staging image containing the fix.

Running on this image, so far it seems the problem is fixed (we had 10+ jobs in queue with proper status filled). I will let you know in a few days if it's 100% fixed.
