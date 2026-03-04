#!/bin/bash
# ============================================================
# 사내AI비서 — 자동 워크플로우 실행 스크립트
# 사용법: ./run-workflow.sh [step번호]
#   ./run-workflow.sh        → 전체 실행 (STEP 2~7)
#   ./run-workflow.sh 2      → STEP 2만 실행
#   ./run-workflow.sh 5 3    → STEP 5 챕터 3만 실행
# ============================================================

set -e
cd "$(dirname "$0")"
PROJECT_ROOT="$(cd ../.. && pwd)"
PROJECT="사내AI비서"

COMMON="모든 질문은 합리적으로 판단하여 자동으로 답변하고 진행해주세요. 저자에게 묻지 말고 스스로 결정하세요."

run_step() {
  local step=$1
  local extra=$2
  echo ""
  echo "========================================"
  echo "  STEP $step 시작"
  echo "========================================"

  case $step in
    2)
      claude -p "코드 분석을 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      ;;
    3)
      claude -p "시나리오 설계를 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      ;;
    4)
      claude -p "뼈대 세우기를 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      ;;
    5)
      if [ -n "$extra" ]; then
        claude -p "챕터 작성 $extra 를 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      else
        # progress.json에서 챕터 수를 읽어서 전부 실행
        echo "전체 챕터 자동 집필..."
        local total=$(cat progress.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['steps']['step_5_chapters']['chapters']) if d['steps']['step_5_chapters']['chapters'] else 0)")
        if [ "$total" -eq 0 ]; then
          echo "outline.md에서 챕터 수를 확인하세요."
          exit 1
        fi
        for i in $(seq 1 $total); do
          run_step 5 $i
        done
      fi
      ;;
    6)
      claude -p "프롤로그 생성을 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      ;;
    7)
      claude -p "마무리를 진행해주세요. $COMMON" --allowedTools 'Read,Write,Edit,Glob,Grep,Bash,Agent'
      ;;
    *)
      echo "사용법: ./run-workflow.sh [2|3|4|5|6|7]"
      exit 1
      ;;
  esac

  echo "  STEP $step 완료"
  echo "========================================"
}

# 메인 실행
if [ -n "$1" ]; then
  run_step $1 $2
else
  echo "========================================"
  echo "  사내AI비서 — 전체 워크플로우 자동 실행"
  echo "========================================"
  for step in 2 3 4 5 6 7; do
    run_step $step
  done
  echo ""
  echo "전체 워크플로우 완료!"
fi
