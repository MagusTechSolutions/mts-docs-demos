# 💻 Browser IDE: NGINX static site

Welcome to the copyable source browser for the [NGINX static site tutorial](../17-nginx-static-site.md). Expand a file to read or copy it. Each file also includes GitHub view and raw download links.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 nginx
│   └── 📄 configmap.yml
│   └── 📄 deployment.yml
│   └── 📄 service.yml
```

[Browse the complete `nginx` starter on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/nginx) · [Download the repository as a ZIP](https://github.com/MagusTechSolutions/mts-docs-demos/archive/refs/heads/master.zip)

## Use the complete starter

1. Create a local folder named `nginx`.
2. Expand and copy each file below, or download it from its raw link.
3. Save it at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

## Files

<details>
<summary><strong>📄 configmap.yml</strong></summary>

**Save as:** `configmap.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/nginx/configmap.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/nginx/configmap.yml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo-nginx-content
  namespace: demo
data:
  index.html: |
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Hello from MTS Labs</title>
        <style>
          body { font: 18px system-ui, sans-serif; max-width: 720px; margin: 10vh auto; padding: 2rem; color: #1f2937; }
          h1 { color: #2563eb; }
        </style>
      </head>
      <body>
        <h1>🚀 Hello from MKP!</h1>
        <p>Your NGINX Deployment, Service, and ConfigMap are working.</p>
      </body>
    </html>
```

</details>

<details>
<summary><strong>📄 deployment.yml</strong></summary>

**Save as:** `deployment.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/nginx/deployment.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/nginx/deployment.yml)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-nginx
  namespace: demo
  labels:
    app: demo-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo-nginx
  template:
    metadata:
      labels:
        app: demo-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27-alpine
          ports:
            - name: http
              containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          resources:
            requests:
              cpu: 25m
              memory: 32Mi
            limits:
              cpu: 100m
              memory: 64Mi
          volumeMounts:
            - name: content
              mountPath: /usr/share/nginx/html/index.html
              subPath: index.html
              readOnly: true
      volumes:
        - name: content
          configMap:
            name: demo-nginx-content
```

</details>

<details>
<summary><strong>📄 service.yml</strong></summary>

**Save as:** `service.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/nginx/service.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/nginx/service.yml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-nginx
  namespace: demo
spec:
  type: ClusterIP
  selector:
    app: demo-nginx
  ports:
    - name: http
      port: 80
      targetPort: http
```

</details>
