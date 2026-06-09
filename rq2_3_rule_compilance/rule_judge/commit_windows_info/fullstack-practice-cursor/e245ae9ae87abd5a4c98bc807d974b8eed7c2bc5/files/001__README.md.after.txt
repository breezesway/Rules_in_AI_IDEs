# 이메일 인증이 포함된 풀스택 Todo 애플리케이션

Spring Boot 백엔드와 React 프론트엔드로 구축된 포괄적인 Todo 애플리케이션으로, 이메일 인증 시스템을 통한 안전한 인증 기능을 제공합니다.

## 🚀 주요 기능

### 핵심 기능
- **사용자 인증**: 안전한 회원가입 및 로그인 시스템
- **이메일 인증**: SMTP를 통한 6자리 인증 코드 전송
- **Todo 관리**: Todo 생성, 읽기, 수정, 삭제 및 완료 상태 토글
- **사용자 프로필**: 개인 정보 및 설정 관리
- **JWT 인증**: 리프레시 토큰을 사용한 무상태 인증

### 이메일 인증 시스템
- **6자리 코드**: 안전한 숫자 인증 코드
- **10분 만료**: 보안을 위한 자동 코드 만료
- **속도 제한**: 이메일 폭격 방지 (1분 쿨다운)
- **재전송 기능**: 사용자가 새 코드 요청 가능
- **전문적인 템플릿**: 아름다운 HTML 이메일 템플릿
- **계정 활성화**: 로그인 전 이메일 인증 필수

### 보안 기능
- **비밀번호 해싱**: BCrypt 암호화
- **입력 검증**: 포괄적인 서버 측 검증
- **CORS 설정**: 안전한 크로스 오리진 요청
- **역할 기반 접근**: 사용자 및 관리자 역할 관리
- **보호된 라우트**: 프론트엔드 라우트 보호

## 🛠️ 기술 스택

### 백엔드
- **프레임워크**: Spring Boot 3.x
- **언어**: Java 17+
- **데이터베이스**: H2 (인메모리)
- **보안**: JWT를 사용한 Spring Security
- **이메일**: Thymeleaf 템플릿을 사용한 Spring Boot Mail
- **빌드 도구**: Gradle

### 프론트엔드
- **프레임워크**: React 18+
- **언어**: JavaScript/JSX
- **HTTP 클라이언트**: 인터셉터가 포함된 Axios
- **라우팅**: React Router v6
- **상태 관리**: Context API
- **스타일링**: 반응형 디자인이 포함된 CSS 모듈

## 📋 사전 요구사항

이 애플리케이션을 실행하기 전에 다음이 필요합니다:

- **Java 17+** 설치 및 구성
- **Node.js 16+** 및 npm 설치
- **Gradle 7+** (또는 포함된 래퍼 사용)
- **이메일 계정** SMTP 구성용 (Gmail 권장)

## 🚀 설치 및 설정

### 1. 저장소 클론
```bash
git clone <repository-url>
cd fullstack-practice-cursor
```

### 2. 백엔드 설정

#### 백엔드 디렉토리로 이동
```bash
cd backend
```

#### 이메일 설정 구성
백엔드 디렉토리에 `.env` 파일을 생성하거나 환경 변수를 설정하세요:

```bash
# Gmail SMTP 구성
export EMAIL_USERNAME=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
export EMAIL_FROM=noreply@todoapp.com

# 또는 .env 파일 생성:
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=noreply@todoapp.com
```

#### Gmail 앱 비밀번호 설정
1. Gmail 계정에서 2단계 인증 활성화
2. 앱 비밀번호 생성:
   - Google 계정 설정으로 이동
   - 보안 → 2단계 인증 → 앱 비밀번호
   - "메일"용 비밀번호 생성
   - 이 비밀번호를 `EMAIL_PASSWORD`로 사용

#### 백엔드 빌드 및 실행
```bash
# Gradle 래퍼 사용
./gradlew build
./gradlew bootRun

# 또는 시스템 Gradle 사용
gradle build
gradle bootRun
```

백엔드는 `http://localhost:8080`에서 시작됩니다

### 3. 프론트엔드 설정

#### 프론트엔드 디렉토리로 이동
```bash
cd app
```

#### 의존성 설치
```bash
npm install
```

#### 개발 서버 시작
```bash
npm start
```

프론트엔드는 `http://localhost:3000`에서 시작됩니다

## 📧 이메일 구성

### SMTP 설정
애플리케이션은 Gmail SMTP용으로 사전 구성되어 있습니다:

```properties
spring.mail.host=smtp.gmail.com
spring.mail.port=587
spring.mail.username=${EMAIL_USERNAME}
spring.mail.password=${EMAIL_PASSWORD}
spring.mail.properties.mail.smtp.auth=true
spring.mail.properties.mail.smtp.starttls.enable=true
```

### 대체 이메일 제공업체
다른 제공업체를 위해 `application.properties`를 수정할 수 있습니다:

#### Outlook/Hotmail
```properties
spring.mail.host=smtp-mail.outlook.com
spring.mail.port=587
```

#### Yahoo
```properties
spring.mail.host=smtp.mail.yahoo.com
spring.mail.port=587
```

## 🔐 기본 관리자 계정

애플리케이션은 시작 시 기본 관리자 사용자를 생성합니다:

