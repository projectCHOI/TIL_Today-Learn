# 날아오는 물체의 크기 날아오는 방향
def reset_enemy():
    global enemy_pos, enemy_direction, enemy_size
    enemy_size = random.randint(10, 50)  # 물체 크기를 10에서 50 사이의 랜덤한 값으로 설정
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    
    if edge == 'top':
        enemy_pos = [random.randint(0, width - enemy_size), 0]
        enemy_direction = [0, enemy_speed]
    elif edge == 'bottom':
        enemy_pos = [random.randint(0, width - enemy_size), height - enemy_size]
        enemy_direction = [0, -enemy_speed]
    elif edge == 'left':
        enemy_pos = [0, random.randint(0, height - enemy_size)]
        enemy_direction = [enemy_speed, 0]
    else:  # edge == 'right'
        enemy_pos = [width - enemy_size, random.randint(0, height - enemy_size)]
        enemy_direction = [-enemy_speed, 0]


# 플레이어의 이동 처리 담당
if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
    player_pos[0] -= player_speed
if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
    player_pos[0] += player_speed
if keys[pygame.K_UP] and player_pos[1] > player_speed:
    player_pos[1] -= player_speed
if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
    player_pos[1] += player_speed


# 플레이 시간을 나타내는 코드
if not game_over:
    elapsed_time = time.time() - start_time
    time_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, white)
    win.blit(time_text, (10, 10))
