# Dodge Game — JavaScript + Phaser

Windows와 Visual Studio Code 환경에서 JavaScript와 Phaser를 사용해 만든 2D 장애물 피하기 게임입니다.

Lua + LÖVE2D로 제작했던 게임과 동일한 규칙을 JavaScript + Phaser로 다시 구현해 개발 환경, 코드 구조, 실행 방법, 장점과 단점을 비교하는 것이 목표입니다.

## 프로젝트 개요

- 플레이어를 좌우 방향키로 움직입니다.
- 화면 위에서 떨어지는 장애물을 피합니다.
- 장애물을 피할 때마다 점수가 1점 증가합니다.
- 점수가 5점 증가할 때마다 난이도와 장애물 속도가 올라갑니다.
- 장애물과 충돌하면 게임이 종료됩니다.
- 최고 난이도는 7단계입니다.

## 개발 환경

| 항목 | 사용 환경 |
|---|---|
| 운영체제 | Windows |
| 코드 편집기 | Visual Studio Code |
| 언어 | HTML, CSS, JavaScript |
| 게임 프레임워크 | Phaser 4.2.1 |
| Phaser 불러오기 | jsDelivr CDN |
| 로컬 웹 서버 | Python `http.server` |
| 게임 화면 | 480 × 360 |

## 실행 방식 변경 기록

처음에는 Node.js, npm, Vite를 이용해 개발 서버를 실행하려고 했습니다. 그러나 현재 Windows 환경에서 Vite와 esbuild의 네이티브 실행 파일이 다음 접근 위반 코드로 종료됐습니다.

```text
-1073741819
3221225477
0xC0000005
```

HTML, CSS, JavaScript 파일을 검사한 결과 별도의 누락도 발견해 수정했습니다.

- `index.html`: viewport 설정의 `<meta` 누락 수정
- `style.css`: `body`를 닫는 `}` 누락 수정
- `main.js`: 확인된 문법 문제 없음

이후 Vite 대신 Phaser 4.2.1을 CDN으로 불러오고 Python 기본 웹 서버로 실행하도록 변경했습니다. 변경 후 게임이 정상적으로 작동하는 것을 확인했습니다.

## 구현 기능

- 시작 화면
- `Enter` 또는 `Space`로 게임 시작
- 방향키 좌우 이동
- 플레이어의 화면 밖 이동 방지
- 무작위 가로 위치에서 생성되는 낙하 장애물
- 장애물을 피할 때 점수 증가
- 사각형 충돌 판정
- 게임 종료 화면
- 최종 점수와 도달 단계 표시
- `R` 키로 다시 시작
- `P` 키로 일시정지 및 계속하기
- `Esc` 키로 시작 화면 복귀
- 점수에 따른 7단계 난이도
- 단계에 따른 장애물 속도 증가

## 조작 방법

| 키 | 기능 |
|---|---|
| `Enter` 또는 `Space` | 시작 화면에서 게임 시작 |
| `←` | 왼쪽 이동 |
| `→` | 오른쪽 이동 |
| `P` | 일시정지 또는 계속하기 |
| `R` | 게임 종료 화면에서 다시 시작 |
| `Esc` | 시작 화면으로 돌아가기 |

웹 브라우저에서는 JavaScript가 사용자의 탭이나 창을 마음대로 닫는 것이 제한됩니다. 따라서 LÖVE2D판의 `Esc = 게임 종료` 대신 Phaser판에서는 `Esc = 시작 화면으로 돌아가기`로 구현했습니다.

## 난이도

| 점수 | 단계 | 장애물 속도 |
|---:|---:|---:|
| 0 ~ 4 | 1 | 160 |
| 5 ~ 9 | 2 | 195 |
| 10 ~ 14 | 3 | 230 |
| 15 ~ 19 | 4 | 265 |
| 20 ~ 24 | 5 | 300 |
| 25 ~ 29 | 6 | 335 |
| 30 이상 | 7 | 370 |

난이도는 다음 계산을 사용합니다.

```javascript
const calculatedLevel = Math.floor(score / 5) + 1;
const level = Math.min(calculatedLevel, 7);
```

최고 단계가 7로 제한되므로 점수가 30점을 넘어도 장애물 속도는 370을 유지합니다.

## 프로젝트 구조

```text
dodge_game
├── src
│   └── main.js
├── .gitignore
├── index.html
├── README.md
└── style.css
```

### `index.html`

- 게임 페이지의 기본 구조를 만듭니다.
- Phaser 4.2.1을 CDN에서 불러옵니다.
- `style.css`와 `src/main.js`를 연결합니다.

### `style.css`

- 페이지와 게임 화면을 가운데 배치합니다.
- 배경색과 글자색을 지정합니다.
- 480 × 360 게임 화면의 테두리를 표시합니다.

### `src/main.js`

- Phaser 게임과 장면을 생성합니다.
- 플레이어와 장애물을 만듭니다.
- 키보드 입력, 이동, 점수, 난이도, 충돌을 처리합니다.
- 시작·진행·일시정지·게임 종료 상태를 관리합니다.

