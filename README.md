# book-workflow

기술 서적(100페이지 권장)을 이야기처럼 쓰는 워크플로우 시스템.

저자(도메인 전문가)와 하나의 AI(Claude)가 대화하며 책을 완성한다.

## 구조

```
.claude/skills/    ← 스킬 5개 카테고리 (writing, planning, code, visual, review)
workflow/          ← 7 STEP 실행 가이드
design/            ← 설계 문서
projects/          ← 프로젝트별 산출물
```

## 워크플로우 (7 STEP)

| Phase | STEP | 이름 | 산출물 |
|-------|------|------|--------|
| 의도 확립 | 1 | 씨앗 | seed.md |
| 재료 파악 | 2 | 코드 해부 | code-analysis.md |
| 이야기 설계 | 3 | 시나리오+버전 | scenario.md + versions/ |
| 이야기 설계 | 4 | 뼈대 세우기 | outline.md |
| 집필 | 5 | 챕터 집필 | chapters/NN-제목.md |
| 완성 | 6 | 프롤로그+로드맵 | prologue.md, roadmap.md |
| 완성 | 7 | 마무리 | preface.md, afterword.md, appendix.md |
