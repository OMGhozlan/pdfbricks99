function setInterval(cb, ms) {
    evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

var rand_seed = Date.now() % 2147483647;
function rand() {
    return rand_seed = rand_seed * 16807 % 2147483647;
}

// Parameters grouped in a dictionary
var PARAMETERS = {
    TICK_INTERVAL: 50,
    GAME_SPEED: 50,
    PIPE_GAP: 12,
    PIPE_DISTANCE: 20,
    GRAVITY: 0.25,
    FLAP_STRENGTH: -2,
    GRID_WIDTH: ###GRID_WIDTH###,
    GRID_HEIGHT: ###GRID_HEIGHT###,
    PIPE_WIDTH: 6,       // Wider pipes
    BIRD_SIZE: 2,
    MIN_PIPE_BUFFER: (###GRID_HEIGHT### / 10),  // Minimum gap from edges (GRID_HEIGHT / 10)
    SKY_PROBABILITY: 0.05 // Probability of a pixel being white in the sky
};

// Bird color scheme
var BIRD_COLORS = {
    topLeft: color.red,       // Top-left part of the bird
    topRight: color.yellow,  // Top-right part of the bird
    bottomLeft: color.orange, // Bottom-left part of the bird
    bottomRight: color.blue  // Bottom-right part of the bird
};

// Background colors
var BACKGROUND_COLOR = color.cyan;
var SKY_COLOR = color.white;
var GRASS_COLOR = color.green;

// Game state
var pixel_fields = [];
var field = [];
var score = 0;
var time_ms = 0;
var interval = 0;
var game_started = false;

// Bird
var birdX = 10;
var birdY = 10;
var birdVY = 0;

// Pipes
var pipes = [];

function set_controls_visibility(state) {
    this.getField("B_flap").hidden = !state;
}

function game_init() {
    for (var x = 0; x < PARAMETERS.GRID_WIDTH; ++x) {
        field[x] = [];
        for (var y = 0; y < PARAMETERS.GRID_HEIGHT; ++y) {
            field[x][y] = false;
        }
    }

    for (var x = 0; x < PARAMETERS.GRID_WIDTH; ++x) {
        pixel_fields[x] = [];
        for (var y = 0; y < PARAMETERS.GRID_HEIGHT; ++y) {
            pixel_fields[x][y] = this.getField("P_" + x + "_" + y);
        }
    }

    birdX = 5;
    birdY = Math.floor(PARAMETERS.GRID_HEIGHT / 2);
    birdVY = 0;

    pipes = [];

    score = 0;
    draw_updated_score();

    game_started = true;
    time_ms = 0;

    this.getField("B_start").hidden = true;
    set_controls_visibility(true);

    interval = setInterval(game_tick, PARAMETERS.TICK_INTERVAL);
}

function game_tick() {
    this.getField("T_input").hidden = false;
    if (!game_started) return;

    time_ms += PARAMETERS.TICK_INTERVAL;

    birdVY += PARAMETERS.GRAVITY;
    birdY += birdVY;
    if (birdY < 0) {
        birdY = 0;
        birdVY = 0;
    }

    if (time_ms % (PARAMETERS.PIPE_DISTANCE * PARAMETERS.TICK_INTERVAL) == 0) {
        var minY = PARAMETERS.MIN_PIPE_BUFFER; // Minimum buffer from the top
        var maxY = PARAMETERS.GRID_HEIGHT - PARAMETERS.PIPE_GAP - PARAMETERS.MIN_PIPE_BUFFER; // Max buffer from bottom
        var holeY = minY + (rand() % (maxY - minY + 1));
        pipes.push({ x: PARAMETERS.GRID_WIDTH, holeY: holeY });
    }

    for (var i = 0; i < pipes.length; i++) {
        pipes[i].x -= PARAMETERS.GAME_SPEED;
    }

    while (pipes.length > 0 && pipes[0].x < -PARAMETERS.PIPE_WIDTH) {
        pipes.shift();
        score++;
        draw_updated_score();
    }

    if (birdY >= PARAMETERS.GRID_HEIGHT) {
        game_over();
        return;
    }
    if (check_pipe_collisions()) {
        game_over();
        return;
    }

    draw();
}

function check_pipe_collisions() {
    for (var i = 0; i < pipes.length; i++) {
        var p = pipes[i];

        // Check collision with the bird's 2x2 block
        if (birdX + PARAMETERS.BIRD_SIZE - 1 >= p.x && birdX < (p.x + PARAMETERS.PIPE_WIDTH)) {
            if (birdY > (p.holeY + PARAMETERS.PIPE_GAP) || birdY + PARAMETERS.BIRD_SIZE - 1 < p.holeY) {
                return true;
            }
        }
    }
    return false;
}

function flap() {
    birdVY = PARAMETERS.FLAP_STRENGTH;
}

function game_over() {
    app.clearInterval(interval);
    app.alert("Game Over! Score: " + score + ".\nRefresh or click 'Start game' to restart.");
    game_started = false;
    set_controls_visibility(false);
    this.getField("B_start").hidden = false;
}

function handle_input(event) {
    switch (event.change) {
        case ' ':
        case 'w':
        case 'W':
            if (!game_started)
                game_init();
            else
                flap();
            break;
    }
}

function draw() {
    // Draw the background with occasional sky pixels and grass
    for (var x = 0; x < PARAMETERS.GRID_WIDTH; x++) {
        for (var y = 0; y < PARAMETERS.GRID_HEIGHT; y++) {
            var colorToSet = BACKGROUND_COLOR;

            // Add sky effect at the top row
            if (y === PARAMETERS.GRID_HEIGHT - 1 && Math.random() < PARAMETERS.SKY_PROBABILITY) {
                colorToSet = SKY_COLOR;
            }

            // Add grass effect at the bottom rows
            if (y < 5 && Math.random() < PARAMETERS.GRASS_PROBABILITY) {
                colorToSet = GRASS_COLOR;
            }

            set_pixel(x, y, true, colorToSet);
        }
    }

    // Draw the bird with color
    set_pixel(birdX, Math.floor(birdY), true, BIRD_COLORS.topLeft);              // Top-left
    set_pixel(birdX + 1, Math.floor(birdY), true, BIRD_COLORS.topRight);         // Top-right
    set_pixel(birdX, Math.floor(birdY) + 1, true, BIRD_COLORS.bottomLeft);      // Bottom-left
    set_pixel(birdX + 1, Math.floor(birdY) + 1, true, BIRD_COLORS.bottomRight); // Bottom-right

    // Draw the pipes
    for (var i = 0; i < pipes.length; i++) {
        var p = pipes[i];
        for (var y = 0; y < PARAMETERS.GRID_HEIGHT; y++) {
            if (y < p.holeY || y > (p.holeY + PARAMETERS.PIPE_GAP)) {
                for (var offset = 0; offset < PARAMETERS.PIPE_WIDTH; offset++) {
                    var px = Math.floor(p.x) + offset;
                    if (px >= 0 && px < PARAMETERS.GRID_WIDTH) {
                        set_pixel(px, y, true, color.green);
                    }
                }
            }
        }
    }
}

function set_pixel(x, y, state, color) {
    if (x < 0 || y < 0 || x >= PARAMETERS.GRID_WIDTH || y >= PARAMETERS.GRID_HEIGHT) {
        return;
    }
    var field = pixel_fields[x][PARAMETERS.GRID_HEIGHT - 1 - y];
    field.hidden = !state;
    if (color) {
        field.fillColor = color; // This might not work reliably in all PDF viewers
    }
}

function draw_updated_score() {
    this.getField("Score").value = "Score: " + score;
}

set_controls_visibility(false);

app.execMenuItem("FitPage");