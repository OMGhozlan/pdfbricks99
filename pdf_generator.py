import os
from utils.prettylogger import setup_logging

# Rule: Use descriptive variable names
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
###GAME_SCRIPT###
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
      ###COLOR###
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

PAGE_TEMPLATE = """
%% Page ###PAGE_NUMBER###
###PAGE_IDX### 0 obj
<<
  /Annots ###ANNOT_IDX### 0 R
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

###ANNOT_IDX### 0 obj
[
  ###FIELD_LIST###
]
endobj
"""

# Rule: Use dictionaries for modular and scalable design
GAME_CONFIGS = {
    "tetris": {
        "script_path": "src/games/tetris/tetris.js",
        "PX_SIZE": 20,
        "GRID_WIDTH": 10,
        "GRID_HEIGHT": 20,
        "GRID_OFF_X": 200,
        "GRID_OFF_Y": 350,
        "fields_text": "",
        "field_indexes": [],
        "obj_idx_ctr": 50
    },
    "shooter": {
        "script_path": "src/games/shoot/shooter.js",
        "PX_SIZE": 20,
        "GRID_WIDTH": 10,
        "GRID_HEIGHT": 20,
        "GRID_OFF_X": 200,
        "GRID_OFF_Y": 350,
        "fields_text": "",
        "field_indexes": [],
        "obj_idx_ctr": 50
    }
    # Add other games here similarly
}

def generate_pdf(file_path, games):
    """
    Generates a PDF file containing the specified games.
    
    Args:
        file_path (str): The path where the PDF will be saved.
        games (list): A list of game configurations to include in the PDF.
    """
    log.info("Generating PDF...")
    pages_content = ""
    page_references = []
    page_count = 0    
    for game in games:
      log.warning(game)
      filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", generate_fields(game))
      filled_pdf = filled_pdf.replace("###GAME_SCRIPT###", generate_script(games))    
      filled_pdf = filled_pdf.replace("###FIELD_LIST###", generate_field_list(GAME_CONFIGS[game['value']]))
      # pages_content += filled_pdf
      
    # pdf_content = PAGE_TEMPLATE.replace("###PAGE_COUNT###", str(page_count))
    # pdf_content = pdf_content.replace("###PAGE_REFERENCES###", "\n".join(page_references))
    # pdf_content = pdf_content.replace("###PAGES###", pages_content)
    pdf_content = filled_pdf

    with open(file_path, 'wb') as pdf_file:
        pdf_file.write(pdf_content.encode('utf-8'))
    log.info(f"PDF generated and saved to {file_path}")

def generate_field_list(config):
    """
    Generates a list of fields for the PDF based on the provided games.
    
    Args:
        games (list): A list of game configurations.
    
    Returns:
        str: A string representation of the field list.
    """
    log.debug("Generating field list...")
    return " ".join([f"{i} 0 R" for i in config.get('field_indexes', [])])

def generate_fields(game):
    """
    Generates the fields section of the PDF based on the provided games.
    
    Args:
        games (list): A list of game configurations.
    
    Returns:
        str: A string representation of the fields section.
    """
    log.debug("Generating fields...")
    fields_text = ""

    log.warning(game)
    game_name = game["name"].lower()
    if game_name in GAME_CONFIGS:
      game_config = GAME_CONFIGS[game_name]
      generate_game_fields(game_config)
      fields_text += game_config['fields_text']
    else:
        log.error(f"Field generator for game {game_name} not found.")

    return fields_text

