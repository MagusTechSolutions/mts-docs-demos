# 💻 Browser IDE: Generic image

Welcome to the copyable source browser for the [Generic image tutorial](../13-jenkins-generic-image.md). Expand a file to read or copy it. Each file also includes GitHub view and raw download links.

> [!NOTE]
> This page requires no JavaScript. If Outline removes HTML details elements, the file contents remain visible as ordinary Markdown code blocks.

## Explorer

```text
📁 generic-image
│   └── 📄 Dockerfile
│   └── 📄 Jenkinsfile
│   └── 📄 nginx.conf
│   └── 📄 pipeline.yml
│   ├── 📁 scripts
│   │   └── 📄 build.sh
```

[Browse the complete `generic-image` starter on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/generic-image) · [Download the repository as a ZIP](https://github.com/MagusTechSolutions/mts-docs-demos/archive/refs/heads/master.zip)

## Use the complete starter

1. Create a local folder named `generic-image`.
2. Expand and copy each file below, or download it from its raw link.
3. Save it at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

## Files

<details>
<summary><strong>📄 Dockerfile</strong></summary>

**Save as:** `Dockerfile` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/generic-image/Dockerfile) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/generic-image/Dockerfile)

```dockerfile
FROM nginx:1.27-alpine
COPY build/index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

</details>

<details>
<summary><strong>📄 Jenkinsfile</strong></summary>

**Save as:** `Jenkinsfile` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/generic-image/Jenkinsfile) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/generic-image/Jenkinsfile)

```groovy
library identifier: 'buildPipeline@master',
  retriever: modernSCM([
    $class: 'GitSCMSource',
    credentialsId: 'github-repo-token',
    remote: 'https://github.com/MagusTechSolutions/mts-jenkins-lib.git'
  ])

buildPipeline(configFile: 'pipeline.yml')
```

</details>

<details>
<summary><strong>📄 nginx.conf</strong></summary>

**Save as:** `nginx.conf` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/generic-image/nginx.conf) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/generic-image/nginx.conf)

```nginx
server {
  listen 80;
  server_name _;

  location / {
    root /usr/share/nginx/html;
    try_files $uri $uri/ /index.html;
  }

  location = /health {
    access_log off;
    add_header Content-Type application/json;
    return 200 '{"status":"ok"}';
  }
}
```

</details>

<details>
<summary><strong>📄 pipeline.yml</strong></summary>

**Save as:** `pipeline.yml` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/generic-image/pipeline.yml) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/generic-image/pipeline.yml)

```yaml
app: demo-image
stack: generic
project: demo

custom:
  pre_build_commands:
    - "echo \"Preparing demo-image\""
  build_commands:
    - "sh scripts/build.sh"
  post_build_commands:
    - "cat build/output.txt"

artifacts:
  - 'build/output.txt'
  - 'imageRef.properties'
  - 'pipeline.properties'
```

</details>

<details>
<summary><strong>📄 scripts/build.sh</strong></summary>

**Save as:** `scripts/build.sh` · [View on GitHub](https://github.com/MagusTechSolutions/mts-docs-demos/blob/master/examples/generic-image/scripts/build.sh) · [Download raw file](https://github.com/MagusTechSolutions/mts-docs-demos/raw/refs/heads/master/examples/generic-image/scripts/build.sh)

```bash
#!/bin/sh
set -eu

mkdir -p build
cat > build/index.html <<'EOF'
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>MTS generic image</title></head>
  <body><h1>📦 Hello from the MTS generic image</h1></body>
</html>
EOF
printf 'Generic build completed at %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > build/output.txt
```

</details>
