from __future__ import annotations
from typing import TYPE_CHECKING
from rubato import Component, Radio, Animation, Vector, Time, ScheduledTask
from .human import Human

if TYPE_CHECKING:
    from tiles import Tilemap


class Frog(Component):

    def __init__(self, x, y, tilemap: Tilemap):
        super().__init__()
        self.type = "frog"
        self.tilepos = Vector(x, y)
        self.tilemap = tilemap
        self.movement_target_amount = 1
        self.movement_target = Vector(x, y)
        self.movement_speed = 5

        self.human: Human | None = None

        self.tilemap.set(*self.tilepos.tuple_int(), self)
        Radio.listen("KEYDOWN", self.handle_keydown)

    def setup(self):
        self.anim = self.gameobj.get(Animation)

    def handle_keydown(self, info):
        new = self.tilepos.clone()
        k = info["key"]
        if k == "w" or k == "up":
            new.y -= 1
        elif k == "a" or k == "left":
            new.x -= 1
        elif k == "s" or k == "down":
            new.y += 1
        elif k == "d" or k == "right":
            new.x += 1

        if self.tilepos != new and self.tilemap.checkbounds(*new) and self.movement_target_amount == 1 and \
                (self.human is None or self.human.movement_target_amount == 0):
            self.movement_target = new
            self.movement_target_amount = 0
            self.tilemap.set(*self.tilepos.tuple_int(), None)
            self.human = None

    def update(self):
        t = None
        if self.movement_target != self.tilepos:
            self.anim.fps = 8
            self.anim.set_state("jumping", freeze=1)
            if self.movement_target.x < self.tilepos.x:
                self.anim.flipx = True
            elif self.movement_target.x > self.tilepos.x:
                self.anim.flipx = False

            self.movement_target_amount += self.movement_speed * Time.delta_time
            t = self.tilepos.lerp(self.movement_target, self.movement_target_amount)

            if self.movement_target_amount >= 1:
                self.tilepos = self.movement_target.clone()

                tile = self.tilemap.get(*self.tilepos.tuple_int())
                if tile is not None and tile.type == "human":
                    self.human = tile  # type: ignore
                    self.shift_up()
                else:
                    self.shift_down()

                self.anim.fps = 1
                self.anim.set_state("blinking", loop=True)
                self.movement_target_amount = 1
                self.tilemap.set(*self.tilepos.tuple_int(), self)

        if self.human is not None:
            self.gameobj.pos = self.human.gameobj.pos.clone()
            self.tilepos = self.human.tilepos.clone()
            self.movement_target = self.tilepos.clone()
        else:
            self.gameobj.pos = self.tilemap.to_world(*(t or self.tilepos))

    def shift_up(self):
        if self.anim.offset.y != -32:
            self.anim.offset.y -= 1
            Time.delayed_call(5, self.shift_up)

    def shift_down(self):
        if self.anim.offset.y != 0:
            self.anim.offset.y += 1
            Time.delayed_call(5, self.shift_down)