def generate_game_fields(config):
    """
    Generates the fields for a game based on the provided configuration.
    
    Args:
        config (dict): Configuration dictionary for the game.
    
    Returns:
        str: A string representation of the game fields.
    """
    log.debug(f"Generating fields for game with config: {config}")

    def add_field(field, config):
        config['fields_text'] += field
        config['field_indexes'].append(config['obj_idx_ctr'])
        config['obj_idx_ctr'] += 1

    # Playing field outline
    playing_field = PLAYING_FIELD_OBJ
    playing_field = playing_field.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
    playing_field = playing_field.replace("###RECT###", f"{config['GRID_OFF_X']} {config['GRID_OFF_Y']} {config['GRID_OFF_X']+config['GRID_WIDTH']*config['PX_SIZE']} {config['GRID_OFF_Y']+config['GRID_HEIGHT']*config['PX_SIZE']}")
    add_field(playing_field, config)

    for x in range(config['GRID_WIDTH']):
        for y in range(config['GRID_HEIGHT']):
            # Build object
            pixel = PIXEL_OBJ
            pixel = pixel.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
            c = [0, 0, 0]
            pixel = pixel.replace("###COLOR###", f"{c[0]} {c[1]} {c[2]}")
            pixel = pixel.replace("###RECT###", f"{config['GRID_OFF_X']+x*config['PX_SIZE']} {config['GRID_OFF_Y']+y*config['PX_SIZE']} {config['GRID_OFF_X']+x*config['PX_SIZE']+config['PX_SIZE']} {config['GRID_OFF_Y']+y*config['PX_SIZE']+config['PX_SIZE']}")
            pixel = pixel.replace("###X###", f"{x}")
            pixel = pixel.replace("###Y###", f"{y}")

            add_field(pixel, config)

    def add_button(config, label, name, x, y, width, height, js):
        script = STREAM_OBJ
        script = script.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
        script = script.replace("###CONTENT###", js)
        add_field(script, config)

        ap_stream = BUTTON_AP_STREAM
        ap_stream = ap_stream.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
        ap_stream = ap_stream.replace("###TEXT###", label)
        ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
        ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
        add_field(ap_stream, config)

        button = BUTTON_OBJ
        button = button.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
        button = button.replace("###SCRIPT_IDX###", f"{config['obj_idx_ctr']-2} 0")
        button = button.replace("###AP_IDX###", f"{config['obj_idx_ctr']-1} 0")
        button = button.replace("###NAME###", name if name else f"B_{config['obj_idx_ctr']}")
        button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
        add_field(button, config)

    def add_text(config, label, name, x, y, width, height, js):
        script = STREAM_OBJ
        script = script.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
        script = script.replace("###CONTENT###", js)
        add_field(script, config)

        text = TEXT_OBJ
        text = text.replace("###IDX###", f"{config['obj_idx_ctr']} 0")
        text = text.replace("###SCRIPT_IDX###", f"{config['obj_idx_ctr']-1} 0")
        text = text.replace("###LABEL###", label)
        text = text.replace("###NAME###", name)
        text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
        add_field(text, config)

    add_button(config, "<", "B_left", config['GRID_OFF_X'] + 0, config['GRID_OFF_Y'] - 70, 50, 50, "move_left();")
    add_button(config, ">", "B_right", config['GRID_OFF_X'] + 60, config['GRID_OFF_Y'] - 70, 50, 50, "move_right();")
    add_button(config, "\\\\/", "B_down", config['GRID_OFF_X'] + 30, config['GRID_OFF_Y'] - 130, 50, 50, "lower_piece();")
    add_button(config, "SPIN", "B_rotate", config['GRID_OFF_X'] + 140, config['GRID_OFF_Y'] - 70, 50, 50, "rotate_piece();")
    add_button(config, "SPIN", "B_space", config['GRID_OFF_X'] + 200, config['GRID_OFF_Y'] - 70, 50, 50, "rotate_piece();")

    add_button(config, "Start game", "B_start", config['GRID_OFF_X'] + (config['GRID_WIDTH']*config['PX_SIZE'])/2-50, config['GRID_OFF_Y'] + (config['GRID_HEIGHT']*config['PX_SIZE'])/2-50, 100, 100, "game_init();")

    add_text(config, "Type here for keyboard controls (WASD)", "T_input", config['GRID_OFF_X'] + 0, config['GRID_OFF_Y'] - 200, config['GRID_WIDTH']*config['PX_SIZE'], 50, "handle_input(event);")

    add_text(config, "Score: 0", "T_score", config['GRID_OFF_X'] + config['GRID_WIDTH']*config['PX_SIZE']+10, config['GRID_OFF_Y'] + config['GRID_HEIGHT']*config['PX_SIZE']-50, 100, 50, "")


def generate_script(games):
    """
    Generates the JavaScript section of the PDF based on the provided games.
    
    Args:
        games (list): A list of game configurations.
    
    Returns:
        str: A string representation of the JavaScript section.
    """
    log.debug("Generating script...")
    script = ""
    src_dir = os.path.join(os.getcwd(), "src")
    for game in games:
        game_name = game["name"].lower()
        if game_name in GAME_CONFIGS:
            game_file_path = GAME_CONFIGS[game_name]["script_path"]
            try:
                with open(game_file_path, "r") as file:
                    game_script = file.read()
                    game_script = game_script.replace("###GRID_WIDTH###", f"{GAME_CONFIGS[game_name]['GRID_WIDTH']}")
                    game_script = game_script.replace("###GRID_HEIGHT###", f"{GAME_CONFIGS[game_name]['GRID_HEIGHT']}")
                    script += game_script
            except FileNotFoundError:
                log.error(f"Error: {game_file_path} not found.")
        else:
            log.error(f"Script path for game {game_name} not found.")
    return script

if __name__ == "__main__":
    log = setup_logging(debug=True)
    games = [
        {"name": "Tetris", "value": "tetris"},
        # {"name": "Shoot", "value": "shoot"}
    ]
    generate_pdf("game.pdf", games)