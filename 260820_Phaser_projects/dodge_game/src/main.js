class MainScene extends Phaser.Scene {
    constructor() {
        super("MainScene");
    }

    create() {
        this.cameras.main.setBackgroundColor("#11131a");

        this.add
            .text(
                240,
                180,
                "Hello, Phaser!",
                {
                    fontFamily: "Arial",
                    fontSize: "24px",
                    color: "#ffffff"
                }
            )
            .setOrigin(0.5);
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