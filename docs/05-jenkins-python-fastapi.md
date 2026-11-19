# 🐍 Jenkins demo: Python FastAPI

Build a production-shaped FastAPI image with a predictable test and container workflow.

Use [examples/python-fastapi](../examples/python-fastapi/) as the complete starter.

> **Open the starter in a browser IDE:** [FastAPI source browser](code-browser/python-fastapi.md). You can expand, copy, and save every file, including the tagged `Jenkinsfile`.

## 1. Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
uvicorn app.main:app --reload
```

On Windows PowerShell, activate with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. Review the MTS pipeline config

```yaml
app: demo-fastapi
stack: python311
project: demo
artifacts:
  - 'coverage.xml'
  - 'imageRef.properties'
  - 'pipeline.properties'
```

The Python pipeline expects:

- `requirements.txt`;
- a package that supports `pip install -e .`;
- pytest tests;
- a root Docker build context.

Its default test command produces:

```text
coverage.xml
```

## 3. Check the app

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## 4. Container check

```bash
docker build -t demo-fastapi:local .
docker run --rm -p 8000:8000 demo-fastapi:local
```

## 5. Add optional deployment

```yaml
spinnaker_app: demo-fastapi
environments:
  - name: develop
    deploy: true
    spinnaker:
      pipeline: deploy-dev
      parameters:
        namespace: demo
        appname: demo-fastapi
```

## Topic Q&A

### 1. Why include `pyproject.toml`?
The MTS Python pipeline performs `pip install -e .`, which requires package metadata.

### 2. Why pin dependencies?
Pinning makes local and Jenkins builds repeatable.

### 3. Which command starts FastAPI in the image?
`uvicorn app.main:app --host 0.0.0.0 --port 8000`.

### 4. Does pytest-cov produce evidence?
Yes. The pipeline creates `coverage.xml`, which can be archived or sent to SonarQube.

### 5. Can I use Python 3.10?
Set `stack: python310` and confirm that the corresponding Jenkins agent exists.

## MTS Labs Q&A

### 1. Which agent runs `stack: python311`?
The shared library routes it to `python311`.

### 2. What is the MTS image path?
`mts-release/demo/demo-fastapi` for master/release branches, otherwise `mts-sandbox/demo/demo-fastapi`.

### 3. Must I add a Docker push stage?
No. The Python shared-library pipeline builds and pushes the image.

### 4. Which health path should MKP probes use?
This starter exposes `/health` on port `8000`.

### 5. How is the digest delivered to deployment?
Jenkins writes `IMAGE_NAME` into `imageRef.properties` and `pipeline.properties`.

## Troubleshooting questions

### Why does editable installation fail?
Confirm `pyproject.toml` exists and the package directory is included.

### Why did pytest fail only in Jenkins?
Compare Python versions, dependencies, environment variables, and test files between local and agent environments.

### Why is coverage absent?
Verify pytest-cov ran and `coverage.xml` is included in `artifacts`.

### Why does the container exit immediately?
Inspect logs for import errors, check `app.main:app`, and ensure port 8000 matches the Service target port.

