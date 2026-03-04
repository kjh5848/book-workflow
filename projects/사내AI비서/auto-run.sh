#!/bin/bash
# ============================================================
# 사내AI비서 — 자동 실행 (자고 일어나면 완성)
# 사용법: ./auto-run.sh  (그냥 실행하면 됨, 로그 자동 저장)
# ============================================================

set -e

# 프로젝트 루트로 이동
cd "$(dirname "$0")/../.."
PROJECT="projects/사내AI비서"
LOG="${PROJECT}/auto-run.log"

# 로그 자동 저장 (stdout + stderr → 화면 + 파일 동시 출력)
exec > >(tee -a "$LOG") 2>&1

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

run_claude() {
  local desc=$1
  local prompt=$2
  log "시작: $desc"
  claude -p "$prompt" \
    --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
  log "완료: $desc"
  echo ""
}

COMMON="projects/사내AI비서 프로젝트 작업 중이다. 모든 질문은 합리적으로 판단하여 자동으로 답변하고 진행하라. 저자에게 묻지 말고 스스로 결정하라. progress.json을 업데이트하라."

log "========================================"
log "사내AI비서 자동 워크플로우 시작"
log "========================================"

# STEP 5: 챕터 집필 (7개)
for i in 1 2 3 4 5 6 7; do
  run_claude "CH0${i} 집필" \
    "챕터 작성 ${i}. ${COMMON} planning/outline-v1.md의 Ch.${i} 내용을 참고하여 chapters/0${i}-*.md를 생성하라. 이야기 파트(코드 없음, 비유 중심) → 기술 파트(실행 결과 확인) 구조로 작성하라. 완료 후 progress.json의 해당 챕터 status를 done으로 업데이트하라."
done

# STEP 6: 프롤로그 + 로드맵
run_claude "STEP 6 프롤로그" \
  "프롤로그 생성. ${COMMON} 코드 없이 전체 개념을 이야기로 엮어라. book/front/prologue.md와 book/front/roadmap.md를 생성하라."

# STEP 7: 마무리
run_claude "STEP 7 마무리" \
  "마무리. ${COMMON} book/front/preface.md(서문), book/back/epilogue.md(에필로그), book/back/appendix.md(부록)를 생성하라. 최종 제목을 확정하고 progress.json을 업데이트하라."

log "========================================"
log "전체 워크플로우 완료!"
log "========================================"
