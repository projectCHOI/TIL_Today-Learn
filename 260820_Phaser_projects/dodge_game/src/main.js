class MainScene extends Phaser.Scene {
    constructor() {
        super("MainScene");
    }

    create() {
        this.cameras.main.setBackgroundColor("#11131a");

        // 게임 상태
        this.gameState = "playing";

        // 플레이어
        this.player = this.add.rectangle(
            240,
            322.5,
            50,
            25,
            0x33b3ff
        );

        this.playerSpeed = 300;

        // 장애물
        this.obstacle = this.add.rectangle(
            240,
            -17.5,
            35,
            35,
            0xff3333
        );

        this.obstacleSpeed = 160;

        // 점수
        this.score = 0;

        this.scoreText = this.add.text(
            10,
            10,
            "Score: 0",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.scoreText.setDepth(10);

        // 방향키
        this.cursors = this.input.keyboard.createCursorKeys();

        // 다시 시작 키
        this.restartKey = this.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.R
        );

        this.input.keyboard.addCapture([
            Phaser.Input.Keyboard.KeyCodes.LEFT,
            Phaser.Input.Keyboard.KeyCodes.RIGHT,
            Phaser.Input.Keyboard.KeyCodes.R
        ]);

        // 게임 종료용 어두운 배경
        this.gameOverBackground = this.add.rectangle(
            240,
            180,
            480,
            360,
            0x000000,
            0.75
        );

        this.gameOverBackground
            .setDepth(20)
            .setVisible(false);

        // GAME OVER 글자
        this.gameOverText = this.add.text(
            240,
            125,
            "GAME OVER",
            {
                fontFamily: "Arial",
                fontSize: "28px",
                color: "#ff3333"
            }
        );

        this.gameOverText
            .setOrigin(0.5)
            .setDepth(21)
            .setVisible(false);

        // 최종 점수
        this.finalScoreText = this.add.text(
            240,
            175,
            "Final Score: 0",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.finalScoreText
            .setOrigin(0.5)
            .setDepth(21)
            .setVisible(false);

        // 다시 시작 안내
        this.restartText = this.add.text(
            240,
            215,
            "Press R to Restart",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.restartText
            .setOrigin(0.5)
            .setDepth(21)
            .setVisible(false);

        this.resetObstacle();
    }

    resetObstacle() {
        const obstacleHalfWidth = this.obstacle.width / 2;

        this.obstacle.x = Phaser.Math.Between(
            obstacleHalfWidth,
            480 - obstacleHalfWidth
        );

        this.obstacle.y = -this.obstacle.height / 2;
    }

    checkCollision() {
        const playerLeft =
            this.player.x - this.player.width / 2;

        const playerRight =
            this.player.x + this.player.width / 2;

        const playerTop =
            this.player.y - this.player.height / 2;

        const playerBottom =
            this.player.y + this.player.height / 2;

        const obstacleLeft =
            this.obstacle.x - this.obstacle.width / 2;

        const obstacleRight =
            this.obstacle.x + this.obstacle.width / 2;

        const obstacleTop =
            this.obstacle.y - this.obstacle.height / 2;

        const obstacleBottom =
            this.obstacle.y + this.obstacle.height / 2;

        return (
            playerLeft < obstacleRight &&
            playerRight > obstacleLeft &&
            playerTop < obstacleBottom &&
            playerBottom > obstacleTop
        );
    }

    showGameOver() {
        this.gameState = "gameover";

        this.finalScoreText.setText(
            `Final Score: ${this.score}`
        );

        this.gameOverBackground.setVisible(true);
        this.gameOverText.setVisible(true);
        this.finalScoreText.setVisible(true);
        this.restartText.setVisible(true);
    }

    resetGame() {
        this.gameState = "playing";

        this.player.x = 240;
        this.player.y = 322.5;

        this.obstacleSpeed = 160;

        this.score = 0;
        this.scoreText.setText("Score: 0");

        this.gameOverBackground.setVisible(false);
        this.gameOverText.setVisible(false);
        this.finalScoreText.setVisible(false);
        this.restartText.setVisible(false);

        this.resetObstacle();
    }

    update(time, delta) {
        // 게임 종료 상태
        if (this.gameState === "gameover") {
            if (
                Phaser.Input.Keyboard.JustDown(
                    this.restartKey
                )
            ) {
                this.resetGame();
            }

            return;
        }

        const dt = delta / 1000;

        // 플레이어 이동
        if (this.cursors.left.isDown) {
            this.player.x -= this.playerSpeed * dt;
        }

        if (this.cursors.right.isDown) {
            this.player.x += this.playerSpeed * dt;
        }

        // 화면 경계 제한
        const playerHalfWidth =
            this.player.width / 2;

        this.player.x = Phaser.Math.Clamp(
            this.player.x,
            playerHalfWidth,
            480 - playerHalfWidth
        );

        // 장애물 낙하
        this.obstacle.y +=
            this.obstacleSpeed * dt;

        const obstacleTop =
            this.obstacle.y -
            this.obstacle.height / 2;

        // 장애물을 피하면 점수 증가
        if (obstacleTop > 360) {
            this.score += 1;

            this.scoreText.setText(
                `Score: ${this.score}`
            );

            this.resetObstacle();
        }

        // 충돌 확인
        if (this.checkCollision()) {
            this.showGameOver();
        }
    }
}

const config = {
    type: Phaser.AUTO,

    width: 480,
    height: 360,

    parent: "game-container",
    backgroundColor: "#11131a",

    scene: [MainScene]
};

new Phaser.Game(config);