## 로컬 실행 방법

### 1. 프로젝트 폴더로 이동

```powershell
Set-Location "C:\Users\boss3\OneDrive\바탕 화면\GitHub\TIL_Today-Learn\260820_Phaser_projects\dodge_game"
```

### 2. Python 웹 서버 실행

```powershell
python -m http.server 8000
```

### 3. 브라우저 접속

```text
http://localhost:8000/
```

코드를 수정한 뒤 브라우저에서 `Ctrl + F5`를 누르면 캐시를 무시하고 새로고침할 수 있습니다.

### 4. 서버 종료

PowerShell에서 다음 키를 누릅니다.

```text
Ctrl + C
```

## 인터넷 연결 조건

현재 프로젝트는 다음 주소에서 Phaser를 불러옵니다.

```html
<script src="https://cdn.jsdelivr.net/npm/phaser@4.2.1/dist/phaser.js"></script>
```

따라서 처음 게임을 불러올 때 인터넷 연결이 필요합니다. CDN 연결에 실패하면 브라우저 콘솔에 다음과 같은 오류가 나타날 수 있습니다.

```text
Phaser is not defined
Failed to load resource
```

## 브라우저 개발자 도구 검사

1. 게임 페이지에서 `F12`를 누릅니다.
2. `Console`을 선택합니다.
3. 페이지를 새로고침합니다.
4. 빨간색 오류가 없는지 확인합니다.

Python 서버 기록에서 다음 요청이 HTTP 200으로 처리되면 프로젝트 파일을 정상적으로 제공한 것입니다.

```text
GET / HTTP/1.1 200
GET /style.css HTTP/1.1 200
GET /src/main.js HTTP/1.1 200
```

다음 오류는 브라우저 탭 아이콘 파일이 없다는 뜻이며 게임 실행에는 영향을 주지 않습니다.

```text
GET /favicon.ico HTTP/1.1 404
```

## Git에서 제외하는 파일

`.gitignore`에는 다음 내용을 사용합니다.

```gitignore
node_modules/
dist/
.vite/
*.log
.env
.env.*
!.env.example
```

최종 프로젝트는 CDN 방식이므로 `node_modules`, `package.json`, `package-lock.json`을 사용하지 않습니다.

## GitHub Pages 배포 참고

이 프로젝트는 정적 HTML, CSS, JavaScript로 구성되어 GitHub Pages에서 게시할 수 있습니다.

현재 프로젝트가 `TIL_Today-Learn` 저장소의 하위 폴더에 있으므로 예상 주소 형식은 다음과 같습니다.

```text
https://projectCHOI.github.io/TIL_Today-Learn/260820_Phaser_projects/dodge_game/
```

실제 주소는 GitHub Pages가 어떤 브랜치와 폴더를 게시하도록 설정됐는지에 따라 달라질 수 있습니다.

## JavaScript + Phaser에서 확인한 장점

- HTML, CSS, JavaScript만으로 브라우저 게임을 만들 수 있습니다.
- 게임을 설치 파일로 만들지 않아도 URL로 공유할 수 있습니다.
- Phaser가 장면, 입력, 도형, 글자 등의 기능을 제공합니다.
- 브라우저 개발자 도구로 오류와 파일 요청을 확인할 수 있습니다.
- CDN 방식을 사용하면 npm 설치 없이 간단히 시작할 수 있습니다.

## JavaScript + Phaser에서 확인한 단점

- HTML, CSS, JavaScript의 역할을 함께 이해해야 합니다.
- 로컬 파일을 안정적으로 실행하려면 웹 서버가 필요합니다.
- CDN 방식은 인터넷 연결과 외부 서비스 상태에 영향을 받습니다.
- 브라우저 보안 정책 때문에 프로그램 창을 직접 닫는 기능에는 제한이 있습니다.
- npm과 Vite를 이용하는 개발 환경은 설치 문제가 발생할 수 있습니다.

## LÖVE2D와 비교

| 항목 | LÖVE2D | Phaser |
|---|---|---|
| 언어 | Lua | JavaScript |
| 실행 환경 | LÖVE 프로그램 | 웹 브라우저 |
| 코드 작성 | VS Code | VS Code |
| 기본 배포 | `.love` 또는 Windows 실행 폴더 | 정적 웹사이트 |
| 공유 방법 | 파일 전달 | URL 공유 가능 |
| 화면 구성 | Lua 코드 | HTML, CSS, JavaScript |
| 현재 프로젝트 실행 | `love.exe` | Python 웹 서버 + CDN |

## 제작 결과

Windows와 VS Code에서 JavaScript + Phaser 개발 환경을 준비하고 LÖVE2D판과 동일한 장애물 피하기 게임을 구현했습니다. Vite의 네이티브 실행 충돌을 확인한 뒤 CDN과 Python 웹 서버 방식으로 전환해 게임을 정상 실행했습니다.

이를 통해 같은 게임이라도 프레임워크와 실행 환경에 따라 프로젝트 구성, 실행 방법, 배포 방법이 달라진다는 점을 확인했습니다.
