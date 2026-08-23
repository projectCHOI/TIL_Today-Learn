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
