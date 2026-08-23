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

        // 난이도 설정
        this.baseObstacleSpeed = 160;
        this.obstacleSpeed = 160;
        this.speedStep = 35;
        this.maxLevel = 7;

        this.score = 0;
        this.level = 1;

        // 점수 표시
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

        // 단계 표시
        this.levelText = this.add.text(
            240,
            10,
            "Level: 1",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.levelText
            .setOrigin(0.5, 0)
            .setDepth(10);

        // 속도 표시
        this.speedText = this.add.text(
            470,
            10,
            "Speed: 160",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.speedText
            .setOrigin(1, 0)
            .setDepth(10);

        // 키보드
        this.cursors = this.input.keyboard.createCursorKeys();

        this.restartKey = this.input.keyboard.addKey(
            Phaser.Input.Keyboard.KeyCodes.R
        );

        this.input.keyboard.addCapture([
            Phaser.Input.Keyboard.KeyCodes.LEFT,
            Phaser.Input.Keyboard.KeyCodes.RIGHT,
            Phaser.Input.Keyboard.KeyCodes.R
        ]);

        // 게임 종료 배경
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

        // 게임 종료 제목
        this.gameOverText = this.add.text(
            240,
            110,
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
            160,
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

        // 최종 단계
        this.finalLevelText = this.add.text(
            240,
            190,
            "Reached Level: 1",
            {
                fontFamily: "Arial",
                fontSize: "16px",
                color: "#ffffff"
            }
        );

        this.finalLevelText
            .setOrigin(0.5)
            .setDepth(21)
            .setVisible(false);

        // 다시 시작 안내
        this.restartText = this.add.text(
            240,
            235,
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
        const obstacleHalfWidth =
            this.obstacle.width / 2;

        this.obstacle.x = Phaser.Math.FloatBetween(
            obstacleHalfWidth,
            480 - obstacleHalfWidth
        );

        this.obstacle.y =
            -this.obstacle.height / 2;
    }

    updateDifficulty() {
        const calculatedLevel =
            Math.floor(this.score / 5) + 1;

        this.level = Math.min(
            calculatedLevel,
            this.maxLevel
        );

        this.obstacleSpeed =
            this.baseObstacleSpeed +
            (this.level - 1) * this.speedStep;

        this.levelText.setText(
            `Level: ${this.level}`
        );

        this.speedText.setText(
            `Speed: ${this.obstacleSpeed}`
        );
    }