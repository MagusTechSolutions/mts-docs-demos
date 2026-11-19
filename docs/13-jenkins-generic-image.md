# 📦 Jenkins demo: generic image

Use the generic pipeline when the build is not Java, Node, Python, or Helm—but you can still produce a Docker image from the repository root.

The full starter is in [examples/generic-image](https://github.com/MagusTechSolutions/mts-docs-demos/tree/master/examples/generic-image).

> **Open the starter in a browser IDE:** [Generic image source browser](code-browser/generic-image.md). You can expand, copy, and save every file.

## 1. Review the custom build

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

The commands run on `agent any`; your Jenkins administrator must ensure it has every required build tool and Docker access.

## 2. Build locally

```bash
sh scripts/build.sh
docker build -t demo-image:local .
docker run --rm -p 8080:80 demo-image:local
```

## 3. When to use generic

Good examples:

- a compiled Go, Rust, or C++ service;
- an image assembled by Make;
- a static frontend with a custom generator;
- a wrapper around an external build tool.

Prefer a supported language pipeline when it provides meaningful test and security stages.

## 4. Keep a root Dockerfile

The generic pipeline runs:

```groovy
docker.build(imageTag, "./")
```

That means the Dockerfile and its COPY inputs must be reachable from the repository root.

## Topic Q&A

### 1. When should I use the generic pipeline?
Use it when no supported stack pipeline matches but the repository can build a Docker context.

### 2. Does it run tests automatically?
No. Put validation in `custom.build_commands` and make failures return non-zero.

### 3. Where can build output be created?
Any path used by the root Dockerfile and, when desired, archived as an artifact.

### 4. What if I need special compilers?
Build them in Docker or select an agent installed with the required toolchain.

### 5. Can I build without deploying?
Yes. Omit `spinnaker` and `spinnaker_app`.

## MTS Labs Q&A

### 1. Which agent executes a generic build?
`agent any`; availability of the needed tool is therefore your responsibility.

### 2. Which image context does Jenkins use?
The repository root, `./`.

### 3. How do I retain evidence?
List files from `build/` and the generated image-reference properties under `artifacts`.

### 4. Does the generic route use the same registry policy?
Yes. It uses the same sandbox/release path, push/fallback behavior, and digest output.

### 5. How does this reach Spinnaker?
Add `spinnaker_app` and branch mappings only after the MTS Spinnaker application/pipeline exists.

## Troubleshooting questions

### Why did Docker report a missing COPY source?
Run the custom build first and confirm every referenced file is below the repository root.

### Why did a failed script not stop Jenkins?
Use `set -eu` in shell scripts and return a non-zero exit code for validation failures.

### Why is the agent missing a compiler?
The generic route uses any available agent; use a purpose-built agent or Docker build stage.

### Why is `build/output.txt` not archived?
Confirm the custom script created it before the Store Artifacts stage.

