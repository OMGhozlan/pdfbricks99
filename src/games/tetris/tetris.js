// Tetris game logic
function setInterval(cb, ms) {
    evalStr = "(" + cb.toString() + ")();";
    return app.setInterval(evalStr, ms);
}

var rand_seed = Date.now() % 2147483647;
function rand() {
    return rand_seed = rand_seed * 16807 % 2147483647;
}

var piece_rotations = [1, 2, 2, 2, 4, 4, 4];
var piece_data = [
    0, 0, -1, 0, -1, -1, 0, -1, 
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

    0, 0, -2, 0, -1, 0, 1, 0,
    0, 0, 0, 1, 0, -1, 0, -2,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

    0, 0, -1, -1, 0, -1, 1, 0, 
    0, 0, 0, 1, 1, 0, 1, -1, 
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

    0, 0, -1, 0, 0, -1, 1, -1, 
    0, 0, 1, 1, 1, 0, 0, -1, 
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

    0, 0, -1, 0, -1, -1, 1, 0, 
    0, 0, 0, 1, 0, -1, 1, -1, 
    0, 0, -1, 0, 1, 0, 1, 1, 
    0, 0, -1, 1, 0, 1, 0, -1, 

    0, 0, -1, 0, 1, 0, 1, -1, 
    0, 0, 0, 1, 0, -1, 1, 1, 
    0, 0, -1, 1, -1, 0, 1, 0, 
    0, 0, 0, 1, 0, -1, -1, -1, 

    0, 0, -1, 0, 0, -1, 1, 0,  
    0, 0, 0, 1, 0, -1, 1, 0, 
    0, 0, -1, 0, 0, 1, 1, 0, 
    0, 0, -1, 0, 0, 1, 0, -1
]

var TICK_INTERVAL = 50;
var GAME_STEP_TIME = 400;

var pixel_fields = [];
var field = [];
var score = 0;
var time_ms = 0;
var last_update = 0;
var interval = 0;

var piece_type = rand() % 7;
var piece_x = 0;
var piece_y = 0;
var piece_rot = 0;

function spawn_new_piece() {
    piece_type = rand() % 7;
    piece_x = 4;
    piece_y = 0;
    piece_rot = 0;
}

function set_controls_visibility(state) {
    this.getField("T_input").hidden = !state;
    this.getField("B_left").hidden = !state;
    this.getField("B_right").hidden = !state;
    this.getField("B_down").hidden = !state;
    this.getField("B_rotate").hidden = !state;
}

function game_init() {
    spawn_new_piece();

    for (var x = 0; x < ###GRID_WIDTH###; ++x) {
        pixel_fields[x] = [];
        field[x] = [];
        for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
            pixel_fields[x][y] = this.getField(`P_${x}_${y}`);
            field[x][y] = 0;
        }
    }

    last_update = time_ms;
    score = 0;

    interval = setInterval(game_tick, TICK_INTERVAL);

    this.getField("B_start").hidden = true;

    set_controls_visibility(true);
}

function game_update() {
    if (time_ms - last_update >= GAME_STEP_TIME) {
        lower_piece();
        last_update = time_ms;
    }
}

function game_over() {
    app.clearInterval(interval);
    app.alert(`Game over! Score: ${score}\nRefresh to restart.`);
}

function rotate_piece() {
    piece_rot++;
    if (piece_rot >= piece_rotations[piece_type]) {
        piece_rot = 0;
    }

    var illegal = false;
    for (var square = 0; square < 4; ++square) {
        var x_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 0];
        var y_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 1];

        var abs_x = piece_x + x_off;
        var abs_y = piece_y + y_off;

        if (abs_x < 0 || abs_y < 0 || abs_x >= ###GRID_WIDTH### || abs_y >= ###GRID_HEIGHT###) {
            illegal = true;
            break;    
        }
    }
    if (illegal) {
        piece_rot--;
        if (piece_rot < 0) {
            piece_rot = piece_rotations[piece_type] - 1;
        }
    }
}

function is_side_collision() {
    for (var square = 0; square < 4; ++square) {
        var x_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 0];
        var y_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 1];

        var abs_x = piece_x + x_off;
        var abs_y = piece_y + y_off;

        if (abs_x < 0 || abs_x >= ###GRID_WIDTH###) {
            return true;
        }

        if (field[abs_x][abs_y]) {
            return true;
        }
    }
    return false;
}

function handle_input(event) {
    switch (event.change) {
        case 'w': rotate_piece(); break;
        case 'a': move_left(); break;
        case 'd': move_right(); break;
        case 's': lower_piece(); break;
    }
}

function move_left() {
    piece_x--;
    if (is_side_collision()) {
        piece_x++;
    }
}

function move_right() {
    piece_x++;
    if (is_side_collision()) {
        piece_x--;
    }
}

function check_for_filled_lines() {
    for (var row = 0; row < ###GRID_HEIGHT###; ++row) {
        var fill_count = 0;
        for (var column = 0; column < ###GRID_WIDTH###; ++column) {
            fill_count += field[column][row];
        }
        if (fill_count == ###GRID_WIDTH###) {
            score++;
            draw_updated_score();

            for (var row2 = row; row2 > 0; row2--) {
                for (var column2 = 0; column2 < ###GRID_WIDTH###; ++column2) {
                    field[column2][row2] = field[column2][row2-1];
                }
            }
        }
    }
}

function lower_piece() {
    piece_y++;

    var collision = false;
    for (var square = 0; square < 4; ++square) {
        var x_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 0];
        var y_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 1];

        var abs_x = piece_x + x_off;
        var abs_y = piece_y + y_off;

        if (abs_x < 0 || abs_y < 0 || abs_x >= ###GRID_WIDTH### || abs_y >= ###GRID_HEIGHT###) {
            collision = true;
            break;    
        }

        if (abs_y >= ###GRID_HEIGHT### || field[abs_x][abs_y]) {
            collision = true;
            break;
        }
    }

    if (collision) {
        if (piece_y == 1) {
            game_over();
            return;
        }

        piece_y--;
        for (var square = 0; square < 4; ++square) {
            var x_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 0];
            var y_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 1];

            var abs_x = piece_x + x_off;
            var abs_y = piece_y + y_off;

            if (abs_x < 0 || abs_y < 0 || abs_x >= ###GRID_WIDTH### || abs_y >= ###GRID_HEIGHT###) {
                continue;
            }

            field[abs_x][abs_y] = true;
        }

        check_for_filled_lines();
        spawn_new_piece();
    }
}

function draw_updated_score() {
    this.getField("T_score").value = `Score: ${score}`;
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

function draw_current_piece() {
    for (var square = 0; square < 4; ++square) {
        var x_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 0];
        var y_off = piece_data[piece_type * 32 + piece_rot * 8 + square * 2 + 1];

        var abs_x = piece_x + x_off;
        var abs_y = piece_y + y_off;

        set_pixel(abs_x, abs_y, 1);
    }
}

function draw() {
    draw_field();
    draw_current_piece();
}

function game_tick() {
    time_ms += TICK_INTERVAL;
    game_update();
    draw();
}

set_controls_visibility(false);
app.execMenuItem("FitPage");