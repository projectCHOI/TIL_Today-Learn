# Pong

LÖVE2D와 Lua를 사용하여 제작한 **Pong 게임 프로젝트**

1972년 Atari의 고전 게임 **Pong**을 참고하여 기본적인 패들-볼 게임 구조를 구현하고, 1인 플레이, 2인 플레이, 점수 시스템, 일시정지, 게임 오버 등의 기능을 추가.

또한 개발이 완료된 게임을 `.love` 파일과 Windows용 실행 파일(`Pong.exe`)로 패키징하여, LÖVE2D가 설치되어 있지 않은 Windows 환경에서도 실행할 수 있도록 배포본을 제작.

## 1. 프로젝트 소개

이 프로젝트는 Lua와 LÖVE2D의 기본적인 게임 개발 구조를 학습하기 위해 시작했다.

Pong의 핵심 구조인

* 패들 이동
* 공 이동
* 충돌 판정
* 점수 처리

를 구현하고, 이후 게임 상태 관리와 AI, 난이도 변화 등의 기능을 단계적으로 추가했다.

### 개발 환경

* Language : Lua
* Framework : LÖVE2D
* Editor : Visual Studio Code
* Platform : Windows

---

## 2. 주요 기능

### 1 Player

플레이어와 AI가 대결하는 모드

* Player 1은 왼쪽 패들을 조작
* 오른쪽 패들은 AI가 자동으로 움직인다.
* 공의 속도가 증가하면 AI의 이동 속도도 함께 증가해 긴장감 유지

### 2 Player

두 명의 플레이어가 하나의 키보드로 대결하는 모드

* Player 1 : 왼쪽 패들
* Player 2 : 오른쪽 패들
* Player 2 패들은 노란색으로 표시됩니다.

### Score System

상대방이 공을 받아내지 못하면 점수를 획득.

먼저 **5점**을 획득한 플레이어가 승리.

### Rally System

패들이 공을 받아낼 때마다 `RALLY` 값이 증가

새로운 서브가 시작되거나 점수가 발생하면 Rally 값은 다시 초기화

### Ball Speed

게임이 계속될수록 공의 수평 이동 속도가 증가

* 초기 수평 속도 : 120
* 패들 충돌 시 증가량 : 12
* 최대 수평 속도 : 300

공이 패들의 어느 위치에 충돌했는지에 따라 수직 방향과 속도가 달라진다.

패들 중앙에 정확히 충돌하여 수직 속도가 0이 되는 경우에는 최소 수직 속도를 적용하여 공이 계속 수평으로만 이동하는 상황을 방지했다.

### AI Difficulty

1 Player 모드의 AI는 공의 수평 속도에 따라 이동 속도가 증가

따라서 Rally가 길어지고 공이 빨라질수록 AI도 더 빠르게 반응해 플레이 긴장감 유지.

### Game State

게임의 구성은 다음 상태로 관리

* Menu
* Ready
* Playing
* Paused
* Game Over

각 상태에 따라 입력과 화면 표시가 달라진다.

---

## 3. 조작 방법

### Menu

| 입력       | 기능       |
| -------- | -------- |
| Mouse    | 게임 모드 선택 |
| Player 1 | AI 대전 시작 |
| Player 2 | 2인 대전 시작 |

### Player 1

| 키 | 기능     |
| - | ------ |
| W | 위로 이동  |
| S | 아래로 이동 |

### Player 2

| 키 | 기능     |
| - | ------ |
| O | 위로 이동  |
| K | 아래로 이동 |

### Game

| 키     | 기능           |
| ----- | ------------ |
| SPACE | 서브 시작        |
| P     | 일시정지 / 게임 복귀 |
| ESC   | 메뉴로 이동       |

### Game Over

| 키   | 기능         |
| --- | ---------- |
| R   | 같은 모드로 재시작 |
| ESC | 메뉴로 이동     |

---

## 4. 게임 진행

게임 모드를 선택하면 `READY` 상태로 시작

`SPACE` 키를 누르면 공이 움직이며 Rally가 시작.

