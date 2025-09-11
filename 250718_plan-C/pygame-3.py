import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Clone")

# 색상
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font_big   = pygame.font.SysFont(None, 50)
font_small = pygame.font.SysFont(None, 28)

# 패들 설정
paddle_width, paddle_height = 100, 12
paddle_speed = 8

# 공 설정
ball_radius = 8
base_ball_speed = 4  # 스테이지마다 약간 빨라지게 활용

# 벽돌 설정(공통)
BRICK_COLS = 8
BRICK_HEIGHT = 26

def build_bricks(rows, cols=BRICK_COLS, top_offset=50, h=BRICK_HEIGHT, gap=4):
    bricks = []
    brick_width = WIDTH // cols
    for r in range(rows):
        for c in range(cols):
            # 좌우/상하 간격(gap)을 살짝 주어 보기 좋게
            rect = pygame.Rect(
                c * brick_width + gap//2,
                top_offset + r * h + gap//2,
                brick_width - gap,
                h - gap
            )
            bricks.append(rect)
    return bricks

def draw_center_text(text, color, dy=0, big=True):
    surf = (font_big if big else font_small).render(text, True, color)
    win.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2 - surf.get_height()//2 + dy))

def reset_positions():
    paddle_x = WIDTH // 2 - paddle_width // 2
    paddle_y = HEIGHT - 30
    ball_x   = WIDTH // 2
    ball_y   = HEIGHT // 2
    return paddle_x, paddle_y, ball_x, ball_y

def run_game():
    # 스테이지 구성: 줄 수만 다르게
    stages_rows = [2, 4, 6]  # 1: 2줄, 2: 4줄, 3: 6줄
    stage_index = 0          # 0 → 1스테이지

    # 초기화
    paddle_x, paddle_y, ball_x, ball_y = reset_positions()
    ball_dx, ball_dy = base_ball_speed, -base_ball_speed
    bricks = build_bricks(stages_rows[stage_index])
    bricks_destroyed_total = 0

    running = True

    while running:
        clock.tick(60)
        win.fill(BLACK)

        # 이벤트
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # 공 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 공/패들/벽돌 사각형
        ball_rect   = pygame.Rect(int(ball_x - ball_radius), int(ball_y - ball_radius), ball_radius*2, ball_radius*2)
        paddle_rect = pygame.Rect(int(paddle_x), int(paddle_y), paddle_width, paddle_height)

        # 벽 충돌 (반지름 고려)
        if ball_x - ball_radius <= 0:
            ball_x = ball_radius
            ball_dx *= -1
        elif ball_x + ball_radius >= WIDTH:
            ball_x = WIDTH - ball_radius
            ball_dx *= -1
        if ball_y - ball_radius <= 0:
            ball_y = ball_radius
            ball_dy *= -1

        # 패들 충돌 (사각형 충돌)
        if ball_rect.colliderect(paddle_rect) and ball_dy > 0:
            # 튕길 때, 맞은 위치에 따라 약간의 각도 변화
            hit_pos = (ball_x - paddle_rect.centerx) / (paddle_width / 2)
            ball_dy *= -1
            ball_dx = max(min(ball_dx + hit_pos * 2.0, 8), -8)  # 좌우 속도 살짝 조정

            # 패들 위로 살짝 올려서 끼임 방지
            ball_y = paddle_rect.top - ball_radius - 1

        # 벽돌 충돌
        hit_idx = -1
        for i, brick in enumerate(bricks):
            if brick.colliderect(ball_rect):
                hit_idx = i
                # 어느 축으로 반사할지 겹침량으로 판정
                overlap_left   = ball_rect.right - brick.left
                overlap_right  = brick.right - ball_rect.left
                overlap_top    = ball_rect.bottom - brick.top
                overlap_bottom = brick.bottom - ball_rect.top
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

                if min_overlap == overlap_left:
                    ball_x -= overlap_left
                    ball_dx *= -1
                elif min_overlap == overlap_right:
                    ball_x += overlap_right
                    ball_dx *= -1
                elif min_overlap == overlap_top:
                    ball_y -= overlap_top
                    ball_dy *= -1
                else:
                    ball_y += overlap_bottom
                    ball_dy *= -1
                break

        if hit_idx >= 0:
            bricks.pop(hit_idx)
            bricks_destroyed_total += 1
            # ball_rect 갱신
            ball_rect.x = int(ball_x - ball_radius)
            ball_rect.y = int(ball_y - ball_radius)

        # 바닥으로 떨어짐 → 게임오버
        if ball_y - ball_radius >= HEIGHT:
            draw_center_text("Game Over", RED)
            pygame.display.update()
            pygame.time.delay(1500)
            return  # 함수 종료 → 프로그램 종료

        # 스테이지 클리어 → 다음 스테이지로
        if not bricks:
            stage_index += 1
            if stage_index >= len(stages_rows):
                # 모든 스테이지 클리어 → 승리
                win.fill(BLACK)
                draw_center_text("You Win!", BLUE)
                draw_center_text(f"Total Bricks: {bricks_destroyed_total}", WHITE, dy=50, big=False)
                pygame.display.update()
                pygame.time.delay(1500)
                return
            else:
                # 다음 스테이지 준비
                win.fill(BLACK)
                draw_center_text(f"Stage {stage_index + 1}", WHITE)
                pygame.display.update()
                pygame.time.delay(800)

                # 난이도 소폭 상승(공 속도 증가)
                speed = base_ball_speed + stage_index  # 1스테이지: 4, 2:5, 3:6
                ball_dx = speed if ball_dx >= 0 else -speed
                ball_dy = -speed

                bricks = build_bricks(stages_rows[stage_index])
                paddle_x, paddle_y, ball_x, ball_y = reset_positions()
        # 그리기
        pygame.draw.circle(win, WHITE, (int(ball_x), int(ball_y)), ball_radius)
        pygame.draw.rect(win, BLUE, paddle_rect)
        for brick in bricks:
            pygame.draw.rect(win, RED, brick)

        # HUD (스테이지/점수)
        stage_text = font_small.render(f"Stage: {stage_index + 1} / {len(stages_rows)}", True, WHITE)
        score_text = font_small.render(f"Bricks: {bricks_destroyed_total}", True, WHITE)
        win.blit(stage_text, (10, 8))
        win.blit(score_text, (10, 32))

        pygame.display.update()

def main():
    run_game()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()