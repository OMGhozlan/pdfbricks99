PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages <<
    /Count 1
    /Kids [
      16 0 R
    ]
    /Type /Pages
  >>
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents << >>
  /CropBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /MediaBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /Parent 7 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj

42 0 obj
<< >>
stream

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

endstream
endobj

18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj

43 0 obj
<< >>
stream



endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.8
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.9 0.9 0.9
    ]
    /BC [
      0.5 0.5 0.5
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
          /JS ###SCRIPT_IDX### R
          /S /JavaScript
        >>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
        /AA <<
                /K <<
                        /JS ###SCRIPT_IDX### R
                        /S /JavaScript
                >>
        >>
        /F 4
        /FT /Tx
        /MK <<
        >>
        /MaxLen 0
        /P 16 0 R
        /Rect [
                ###RECT###
        ]
        /Subtype /Widget
        /T (###NAME###)
        /V (###LABEL###)
        /Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

PX_SIZE = 20
GRID_WIDTH = 15
GRID_HEIGHT = 15
GRID_OFF_X = 100
GRID_OFF_Y = 100
BUTTON_SIZE = 40
BUTTON_SPACING = 10

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
    global fields_text, field_indexes, obj_idx_ctr
    fields_text += field
    field_indexes.append(obj_idx_ctr)
    obj_idx_ctr += 1

# Playing field outline
playing_field = PLAYING_FIELD_OBJ
playing_field = playing_field.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_SIZE} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE}")
add_field(playing_field)

for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        pixel = PIXEL_OBJ
        pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
        pixel = pixel.replace("###RECT###", f"{GRID_OFF_X+x*PX_SIZE} {GRID_OFF_Y+y*PX_SIZE} {GRID_OFF_X+x*PX_SIZE+PX_SIZE} {GRID_OFF_Y+y*PX_SIZE+PX_SIZE}")
        pixel = pixel.replace("###X###", f"{x}")
        pixel = pixel.replace("###Y###", f"{y}")
        add_field(pixel)

def add_button(label, name, x, y, width, height, js_function_name):
    script = STREAM_OBJ;
    script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
    script = script.replace("###CONTENT###", f"{js_function_name}();")
    add_field(script)

    ap_stream = BUTTON_AP_STREAM;
    ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
    ap_stream = ap_stream.replace("###TEXT###", label)
    ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
    ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
    add_field(ap_stream)

    button = BUTTON_OBJ;
    button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
    button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
    button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
    button = button.replace("###LABEL###", label)
    button = button.replace("###NAME###", name if name else f"B_{obj_idx_ctr}")
    button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(button)

def add_text(label, name, x, y, width, height, js_function_name=""):
    
    if js_function_name:
        script = STREAM_OBJ;
        script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
        script = script.replace("###CONTENT###", f"{js_function_name}(event);")
        add_field(script)
        script_idx = f"{obj_idx_ctr-1} 0"
    else:
        script_idx = "43 0"
        
    text = TEXT_OBJ;
    text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
    text = text.replace("###SCRIPT_IDX###", script_idx) # Use the main JS block or the newly created one
    text = text.replace("###LABEL###", label)
    text = text.replace("###NAME###", name)
    text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
    add_field(text)

# Control Buttons
button_panel_x = GRID_OFF_X + GRID_WIDTH * PX_SIZE + 20
button_panel_y = GRID_OFF_Y

add_button("v", "B_up", button_panel_x + BUTTON_SIZE + BUTTON_SPACING, button_panel_y, BUTTON_SIZE, BUTTON_SIZE, "move_up")
add_button("^", "B_down", button_panel_x + BUTTON_SIZE + BUTTON_SPACING, button_panel_y + BUTTON_SIZE + BUTTON_SPACING, BUTTON_SIZE, BUTTON_SIZE, "move_down")
add_button("<", "B_left", button_panel_x, button_panel_y + BUTTON_SIZE + BUTTON_SPACING, BUTTON_SIZE, BUTTON_SIZE, "move_left")
add_button(">", "B_right", button_panel_x + 2 * BUTTON_SIZE + 2 * BUTTON_SPACING, button_panel_y + BUTTON_SIZE + BUTTON_SPACING, BUTTON_SIZE, BUTTON_SIZE, "move_right")

# Keyboard input text box
add_text("", "T_input", button_panel_x, button_panel_y + 2 * (BUTTON_SIZE + BUTTON_SPACING) , BUTTON_SIZE * 4, BUTTON_SIZE, "handle_input")

# Start Button
add_button("Start", "B_start", GRID_OFF_X + (GRID_WIDTH * PX_SIZE) / 2 - 50, GRID_OFF_Y + GRID_HEIGHT * PX_SIZE + 20, 100, 40, "game_init")

# Score Display
add_text("Score: 0", "T_score", GRID_OFF_X, GRID_OFF_Y + GRID_HEIGHT * PX_SIZE + 20, 100, 30)

filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")

pdffile = open("snake_game.pdf", "w", encoding="latin-1")
pdffile.write(filled_pdf)
pdffile.close()

print("snake_game.pdf created successfully.")