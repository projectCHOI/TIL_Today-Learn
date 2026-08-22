class MainScene extends Phaser.Scene {
    constructor() {
        super("MainScene");
    }

    create() {
        this.cameras.main.setBackgroundColor("#11131a");

        // 플레이어 만들기
        this.player = this.add.rectangle(
            240,
            322.5,
            50,
            25,
            0x33b3ff
        );

        this.playerSpeed = 300;

        // 장애물 만들기
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

        this.input.keyboard.addCapture([
            Phaser.Input.Keyboard.KeyCodes.LEFT,
            Phaser.Input.Keyboard.KeyCodes.RIGHT
        ]);

        // 장애물의 첫 위치 결정
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

    update(time, delta) {
        const dt = delta / 1000;

        // 플레이어 이동
        if (this.cursors.left.isDown) {
            this.player.x -= this.playerSpeed * dt;
        }

        if (this.cursors.right.isDown) {
            this.player.x += this.playerSpeed * dt;
        }

        // 플레이어 화면 경계 제한
        const playerHalfWidth = this.player.width / 2;

        this.player.x = Phaser.Math.Clamp(
            this.player.x,
            playerHalfWidth,
            480 - playerHalfWidth
        );

        // 장애물 낙하
        this.obstacle.y += this.obstacleSpeed * dt;

        const obstacleTop =
            this.obstacle.y - this.obstacle.height / 2;

        // 장애물이 화면 아래를 완전히 통과했는지 확인
        if (obstacleTop > 360) {
            this.score += 1;

            this.scoreText.setText(
                `Score: ${this.score}`
            );

            this.resetObstacle();
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