```text
MENU
  ↓
READY
  ↓
SPACE
  ↓
PLAYING
  ↓
SCORE
  ↓
READY
```

게임 도중 `P`를 누르면:

```text
PLAYING
  ↓
PAUSED
  ↓
PLAYING
```

상태로 전환된다.

한 플레이어가 5점을 획득하면:

```text
PLAYING
  ↓
GAME OVER
```

상태.

Game Over 화면에서는 최종 점수와 승자를 확인할 수 있다.

---

## 5. 프로젝트 구조

```text
pong_game/
│
├─ main.lua
├─ conf.lua
│
└─ assets/
   └─ fonts/
      └─ SLEIGothicTTF.ttf
```

### main.lua

게임의 주요 로직

* 게임 상태 관리
* 플레이어 입력
* AI
* 공 이동
* 충돌 판정
* 점수
* Rally
* 화면 출력

등을 담당.

### conf.lua

LÖVE2D 게임 창의 기본 설정을 구성

현재 게임 해상도는:

```text
800 × 600
```

### assets

게임에서 사용하는 외부 리소스를 저장

현재 프로젝트에서는 게임 UI에 사용할 폰트가 포함되어 있다.

---

## 6. 개발 버전 실행

LÖVE2D가 설치되어 있는 환경에서는 프로젝트 폴더에서 다음과 같이 실행할 수 있다.

```powershell
love .
```

또는 `love.exe`의 경로를 직접 지정하여 실행 가능.

---

## 7. Windows 배포

프로젝트 개발 완료 후 `.love` 패키지를 제작.

```text
main.lua
conf.lua
assets/
   ↓
pong_game.love
```

이후 LÖVE 실행 파일과 게임 패키지를 결합하여 Windows 실행 파일을 제작.

```text
love.exe
    +
pong_game.love
    ↓
Pong.exe
```

최종 Windows 배포 폴더는 다음과 같이 구성

```text
Pong_Windows/
│
├─ Pong.exe
├─ love.dll
├─ lua51.dll
├─ mpg123.dll
├─ msvcp120.dll
├─ msvcr120.dll
├─ OpenAL32.dll
├─ SDL2.dll
└─ license.txt
```

최종적으로 해당 폴더를:

```text
Pong_Windows.zip
```

으로 압축하여 Windows용 배포 파일을 제작

압축 파일을 별도의 위치에 해제한 후 `Pong.exe`를 실행하여 정상 작동하는 것도 확인.

따라서 Windows 배포판은 LÖVE2D를 별도로 설치하지 않은 환경에서도 실행할 수 있도록 구성되어 있다.

---

## 8. 개발 과정에서 학습한 내용

이번 프로젝트를 통해 다음 내용을 직접 구현하고 확인

* Lua 기본 문법
* LÖVE2D 프로젝트 구조
* `love.load`
* `love.update`
* `love.draw`
* 키보드 입력 처리
* 마우스 입력 처리
* Delta Time을 이용한 이동
* 패들 이동과 화면 경계 처리
* 공의 자동 이동
* 화면 상단/하단 충돌
* AABB 방식의 패들 충돌 판정
* 충돌 위치에 따른 공의 반사 방향 변화
* Rally 시스템
* 점수 시스템
* AI 이동
* 게임 상태 관리
* Pause / Resume
* Game Over / Restart
* 커스텀 폰트 적용
* `.love` 패키징
* Windows 실행 파일 제작
* Windows 배포용 ZIP 제작

---

## 9. 프로젝트 결과

이번 프로젝트에서는 단순히 Pong의 기본 동작만 구현하는 것에서 끝나지 않고,

**게임 제작 → 기능 개선 → UI 개선 → 테스트 → 패키징 → Windows 배포**

까지 전체 과정을 경험하는 것을 목표로 했다.

최종적으로 1 Player와 2 Player 모드를 모두 지원하는 Pong 게임을 완성했으며, Windows에서 실행할 수 있는 독립 배포본까지 제작했다.

---

## Version

**v1.0.0**

첫 번째 완성 및 Windows 배포 버전.