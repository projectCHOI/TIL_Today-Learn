class MainScene extends Phaser.Scene {
    constructor() {
        super("MainScene");
    }

    create() {
        this.cameras.main.setBackgroundColor("#11131a");

        this.player = this.add.rectangle(
            240,
            322.5,
            50,
            25,
            0x33b3ff
        );

        this.playerSpeed = 300;

        this.cursors = this.input.keyboard.createCursorKeys();

        this.input.keyboard.addCapture([
            Phaser.Input.Keyboard.KeyCodes.LEFT,
            Phaser.Input.Keyboard.KeyCodes.RIGHT
        ]);
    }

    update(time, delta) {
        const dt = delta / 1000;

        if (this.cursors.left.isDown) {
            this.player.x -= this.playerSpeed * dt;
        }

        if (this.cursors.right.isDown) {
            this.player.x += this.playerSpeed * dt;
        }

        const playerHalfWidth = this.player.width / 2;

        this.player.x = Phaser.Math.Clamp(
            this.player.x,
            playerHalfWidth,
            480 - playerHalfWidth
        );
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