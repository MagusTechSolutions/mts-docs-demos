# 💻 Browser IDE: Spinnaker and Kubernetes

Welcome to the copyable source browser for the [Spinnaker and Kubernetes tutorial](../11-spinnaker-kubernetes.md). Expand a file to read or copy it. Each file also includes GitHub view and raw download links.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 spinnaker
│   ├── 📁 demo-app
│   │   ├── 📁 base
│   │   │   └── 📄 deployment.yml
│   │   │   └── 📄 kustomization.yml
│   │   │   └── 📄 service.yml
│   │   ├── 📁 overlays
│   │   │   ├── 📁 dev
│   │   │   │   └── 📄 kustomization.yml
│   └── 📄 pipeline.json
│   └── 📄 README.md
```

[Browse the complete `spinnaker` starter on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/spinnaker) · [Download the repository as a ZIP](https://github.com/MagusTechSolutions/mts-docs-demos/archive/refs/heads/master.zip)

## Use the complete starter

1. Create a local folder named `spinnaker`.
2. Expand and copy each file below, or download it from its raw link.
3. Save it at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

## Files

<details>
<summary><strong>📄 demo-app/base/deployment.yml</strong></summary>

**Save as:** `demo-app/base/deployment.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/demo-app/base/deployment.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/demo-app/base/deployment.yml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${appname}
  labels:
    app: ${appname}
    project: demo
  annotations:
    strategy.spinnaker.io/versioned: "true"
    strategy.spinnaker.io/max-version-history: "2"
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${appname}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels:
        app: ${appname}
        project: demo
    spec:
      containers:
        - name: ${appname}
          image: app-image
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 250m
              memory: 256Mi
```

</details>

<details>
<summary><strong>📄 demo-app/base/kustomization.yml</strong></summary>

**Save as:** `demo-app/base/kustomization.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/demo-app/base/kustomization.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/demo-app/base/kustomization.yml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yml
  - service.yml
```

</details>

<details>
<summary><strong>📄 demo-app/base/service.yml</strong></summary>

**Save as:** `demo-app/base/service.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/demo-app/base/service.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/demo-app/base/service.yml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${appname}
  labels:
    app: ${appname}
    project: demo
spec:
  type: ClusterIP
  selector:
    app: ${appname}
  ports:
    - name: http
      port: 80
      targetPort: http
```

</details>

<details>
<summary><strong>📄 demo-app/overlays/dev/kustomization.yml</strong></summary>

**Save as:** `demo-app/overlays/dev/kustomization.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/demo-app/overlays/dev/kustomization.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/demo-app/overlays/dev/kustomization.yml)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: ${namespace}
commonLabels:
  project: demo
resources:
  - ../../base
images:
  - name: app-image
    newName: ${image}
```

</details>

<details>
<summary><strong>📄 pipeline.json</strong></summary>

**Save as:** `pipeline.json` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/pipeline.json) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/pipeline.json)

```json
{
  "application": "demo",
  "name": "Deploy demo application",
  "description": "Bake and deploy the demo application with Kustomize.",
  "keepWaitingPipelines": false,
  "limitConcurrent": true,
  "spelEvaluator": "v4",
  "parameterConfig": [
    {
      "name": "namespace",
      "label": "Kubernetes namespace",
      "description": "Namespace receiving the demo application.",
      "default": "demo",
      "required": true
    },
    {
      "name": "appname",
      "label": "Application name",
      "description": "Name inserted into deployment manifests.",
      "default": "demo-node",
      "required": true
    },
    {
      "name": "image",
      "label": "Immutable image reference",
      "description": "Digest-pinned image supplied by Jenkins.",
      "default": "",
      "required": true
    }
  ],
  "stages": [
    {
      "name": "Bake demo manifests",
      "type": "bakeManifest",
      "refId": "bake",
      "requisiteStageRefIds": [],
      "templateRenderer": "KUSTOMIZE4",
      "kustomizeFilePath": "demo-app/overlays/dev/kustomization.yml",
      "outputName": "demo-baked-manifests",
      "namespace": "${parameters.namespace}",
      "evaluateOverrideExpressions": true,
      "inputArtifact": {
        "account": "REPLACE_WITH_GIT_ARTIFACT_ACCOUNT",
        "id": null,
        "artifact": {
          "artifactAccount": "REPLACE_WITH_GIT_ARTIFACT_ACCOUNT",
          "name": "mts-labs-deployment-configs",
          "reference": "REPLACE_WITH_DEPLOYMENT_REPOSITORY_URL",
          "type": "git/repo",
          "version": "main"
        }
      },
      "expectedArtifacts": [
        {
          "defaultArtifact": {
            "customKind": false,
            "id": "REPLACE_WITH_EXPECTED_ARTIFACT_ID",
            "name": "demo-baked-manifests",
            "type": "embedded/base64"
          },
          "displayName": "Demo baked manifests",
          "id": "REPLACE_WITH_EXPECTED_ARTIFACT_ID",
          "matchArtifact": {
            "id": "REPLACE_WITH_EXPECTED_ARTIFACT_ID",
            "name": "demo-baked-manifests",
            "type": "embedded/base64"
          },
          "useDefaultArtifact": false,
          "usePriorArtifact": false
        }
      ]
    },
    {
      "name": "Deploy demo manifests",
      "type": "deployManifest",
      "refId": "deploy",
      "requisiteStageRefIds": [
        "bake"
      ],
      "cloudProvider": "kubernetes",
      "account": "REPLACE_WITH_KUBERNETES_ACCOUNT",
      "source": "artifact",
      "manifestArtifactId": "REPLACE_WITH_EXPECTED_ARTIFACT_ID",
      "manifestArtifactAccount": "embedded-artifact",
      "requiredArtifactIds": [],
      "requiredArtifacts": [],
      "skipExpressionEvaluation": false
    }
  ],
  "triggers": [],
  "notifications": [],
  "parallel": false
}
```

</details>

<details>
<summary><strong>📄 README.md</strong></summary>

**Save as:** `README.md` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/spinnaker/README.md) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/spinnaker/README.md)

```markdown
# Spinnaker Kubernetes starter

This template follows the MTS Kustomize and `bakeManifest` to `deployManifest` pattern.

Replace:

- `REPLACE_WITH_GIT_ARTIFACT_ACCOUNT`
- `REPLACE_WITH_KUBERNETES_ACCOUNT`
- the deployment repository URL and version in `pipeline.json`

Jenkins should provide `image`, `namespace`, and `appname` as pipeline parameters. The deployment base uses `app-image`; the dev overlay replaces it with `${image}`.

Import `pipeline.json` through the Spinnaker pipeline configuration workflow supported by your MTS environment, then generate a fresh expected-artifact ID through Spinnaker rather than reusing the placeholder.
```

</details>
