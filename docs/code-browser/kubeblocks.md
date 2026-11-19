# 💻 Browser IDE: KubeBlocks data services

Welcome to the copyable source browser for the [KubeBlocks data services tutorial](../09-kubeblocks-databases.md). Expand a file to read it. Select the code block's copy action, then save it using the displayed path.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 kubeblocks
│   └── 📄 minio-bucket-job.yml
│   └── 📄 minio-cluster.yml
│   └── 📄 minio-service.yml
│   └── 📄 postgres-cluster.yml
│   └── 📄 postgres-service.yml
│   └── 📄 README.md
│   └── 📄 redis-cluster.yml
│   └── 📄 redis-service.yml
```

## Save the complete starter

1. Create a local folder named `kubeblocks`.
2. Expand each file below.
3. Copy its code block into a file at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

A separate whole-folder ZIP/download link can be added later without changing any of the source shown on this page.

## Files

<details>
<summary><strong>📄 minio-bucket-job.yml</strong></summary>

**Save as:** `minio-bucket-job.yml`

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: demo-minio-buckets
  namespace: demo
spec:
  backoffLimit: 10
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: init
          image: public.ecr.aws/aws-cli/aws-cli:latest
          env:
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: demo-minio-minio-account-root
                  key: username
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: demo-minio-minio-account-root
                  key: password
            - name: AWS_DEFAULT_REGION
              value: us-east-1
          command: ["/bin/sh", "-c"]
          args:
            - |
              set -eu
              cat > /tmp/aws-config <<'EOF'
              [default]
              s3 =
                  addressing_style = path
              EOF
              export AWS_CONFIG_FILE=/tmp/aws-config
              endpoint=http://demo-minio:9000
              until aws --endpoint-url "$endpoint" s3api list-buckets >/dev/null; do
                sleep 5
              done
              for bucket in demo-uploads demo-assets demo-backups; do
                aws --endpoint-url "$endpoint" s3api head-bucket --bucket "$bucket" \
                  2>/dev/null || \
                aws --endpoint-url "$endpoint" s3api create-bucket --bucket "$bucket"
              done
```

</details>

<details>
<summary><strong>📄 minio-cluster.yml</strong></summary>

**Save as:** `minio-cluster.yml`

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: demo-minio
  namespace: demo
spec:
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: minio
      componentDef: minio
      replicas: 2
      resources:
        requests:
          cpu: 100m
          memory: 256Mi
        limits:
          cpu: 500m
          memory: 512Mi
      volumeClaimTemplates:
        - name: data
          spec:
            storageClassName: truenas-nfs
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 15Gi
```

</details>

<details>
<summary><strong>📄 minio-service.yml</strong></summary>

**Save as:** `minio-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-minio
  namespace: demo
spec:
  type: NodePort
  selector:
    app.kubernetes.io/instance: demo-minio
    apps.kubeblocks.io/component-name: minio
  ports:
    - name: s3-api
      port: 9000
      targetPort: 9000
```

</details>

<details>
<summary><strong>📄 postgres-cluster.yml</strong></summary>

**Save as:** `postgres-cluster.yml`

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: demo-db
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: postgresql
      componentDef: postgresql
      replicas: 1
      resources:
        requests:
          cpu: 100m
          memory: 512Mi
        limits:
          cpu: 500m
          memory: 1Gi
      volumeClaimTemplates:
        - name: data
          spec:
            storageClassName: truenas-nfs
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 5Gi
```

</details>

<details>
<summary><strong>📄 postgres-service.yml</strong></summary>

**Save as:** `postgres-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-db
  namespace: demo
spec:
  type: NodePort
  selector:
    app.kubernetes.io/instance: demo-db
    apps.kubeblocks.io/component-name: postgresql
    kubeblocks.io/role: primary
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
```

</details>

<details>
<summary><strong>📄 README.md</strong></summary>

**Save as:** `README.md`

```markdown
# KubeBlocks demo manifests

These manifests use the shared MTS KubeBlocks StorageClass:

```text
truenas-nfs
```

For external MTS clients, use `mts-db.magus.lab` rather than hard-coding its current address (`192.168.1.241`). PostgreSQL, Redis, and MinIO have separate NodePorts; read each port from its Service before connecting.

Apply only after confirming the KubeBlocks `Cluster`, PostgreSQL, Redis, and MinIO component definitions installed in the cluster.

```bash
kubectl -n demo apply -f postgres-cluster.yml
kubectl -n demo apply -f postgres-service.yml
kubectl -n demo apply -f redis-cluster.yml
kubectl -n demo apply -f redis-service.yml
kubectl -n demo apply -f minio-cluster.yml
kubectl -n demo apply -f minio-service.yml
kubectl -n demo apply -f minio-bucket-job.yml
```
```

</details>

<details>
<summary><strong>📄 redis-cluster.yml</strong></summary>

**Save as:** `redis-cluster.yml`

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: demo-redis
  namespace: demo
spec:
  clusterDef: redis
  topology: standalone
  terminationPolicy: DoNotTerminate
  componentSpecs:
    - name: redis
      componentDef: redis
      replicas: 1
      resources:
        requests:
          cpu: 25m
          memory: 128Mi
        limits:
          cpu: 100m
          memory: 256Mi
      volumeClaimTemplates:
        - name: data
          spec:
            storageClassName: truenas-nfs
            accessModes:
              - ReadWriteOnce
            resources:
              requests:
                storage: 1Gi
```

</details>

<details>
<summary><strong>📄 redis-service.yml</strong></summary>

**Save as:** `redis-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-redis
  namespace: demo
spec:
  type: NodePort
  selector:
    app.kubernetes.io/instance: demo-redis
    apps.kubeblocks.io/component-name: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
```

</details>
