# 📝 풀스택 Todo 애플리케이션

Spring Boot (Java 17)와 React 19를 사용하여 구축된 현대적이고 반응형 Todo 애플리케이션입니다. 업계 모범 사례와 깔끔한 아키텍처 원칙을 따릅니다.

## 🚀 주요 기능

- **생성, 읽기, 수정, 삭제** - Todo 항목의 모든 CRUD 작업
- **완료 상태 토글** - 한 번의 클릭으로 완료/미완료 전환
- **실시간 유효성 검사** - 프론트엔드와 백엔드 모두에서
- **반응형 디자인** - 모든 기기에서 작동
- **현대적인 UI/UX** - 부드러운 애니메이션과 전환 효과
- **통계 대시보드** - 활성, 완료, 총 Todo 수 표시
- **포괄적인 오류 처리** - 사용자 친화적인 메시지
- **로딩 상태** 및 적절한 사용자 피드백

## 🛠️ 기술 스택

### 백엔드
- **Spring Boot 3.5.4** (Java 17 기반)
- **Spring Data JPA** - 데이터베이스 작업용
- **Spring Boot Validation** - 입력 유효성 검사용
- **H2 Database** - 개발용 인메모리 데이터베이스
- **Gradle** - 빌드 도구
- **Lombok** - 보일러플레이트 코드 감소용

### 프론트엔드
- **React 19.1.1** - 최신 훅 사용
- **Axios** - HTTP 클라이언트
- **CSS 모듈** - 컴포넌트 스타일링
- **반응형 디자인** - 모바일 우선 접근법

## 📁 프로젝트 구조

```
todo-prac/
├── backend/                 # Spring Boot 애플리케이션
│   ├── src/main/java/com/example/todoapp/
│   │   ├── controller/     # REST API 컨트롤러
│   │   ├── service/        # 비즈니스 로직 계층
│   │   ├── repository/     # 데이터 접근 계층
│   │   ├── entity/         # JPA 엔티티
│   │   ├── dto/           # 데이터 전송 객체
│   │   └── exception/     # 전역 예외 처리
│   └── src/main/resources/
│       └── application.properties
├── app/                    # React 프론트엔드
│   ├── src/
│   │   ├── components/    # React 컴포넌트
│   │   ├── services/      # API 서비스 계층
│   │   ├── hooks/         # 커스텀 React 훅
│   │   └── styles/        # 컴포넌트 스타일
│   └── package.json
└── README.md
```

## 🚀 시작하기

### 필수 요구사항
- **Java 17** 이상
- **Node.js 18** 이상
- **Gradle 7.6** 이상 (또는 포함된 Gradle 래퍼 사용)

### 백엔드 설정

1. **백엔드 디렉토리로 이동:**
   ```bash
   cd backend
   ```

2. **Spring Boot 애플리케이션 실행:**
   ```bash
   # Gradle 래퍼 사용
   ./gradlew bootRun
   
   # 또는 로컬 Gradle 설치 사용
   gradle bootRun
   ```

3. **백엔드 실행 확인:**
   - API: `http://localhost:8080`
   - H2 콘솔: `http://localhost:8080/h2-console`
   - 데이터베이스 URL: `jdbc:h2:mem:tododb`
   - 사용자명: `sa`
   - 비밀번호: `password`

### 프론트엔드 설정

1. **app 디렉토리로 이동:**
   ```bash
   cd app
   ```

2. **의존성 설치:**
   ```bash
   npm install
   ```

3. **개발 서버 시작:**
   ```bash
   npm start
   ```

4. **브라우저에서 열기:**
   - 프론트엔드: `http://localhost:3000`

## 📡 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|----------|-------------|
| `GET` | `/api/todos` | 모든 Todo 조회 |
| `GET` | `/api/todos/{id}` | 특정 Todo 조회 |
| `POST` | `/api/todos` | 새 Todo 생성 |
| `PUT` | `/api/todos/{id}` | Todo 수정 |
| `PATCH` | `/api/todos/{id}/toggle` | 완료 상태 토글 |
| `DELETE` | `/api/todos/{id}` | Todo 삭제 |

## 🎯 사용법

1. **새 Todo 추가:** 페이지 상단의 폼 사용
2. **Todo 편집:** Todo 항목의 편집 버튼(✎) 클릭
3. **완료 상태 토글:** 토글 버튼(○/✓) 클릭하여 완료/미완료 표시
4. **Todo 삭제:** 삭제 버튼(×) 클릭 후 확인
5. **통계 보기:** 상단에서 활성, 완료, 총 Todo 수 확인

## 🔧 개발

### 백엔드 개발
- **H2 인메모리 데이터베이스** 사용 (개발용)
- **H2 콘솔** 활성화로 데이터베이스 검사 가능
- **Bean Validation** 어노테이션을 사용한 유효성 검사
- **전역 예외 처리**로 일관된 오류 응답 제공

### 프론트엔드 개발
- **컴포넌트 기반 아키텍처**로 재사용 가능한 컴포넌트
- **커스텀 훅**으로 상태 관리 및 API 호출
- **반응형 CSS**로 현대적인 디자인 패턴
- **오류 경계** 및 로딩 상태로 더 나은 UX

## 🧪 테스트

### 백엔드 테스트
```bash
cd backend
./gradlew test
```

### 프론트엔드 테스트
```bash
cd app
npm test
```

## 🚀 프로덕션 배포

### 백엔드
- 프로덕션 데이터베이스로 설정 변경 (PostgreSQL, MySQL 등)
- `spring.jpa.hibernate.ddl-auto=validate` 또는 `none` 설정
- 적절한 로깅 레벨 구성
- 환경별 속성 설정

### 프론트엔드
```bash
cd app
npm run build
```
- `build` 폴더를 웹 서버에 배포
- `todoService.js`의 API 기본 URL을 프로덕션용으로 업데이트

## 📱 반응형 디자인

애플리케이션은 완전히 반응형이며 다음에서 작동합니다:
- **데스크톱** (1200px+)
- **태블릿** (768px - 1199px)
- **모바일** (320px - 767px)

## 🔒 보안 기능

- **입력 유효성 검사** - 프론트엔드와 백엔드 모두에서
- **SQL 인젝션 방지** - JPA를 통한 방지
- **XSS 방지** - 적절한 콘텐츠 이스케이핑
- **CORS 구성** - API 접근용

## 🎨 UI/UX 기능

- **현대적인 그라디언트 배경**
- **부드러운 호버 애니메이션**
- **로딩 스피너** 및 진행 표시기
- **토스트 알림** - 사용자 피드백용
- **깔끔하고 미니멀한 디자인**
- **접근 가능한 색상 구성**

## 🤝 기여하기

1. 저장소 포크
2. 기능 브랜치 생성
3. 변경사항 작성
4. 적용 가능한 경우 테스트 추가
5. 풀 리퀘스트 제출

## 📄 라이선스

이 프로젝트는 오픈 소스이며 [MIT 라이선스](LICENSE) 하에 제공됩니다.

## 🆘 지원

문제가 발생한 경우:
1. 콘솔에서 오류 메시지 확인
2. 백엔드와 프론트엔드가 모두 실행 중인지 확인
3. H2 콘솔에서 데이터베이스 문제 확인
4. 애플리케이션 로그 검토

---

**즐거운 코딩 되세요! 🎉**
