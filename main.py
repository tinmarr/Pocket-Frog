from rubato import *  # type: ignore
from random import randint
from src.human import *
from src.tiles import *
from src.frog import *

init(res=(96 * 11, 96 * 11), window_size=(2000, 2000), name="Pocket Frog")
mainScene = Scene("Main")

tilemap = Tilemap(11, 11, 96)
surf = Surface(96, 96)
surf.draw_rect((0, 0), (96, 96), fill=Color(0, 255, 0, 191))
mainScene.add(tilemap.make_go(surf))

frog_go = GameObject("Frog")

frog_sheet = Spritesheet("assets/Frog.png", (16, 16))
frog_anim = Animation(fps=1, scale=(3, 3), offset=(0, -32))
frog_anim.add_spritesheet("blinking", frog_sheet, (0, 1), (1, 1))
frog_anim.add_spritesheet("jumping", frog_sheet, (0, 0), (1, 0))
frog_go.add(frog_anim)

frog_comp = Frog(0, 0, tilemap)
frog_go.add(frog_comp)

human_go = GameObject("Human")

human_sheet = Spritesheet("assets/Man.png", (32, 32))
human_anim = Animation(fps=8, scale=(3, 3))
human_anim.add_spritesheet("idle", human_sheet)
human_anim.add_spritesheet("move", human_sheet, (0, 0), (4, 0))
human_go.add(human_anim)

human_comp = Human(0, 0, tilemap, Vector(1, 0))
human_go.add(human_comp)

frog_comp.human = human_comp

l = []
for i in range(10):
    hg = GameObject("Human")
    l.append(hg)

    ha = Animation(fps=8, scale=(3, 3))
    ha.add_spritesheet("idle", human_sheet)
    ha.add_spritesheet("move", human_sheet, (0, 0), (4, 0))
    hg.add(ha)

    human_comp = Human(randint(0, 10), randint(0, 10), tilemap, Vector(randint(-1, 1), randint(-1, 1)))
    hg.add(human_comp)

mainScene.add(frog_go, human_go, *l)

begin()
