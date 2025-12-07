# create ci_audit.sh with the following content and run it:
cat > ci_audit.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "=== 1) Repo root and top-level files ==="
ls -la

echo
echo "=== 2) File tree (top 4 levels) ==="
find . -maxdepth 4 -type f -print | sed -e 's/^\.\///' | sed -n '1,500p'

echo
echo "=== 3) Important files content (if present) ==="
for f in Dockerfile cloudbuild.yaml cloudbuild.yml package.json requirements.txt Pipfile pyproject.toml .github/workflows/*; do
  if [ -f "$f" ]; then
    echo
    echo "---- $f ----"
    sed -n '1,400p' "$f"
  fi
done

echo
echo "=== 4) Show .github/workflows files list ==="
if [ -d ".github/workflows" ]; then ls -la .github/workflows || true; fi

echo
echo "=== 5) Try tests (Python/Node) ==="
if [ -f requirements.txt ] || [ -f Pipfile ] || [ -f pyproject.toml ]; then
  echo "-- Python detected. Running pytest if installed --"
  if command -v pytest >/dev/null 2>&1; then pytest -q || true; else echo "pytest not installed locally."; fi
fi
if [ -f package.json ]; then
  echo "-- Node detected. Checking npm test --"
  if command -v npm >/dev/null 2>&1; then
    if grep -q "\"test\"" package.json; then npm test || true; else echo "No test script in package.json"; fi
  else
    echo "npm not installed locally."
  fi
fi

echo
echo "=== 6) Attempt docker build (if Dockerfile exists) ==="
if [ -f Dockerfile ]; then
  if command -v docker >/dev/null 2>&1; then docker build -t ci-audit-image:latest . || true; else echo "docker not installed."; fi
fi

echo "=== AUDIT COMPLETE ==="
EOF

chmod +x ci_audit.sh
./ci_audit.sh 2>&1 | tee ci_audit.log
