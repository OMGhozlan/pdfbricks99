 
// Hacky wrapper to work with a callback instead of a string
function setInterval(cb, ms) {
    evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

// https://gist.github.com/blixt/f17b47c62508be59987b
var rand_seed = Date.now() % 2147483647;
function rand() {
    return rand_seed = rand_seed * 16807 % 2147483647;
}

var TICK_INTERVAL = 230; // Adjust for game speed
var GRID_WIDTH = ###GRID_WIDTH###;
var GRID_HEIGHT = ###GRID_HEIGHT###;

// Game state
var snake = [];
var food = {};
var direction = 'right';
var score = 0;
var interval;
var game_over_flag = false;

var pixel_fields = [];

function set_controls_visibility(state) {
this.getField("B_up").hidden = !state;
this.getField("B_down").hidden = !state;
this.getField("B_left").hidden = !state;
this.getField("B_right").hidden = !state;
this.getField("T_input").hidden = !state;
}

function game_init() {
game_over_flag = false;
score = 0;
draw_updated_score();

snake = [{x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2)}]; // Initial snake position
direction = 'right';
generate_food();

if (interval) {
    app.clearInterval(interval);
}
interval = setInterval(game_tick, TICK_INTERVAL);

this.getField("B_start").hidden = true;
set_controls_visibility(true); // Controls are now visible from the start
}

function generate_food() {
do {
    food = {x: Math.floor(rand() % GRID_WIDTH), y: Math.floor(rand() % GRID_HEIGHT)};
} while (is_on_snake(food));
}

function is_on_snake(pos) {
for (var i = 0; i < snake.length; i++) {
    if (snake[i].x === pos.x && snake[i].y === pos.y) {
        return true;
    }
}
return false;
}

function game_tick() {
if (game_over_flag) return;
move_snake();
check_collisions();
draw();
}

function move_snake() {
var head = {x: snake[0].x, y: snake[0].y};

switch (direction) {
    case 'up': head.y--; break;
    case 'down': head.y++; break;
    case 'left': head.x--; break;
    case 'right': head.x++; break;
}

snake.unshift(head); // Add new head

if (head.x === food.x && head.y === food.y) {
    score++;
    draw_updated_score();
    generate_food();
} else {
    snake.pop(); // Remove tail if no food eaten
}
}

function check_collisions() {
var head = snake[0];

// Wall collision
if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
    game_over();
    return;
}

// Self collision
for (var i = 1; i < snake.length; i++) {
    if (head.x === snake[i].x && head.y === snake[i].y) {
        game_over();
        return;
    }
}
}

function game_over() {
game_over_flag = true;
app.clearInterval(interval);
app.alert('Game Over! Score: ' + score + '\\nRefresh to restart.');
}

function set_pixel(x, y, state, color) {
if (x < 0 || y < 0 || x >= GRID_WIDTH || y >= GRID_HEIGHT) {
    return;
}
var field = pixel_fields[x][GRID_HEIGHT - 1 - y];
field.hidden = !state;
if (color) {
    field.fillColor = color; // This might not work reliably in all PDF viewers
}
}

function draw() {
// Clear the grid
for (var x = 0; x < GRID_WIDTH; x++) {
    for (var y = 0; y < GRID_HEIGHT; y++) {
        set_pixel(x, y, false);
    }
}

// Draw the snake
for (var i = 0; i < snake.length; i++) {
    set_pixel(snake[i].x, snake[i].y, true, color.red);
}

// Draw the food
set_pixel(food.x, food.y, true, color.green);
}

function change_direction(newDirection) {
if (game_over_flag) return;
if (newDirection === 'up' && direction !== 'down') {
    direction = 'up';
} else if (newDirection === 'down' && direction !== 'up') {
    direction = 'down';
} else if (newDirection === 'left' && direction !== 'right') {
    direction = 'left';
} else if (newDirection === 'right' && direction !== 'left') {
    direction = 'right';
}
}

function draw_updated_score() {
this.getField("T_score").value = 'Score: ' + score;
}

// Input handlers
function move_up() { change_direction('down'); }
function move_down() { change_direction('up'); }
function move_left() { change_direction('left'); }
function move_right() { change_direction('right'); }

function handle_input(event) {
switch (event.change) {
    case 'w': change_direction('up'); break;
    case 'a': change_direction('left'); break;
    case 's': change_direction('down'); break;
    case 'd': change_direction('right'); break;
}
}

// Initialization (after fields are created)
for (var x = 0; x < GRID_WIDTH; ++x) {
pixel_fields[x] = [];
for (var y = 0; y < GRID_HEIGHT; ++y) {
    pixel_fields[x][y] = this.getField('P_' + x + '_' + y);
}
}

set_controls_visibility(true); // Make controls visible from the start
app.execMenuItem('FitPage');

