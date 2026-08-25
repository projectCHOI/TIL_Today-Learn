# Dodge Game — Lua + LÖVE2D

Windows와 Visual Studio Code 환경에서 Lua와 LÖVE2D를 사용해 만든 2D 장애물 피하기 게임입니다.

이 프로젝트의 목표는 개발 환경 설치부터 게임 제작, 실행, `.love` 파일 생성, Windows 배포까지 전체 과정을 직접 경험하는 것입니다. 

## 개발 환경

| 항목 | 사용 환경 |
|---|---|
| 운영체제 | Windows |
| 코드 편집기 | Visual Studio Code |
| 언어 | Lua |
| 게임 프레임워크 | LÖVE 11.5 |
| 게임 화면 | 480 × 360 |

LÖVE는 Lua로 2D 게임을 만들 수 있는 무료 오픈소스 프레임워크입니다.

- 공식 사이트: <https://love2d.org/>
- 공식 시작 안내: <https://love2d.org/wiki/Getting_Started>

## 게임 소개

플레이어를 좌우로 움직여 위에서 떨어지는 장애물을 피하는 게임입니다.

- 장애물을 피할 때마다 점수가 1점 증가합니다.
- 점수가 5점 증가할 때마다 단계와 장애물 속도가 올라갑니다.
- 장애물과 충돌하면 게임이 종료됩니다.
- 최고 난이도는 7단계입니다.

## 구현 기능

- 시작 화면
- 키보드 좌우 이동
- 화면 밖 이동 방지
- 무작위 위치에서 생성되는 장애물
- 사각형 충돌 판정
- 점수와 단계 표시
- 단계별 장애물 속도 증가
- `P` 키 일시정지 및 계속하기
- 게임 종료 화면
- 최종 점수와 도달 단계 표시
- `R` 키 다시 시작
- `Esc` 키 게임 종료
- `.love` 파일 제작
- Windows 배포용 실행 파일 제작

## 조작 방법

| 키 | 기능 |
|---|---|
| `Enter` 또는 `Space` | 시작 화면에서 게임 시작 |
| `←` | 왼쪽으로 이동 |
| `→` | 오른쪽으로 이동 |
| `P` | 일시정지 또는 계속하기 |
| `R` | 게임 종료 화면에서 다시 시작 |
| `Esc` | 게임 종료 |

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

속도는 초당 이동 거리를 나타냅니다. `love.update(dt)`에서 속도에 `dt`를 곱해 컴퓨터의 화면 갱신 속도가 달라도 움직임이 크게 달라지지 않도록 했습니다.

## 프로젝트 구조

```text
260817_love2d_projects
├── dodge_game
│   ├── conf.lua
│   └── main.lua
├── dodge_game.love
└── dodge_game_windows
    ├── dodge_game.exe
    ├── license.txt
    └── LÖVE 실행에 필요한 DLL 파일
```

### `main.lua`

게임의 실제 동작을 담당합니다.

- 플레이어와 장애물 정보
- 키보드 입력
- 이동과 충돌 판정
- 점수와 난이도
- 시작·진행·일시정지·게임 종료 상태
- 화면 그리기

### `conf.lua`

게임 창의 제목과 크기를 설정합니다.

```lua
function love.conf(t)
    t.window.title = "Dodge Game"
    t.window.width = 480
    t.window.height = 360
    t.window.resizable = false
end
```

## 실행 방법

### 1. 프로젝트 폴더 실행

VS Code에서 `dodge_game` 폴더를 열고 PowerShell 터미널을 실행합니다.

```powershell
& "C:\설치_soft\260817_Code\LOVE\love.exe" .
```

LÖVE를 다른 경로에 설치했다면 `love.exe` 경로를 실제 설치 위치에 맞게 변경해야 합니다.

### 2. `.love` 파일 실행

```powershell
& "C:\설치_soft\260817_Code\LOVE\love.exe" "..\dodge_game.love"
```

`.love`는 게임 파일을 하나로 묶은 형식입니다. `.love` 파일만 실행하려면 해당 컴퓨터에 LÖVE가 설치되어 있어야 합니다.