- **사용자명**: `admin`
- **비밀번호**: `Admin123!`
- **이메일**: `admin@example.com`
- **상태**: 이메일 인증 완료 및 활성화됨

## 📱 API 엔드포인트

### 인증
```
POST   /api/auth/register           - 사용자 회원가입
POST   /api/auth/verify-email       - 코드로 이메일 인증
POST   /api/auth/resend-verification - 인증 코드 재전송
POST   /api/auth/login              - 사용자 로그인
POST   /api/auth/logout             - 사용자 로그아웃
GET    /api/auth/me                 - 현재 사용자 정보 가져오기
```

### Todos (보호된 라우트)
```
GET    /api/todos          - 사용자의 todos 가져오기
GET    /api/todos/{id}     - 특정 todo 가져오기
POST   /api/todos          - 새 todo 생성
PUT    /api/todos/{id}     - todo 수정
DELETE /api/todos/{id}     - todo 삭제
PATCH  /api/todos/{id}/toggle - 완료 상태 토글
```

## 🔄 이메일 인증 흐름

### 1. 사용자 회원가입
1. 사용자가 회원가입 양식 작성
2. 시스템이 계정 생성 (비활성화됨)
3. 인증 코드 생성 및 전송
4. 사용자가 인증 페이지로 리디렉션

### 2. 이메일 인증
1. 사용자가 이메일로 6자리 코드 수신
2. 사용자가 인증 양식에 코드 입력
3. 시스템이 코드 및 만료 시간 검증
4. 계정 활성화 및 활성화
5. 환영 이메일 전송
6. 사용자가 로그인 페이지로 리디렉션

### 3. 로그인 접근
1. 사용자가 자격 증명으로 로그인
2. 시스템이 이메일 인증 상태 확인
3. 인증된 경우 JWT 토큰 생성
4. 보호된 라우트에 대한 사용자 접근 허용

## 🎨 이메일 템플릿

애플리케이션에는 세 가지 전문적인 이메일 템플릿이 포함되어 있습니다:

1. **인증 이메일**: 인증 코드가 포함된 환영 메시지
2. **환영 이메일**: 성공적인 인증 후 전송
3. **비밀번호 재설정**: 향후 비밀번호 재설정 기능용

모든 템플릿은 반응형이며 다음을 포함합니다:
- 전문적인 브랜딩
- 명확한 행동 유도 버튼
- 보안 공지 및 만료 경고
- 모바일 친화적 디자인

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

### 이메일 테스트
1. 테스트용 실제 이메일 계정 사용
2. 이메일이 도착하지 않으면 스팸 폴더 확인
3. SMTP 자격 증명이 올바른지 확인
4. 여러 요청을 보내서 속도 제한 테스트

## 🐛 문제 해결

### 일반적인 문제

#### 이메일 전송 안됨
- SMTP 자격 증명 확인
- Gmail 앱 비밀번호가 올바른지 확인
- Gmail에서 2FA가 활성화되어 있는지 확인
- 방화벽/네트워크 제한 확인

#### 인증 코드 문제
- 코드는 10분 후 만료
- 최대 5회 인증 시도
- 재전송 요청 간 1분 쿨다운
- 이메일 스팸 폴더 확인

#### 빌드 오류
- Java 17+가 설치되어 있는지 확인
- Gradle 버전 호환성 확인
- 모든 의존성이 해결되었는지 확인

#### 프론트엔드 문제
- 브라우저 캐시 및 localStorage 지우기
- JavaScript 오류를 위해 콘솔 확인
- 백엔드가 포트 8080에서 실행 중인지 확인

### 디버그 모드
`application.properties`에서 디버그 로깅 활성화:
```properties
logging.level.com.example.todoapp=DEBUG
logging.level.org.springframework.mail=DEBUG
```

## 🔒 보안 고려사항

- **인증 코드는 10분 후 만료**
- **속도 제한**으로 이메일 폭격 방지
- **최대 시도 횟수**로 무차별 대입 공격 제한
- **프로덕션에서는 HTTPS 필수**
- **민감한 데이터용 환경 변수**
- **모든 엔드포인트에서 입력 검증**

## 🚀 프로덕션 배포

### 환경 변수
프로덕션 값을 설정:
- `jwt.secret`: 강력하고 고유한 비밀 키
- `spring.mail.username`: 프로덕션 이메일 계정
- `spring.mail.password`: 프로덕션 앱 비밀번호
- 데이터베이스 연결 세부 정보

### 보안 헤더
프로덕션에서 보안 헤더 활성화:
- HTTPS 강제
- CORS 제한
- 속도 제한
- 입력 살균

## 📝 기여하기

1. 저장소 포크
2. 기능 브랜치 생성
3. 변경사항 작성
4. 새 기능에 대한 테스트 추가
5. 풀 리퀘스트 제출

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 라이선스가 부여됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.

## 🤝 지원

지원 및 질문:
- 저장소에 이슈 생성
- 문제 해결 섹션 확인
- API 문서 검토

## 🎯 로드맵

- [ ] 비밀번호 재설정 기능
- [ ] 2단계 인증
- [ ] 소셜 로그인 통합
- [ ] 모바일 앱 개발
- [ ] 고급 todo 기능 (카테고리, 우선순위)
- [ ] 팀 협업 기능
- [ ] API 속도 제한
- [ ] 포괄적인 테스트 커버리지

---

**즐거운 코딩 되세요! 🎉**
