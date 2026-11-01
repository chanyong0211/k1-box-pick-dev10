#!/usr/bin/env bash
# dev12/docker/start.sh 에서 이름만 바꾸고 화면 설정을 뺐다(헤드리스 전용).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
CYCLOLAB_ROOT="${PROJECTS}/cyclo_lab"
docker compose --env-file "${CYCLOLAB_ROOT}/docker/.env.base" --project-name k1-pelvis-pick-dev10 \
    -f "${CYCLOLAB_ROOT}/docker/docker-compose.yaml" -f "${SCRIPT_DIR}/compose.override.yaml" up -d --no-build cyclo_lab
echo "[INFO] 접속: docker exec -it cyclo_lab-pelvis-pick-dev10 bash"
