# 코드 분석 절차

> STEP 2(코드 해부)에서 사용. 완성 코드를 의도 필터로 분석한다.

## 분석 순서

```
A1. 구조-스캐너  →  프로젝트 전체 구조 파악
       ↓
A2. 기능-추출기  →  사용자 관점 기능 목록
       ↓
A3. 기술스택-탐지기  →  사용 기술/프레임워크 식별
       ↓
A4. 의존성-매퍼  →  컴포넌트 간 의존 관계
```

## A1. 구조-스캐너

프로젝트의 디렉토리/파일 구조를 트리로 출력한다.

**출력 형식**:
```
src/
├── main/
│   ├── java/com/example/
│   │   ├── controller/
│   │   │   └── PostController.java    ← 글 CRUD API
│   │   ├── service/
│   │   │   └── PostService.java       ← 비즈니스 로직
│   │   └── repository/
│   │       └── PostRepository.java    ← DB 접근
│   └── resources/
│       └── application.yml            ← 설정
└── test/
```

**규칙**:
- 파일명 옆에 한 줄 설명 필수
- 설정 파일, 빌드 파일도 포함
- 테스트 코드는 별도 표시

## A2. 기능-추출기

코드에서 **사용자 관점**의 기능 목록을 추출한다.

**출력 형식**:
```
| 기능 | 관련 파일 | 설명 |
|------|----------|------|
| 글 작성 | PostController, PostService | POST /posts로 새 글 생성 |
| 글 목록 | PostController, PostService | GET /posts로 전체 글 조회 |
| 글 수정 | PostController, PostService | PUT /posts/{id}로 수정 |
| 로그인 | AuthController, AuthService | POST /login으로 인증 |
```

**규칙**:
- **사용자가 할 수 있는 행동** 기준 (내부 구현 아님)
- 관련 파일은 핵심 파일만 (설정 파일 제외)

## A3. 기술스택-탐지기

빌드 파일(pom.xml, build.gradle, package.json 등)과 코드에서 기술 스택을 탐지한다.

**출력 형식**:
```
| 기술 | 버전 | 용도 |
|------|------|------|
| Spring Boot | 3.2.0 | 웹 프레임워크 |
| Spring Data JPA | 3.2.0 | ORM / DB 접근 |
| H2 Database | - | 개발용 인메모리 DB |
| Thymeleaf | 3.1.0 | 서버 사이드 템플릿 |
```

**규칙**:
- 빌드 파일에서 명시적 의존성 추출
- 버전 정보가 없으면 `-` 표시
- 용도를 **독자가 이해할 수 있는 한 줄**로

## A4. 의존성-매퍼

코드 컴포넌트 간 의존 관계를 매핑한다.

**출력 형식**:
```
Controller → Service: "요청을 위임"
Service → Repository: "데이터 접근 위임"
Repository → Database: "SQL 실행"
Service → ExternalAPI: "외부 API 호출"
```

**규칙**:
- 화살표 방향 = 의존 방향 (A→B: A가 B를 사용)
- 의존 관계마다 한 줄 설명
- 순환 의존이 있으면 경고 표시

## A5. diff-생성기

두 버전 간 차이점을 요약한다. STEP 3(시나리오+버전)에서 주로 사용.

**출력 형식**:
```
## v0.1 → v0.2 변경 요약

### 신규
- PostService.java: 글 목록 조회 로직
- post-list.html: 글 목록 페이지

### 변경
- PostController.java: /posts GET 엔드포인트 추가 (기존: / 만 존재)

### 삭제
- (없음)

### 핵심 변경
글 목록을 DB에서 조회하여 화면에 보여주는 기능 추가.
```

**규칙**:
- 신규 / 변경 / 삭제 3가지로 분류
- 핵심 변경은 독자 관점에서 **한 줄 요약**

## 의도 필터

> seed.md의 의도가 모든 분석의 기준이다.

코드 분석 결과를 seed.md 의도에 따라 필터링:
- **의도 안 코드**: 상세 분석 (기능, 구조, 의존성)
- **의도 밖 코드**: 존재만 기록 ("있지만 이 책에서는 다루지 않음")
- **판단 불가**: 인사이트 질문으로 저자에게 확인
