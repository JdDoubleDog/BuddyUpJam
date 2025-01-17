from engine import * 
from scripts import *

def init():
    global game_context, scene, timer
    set_path("data/images/")
    game_context = GameContext((1280, 720), pygame.SCALED, vsync=True)
    game_context.zoom_enabled = True
    game_context.zoom = game_context.get_display_size()[1]/220
    game_context.tile_size = 32
    timer = Timer(game_context)
    timer["anim"] = 100000
    scene = Scene(game_context)
    load_assets()
    create_level()

def create_level():
    level = load_tiled("data/maps/test.tmx", "data/tilesets/main.tsx", 2)
    for i, pattern in enumerate(level['pattern'].data):
        if pattern["data"] != None:
            tilemap = Tilemap(game_context, 32, i)
            tilemap.tileset = game_context.assets["tileset"]
            tilemap.tiles_data = level["tileset_data"]
            tilemap.place_pattern(pattern["data"], (0,0))    
            scene.link(tilemap) 
        for obj in pattern["meta_data"]["objects"]:
            if isinstance(obj, pygame.Rect):
                scene.link(RectObject(game_context, obj, i, collide=True))
            elif obj["id"] == 208:
                scene.link(Player(game_context, [obj["pos"][0]*2, obj["pos"][1]*2 - 32]), Shadow(game_context, 1))      
            else:
                scene.link(OffGridObject(game_context, (obj["pos"][0]*2, obj["pos"][1]*2 - 32), obj["id"], "tileset", i-4))
     

def load_assets():
    game_context.assets = {
        "player_sprite" : scale_animations(load_animation("sprites/player.png", (16, 16), 4), (32, 32)),
        "tileset" : scale_image_list(load_sprite('tilesets/tileset.png', (16, 16)), (32, 32)),
        "shadow" : pygame.transform.scale(load_image("sprites/shadow.png"), (32, 32)),
        "blue_curse" : scale_animations(load_animation("objects/curses/blue_curse.png", (32, 32), 11), (64, 64))
    }

def zoom(event):
    scale = True
    if game_context.zoom <= 1*game_context.get_display_size()[1]/640 and event.y <= 0:
        scale = False
    if game_context.zoom >= 8*game_context.get_display_size()[1]/640 and event.y >= 0:
        scale = False
    if scale:
        game_context.zoom *= 1 + event.y/70

def check_player_out_of_bounds(playerObject):
    x = playerObject.rect().left
    y = playerObject.rect().top
    #game_context.set_caption("x: "+str(x)+" y: "+str(y))

def update_window_title(playerObject):
    if playerObject is None:
        game_context.set_caption("FPS : "+str(int(game_context.get_fps())))
    else:
        x = playerObject.rect().left
        y = playerObject.rect().top
        game_context.set_caption("FPS : "+str(int(game_context.get_fps()))+"x: "+str(x)+" y: "+str(y))
    

def game_loop():
    game_context.rendered_objects = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_context.quit()
        if event.type == pygame.MOUSEWHEEL and game_context.zoom_enabled:
            zoom(event)
    game_context.rendering_surface.fill((0,0,0))
    scene.update()
    player = scene.get_objects_by_tags("@Player")[0]
    update_window_title(player)
    game_context.scroll(player.rect().center, 15)
    check_player_out_of_bounds(player)
    timer.update()

init()
game_context.run(game_loop)

