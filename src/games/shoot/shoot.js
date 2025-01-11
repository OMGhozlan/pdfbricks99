// Tetris game logic
function setInterval(cb, ms) {
    evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

var rand_seed = Date.now() % 2147483647;
function rand() {
    return rand_seed = rand_seed * 16807 % 2147483647;
}

// Shooter game modifications
const WIDTH = 10; // Width of the game grid
const HEIGHT = 20; // Height of the game grid
var TICK_INTERVAL = 50;
var GAME_STEP_TIME = 400;
var time_ms = 0;
var last_update = 0;
var interval = 0;

let grid;
let player;
let bullets;
let enemies;
let enemyBullets;
let score;
let gameOver;

function set_controls_visibility(state) {
    this.getField("T_input").hidden = !state;
    this.getField("B_left").hidden = !state;
    this.getField("B_right").hidden = !state;
    this.getField("B_shoot").hidden = !state;
    this.getField("B_shoot").hidden = !state;
}

function game_init() {
    grid = Array.from({ length: HEIGHT }, () => Array(WIDTH).fill(-1));
    player = { x: Math.floor(WIDTH / 2), y: HEIGHT - 1 };
    bullets = [];
    enemies = [];
    enemyBullets = [];
    score = 0;
    gameOver = false;

    spawnEnemies();

    interval = setInterval(game_tick, TICK_INTERVAL);
    this.getField("B_start").hidden = true;
    set_controls_visibility(true);    
}

// Move the player
function movePlayer(direction) {
    if (direction === 'left' && player.x > 0) {
        player.x--;
    } else if (direction === 'right' && player.x < WIDTH - 1) {
        player.x++;
    }
}

// Shoot a bullet
function shoot() {
    bullets.push({ x: player.x, y: player.y - 1 });
}

// Spawn enemies
function spawnEnemies() {
    for (let i = 0; i < WIDTH; i++) {
        if (rand() % 5 === 0) {
            enemies.push({ x: i, y: 0 });
        }
    }
}

// Enemies shoot bullets
function enemyShoot() {
    enemies.forEach(enemy => {
        if (rand() % 10 === 0) {
            enemyBullets.push({ x: enemy.x, y: enemy.y + 1 });
        }
    });
}

// Update game state
function game_update() {
    if (gameOver) return;

    // Move player bullets
    bullets = bullets.filter(bullet => bullet.y > 0);
    bullets.forEach(bullet => bullet.y--);

    // Move enemy bullets
    enemyBullets = enemyBullets.filter(bullet => bullet.y < HEIGHT);
    enemyBullets.forEach(bullet => bullet.y++);

    // Move enemies
    enemies.forEach(enemy => enemy.y++);

    // Check for collisions with player bullets
    bullets.forEach(bullet => {
        enemies = enemies.filter(enemy => {
            if (enemy.x === bullet.x && enemy.y === bullet.y) {
                score++;
                return false; // Remove the enemy
            }
            return true;
        });
    });

    // Check for collisions with enemy bullets
    enemyBullets.forEach(bullet => {
        if (bullet.x === player.x && bullet.y === player.y) {
            gameOver = true;
        }
    });

    // Remove enemies that reach the bottom
    enemies = enemies.filter(enemy => {
        if (enemy.y >= HEIGHT) {
            gameOver = true;
            return false;
        }
        return true;
    });

    // Spawn new enemies and have them shoot
    if (rand() % 10 === 0) {
        spawnEnemies();
    }
    enemyShoot();
}

// Render the game state
function draw() {
    grid = Array.from({ length: HEIGHT }, () => Array(WIDTH).fill(0));

    // Draw player
    grid[player.y][player.x] = 1;

    // Draw player bullets
    bullets.forEach(bullet => {
        if (bullet.y >= 0 && bullet.y < HEIGHT) {
            grid[bullet.y][bullet.x] = 2;
        }
    });

    // Draw enemies
    enemies.forEach(enemy => {
        if (enemy.y >= 0 && enemy.y < HEIGHT) {
            grid[enemy.y][enemy.x] = 3;
        }
    });

    // Draw enemy bullets
    enemyBullets.forEach(bullet => {
        if (bullet.y >= 0 && bullet.y < HEIGHT) {
            grid[bullet.y][bullet.x] = 4;
        }
    });

    console.clear();
    console.log(`Score: ${score}`);
    grid.forEach(row => console.log(row.map(cell => (cell === 1 ? 'P' : cell === 2 ? '*' : cell === 3 ? 'E' : cell === 4 ? 'o' : '.')).join(' ')));
    if (gameOver) console.log("Game Over!");
}

function set_pixel(x, y, state) {
    if (x < 0 || y < 0 || x >= ###GRID_WIDTH### || y >= ###GRID_HEIGHT###) {
        return;
    }
    pixel_fields[x][###GRID_HEIGHT### - 1 - y].hidden = !state;
}

function draw_field() {
    for (var x = 0; x < ###GRID_WIDTH###; ++x) {
        for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
            set_pixel(x, y, field[x][y]);
        }
    }
}

function game_tick() {
    time_ms += TICK_INTERVAL;
    game_update();
    draw();
}

function draw_updated_score() {
    this.getField("T_score").value = `Score: ${score}`;
}

function game_over() {
    app.clearInterval(interval);
    app.alert(`Game over! Score: ${score}\nRefresh to restart.`);
}


// Handle player input
function handle_input(event) {
    switch (event.change) {
        case 'a': movePlayer('left'); break;
        case 'd': movePlayer('right'); break;
        case ' ': shoot(); break;
    }
}

set_controls_visibility(false);
app.execMenuItem("FitPage");