### 3. Windows 배포판 실행

```powershell
& "..\dodge_game_windows\dodge_game.exe"
```

다른 Windows 컴퓨터에 전달할 때는 `dodge_game.exe`만 복사하지 않고 `dodge_game_windows` 폴더 전체를 전달해야 합니다. 함께 들어 있는 DLL 파일이 없으면 실행되지 않을 수 있습니다.

## `.love` 파일 만들기

`dodge_game` 폴더 안에서 다음 명령어를 실행합니다.

```powershell
Compress-Archive -Path ".\main.lua", ".\conf.lua" -DestinationPath "..\dodge_game.zip" -Force
Rename-Item -Path "..\dodge_game.zip" -NewName "dodge_game.love"
```

압축 파일의 최상위 위치에 `main.lua`와 `conf.lua`가 있어야 합니다.

```text
dodge_game.love
├── conf.lua
└── main.lua
```

두 파일이 별도의 `dodge_game` 폴더 안에 들어가면 LÖVE가 `main.lua`를 찾지 못할 수 있습니다.

## Windows 배포 파일 만들기

먼저 배포 폴더를 만듭니다.

```powershell
New-Item -ItemType Directory -Path "..\dodge_game_windows" -Force
```

`love.exe`와 `.love` 파일을 결합합니다.

```powershell
cmd /c 'copy /b "C:\설치_soft\260817_Code\LOVE\love.exe"+"..\dodge_game.love" "..\dodge_game_windows\dodge_game.exe"'
```

필요한 DLL과 라이선스 파일을 복사합니다.

```powershell
Copy-Item "C:\설치_soft\260817_Code\LOVE\*.dll" "..\dodge_game_windows\" -Force
Copy-Item "C:\설치_soft\260817_Code\LOVE\license.txt" "..\dodge_game_windows\" -Force
```

32비트와 64비트 LÖVE 파일을 섞지 않아야 합니다.

## 코드에서 익힌 내용

### LÖVE의 기본 함수

| 함수 | 역할 |
|---|---|
| `love.load()` | 게임 시작 시 한 번 실행 |
| `love.update(dt)` | 게임의 위치와 상태를 계속 변경 |
| `love.draw()` | 화면에 도형과 글자 표시 |
| `love.keypressed(key)` | 한 번 누른 키 처리 |

### Lua 테이블

플레이어와 장애물의 여러 정보를 하나의 테이블로 관리했습니다.

```lua
player = {
    x = 215,
    y = 310,
    width = 50,
    height = 25,
    speed = 300
}
```

### 게임 상태

문자열을 이용해 현재 상태를 구분했습니다.

```text
start → playing ⇄ paused
             ↓
          gameover
```

- `start`: 시작 화면
- `playing`: 게임 진행
- `paused`: 일시정지
- `gameover`: 게임 종료

### 충돌 판정

플레이어와 장애물을 직사각형으로 보고 양쪽 영역이 겹치는지 검사했습니다. 이 방식은 일반적으로 AABB 충돌 판정이라고 부릅니다.

## LÖVE2D를 사용하며 확인한 장점

- 무료 오픈소스입니다.
- Lua 문법이 비교적 짧고 이해하기 쉽습니다.
- VS Code에서 모든 게임 코드를 작성할 수 있습니다.
- 복잡한 설치 도구 없이 작은 2D 게임을 빠르게 만들 수 있습니다.
- 화면 출력, 키보드 입력, 시간 계산 기능이 기본으로 제공됩니다.
- `.love` 형식으로 프로젝트를 하나의 파일로 묶을 수 있습니다.

## LÖVE2D를 사용하며 확인한 단점

- 화면에서 캐릭터를 배치하는 장면 편집기가 없습니다.
- 버튼이나 메뉴도 대부분 코드로 직접 만들어야 합니다.
- 프로젝트가 커지면 파일과 코드를 직접 나누어 관리해야 합니다.
- `.love` 파일만으로는 LÖVE가 설치되지 않은 컴퓨터에서 실행할 수 없습니다.
- Windows 배포 시 실행 파일과 여러 DLL을 함께 전달해야 합니다.


