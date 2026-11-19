# 💻 Browser IDE: Generic image

Welcome to the copyable source browser for the [Generic image tutorial](../06-jenkins-generic-image.md). Expand a file to read it. Select the code block's copy action, then save it using the displayed path.

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

## Save the complete starter

1. Create a local folder named `generic-image`.
2. Expand each file below.
3. Copy its code block into a file at the exact displayed path.
4. Commit the copied folder as the root of a new application repository.

A separate whole-folder ZIP/download link can be added later without changing any of the source shown on this page.

## Files

<details>
<summary><strong>📄 Dockerfile</strong></summary>

**Save as:** `Dockerfile`

```dockerfile
FROM nginx:1.27-alpine
COPY build/index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

</details>

<details>
<summary><strong>📄 Jenkinsfile</strong></summary>

**Save as:** `Jenkinsfile`

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

**Save as:** `nginx.conf`

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

**Save as:** `pipeline.yml`

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

**Save as:** `scripts/build.sh`

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
