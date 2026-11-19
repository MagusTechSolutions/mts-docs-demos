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

