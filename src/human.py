from __future__ import annotations
from typing import TYPE_CHECKING
from rubato import Component, Vector, Time, Animation
if TYPE_CHECKING:
    from tiles import Tilemap


class Human(Component):

    def __init__(self, x, y, tilemap: Tilemap, direction: Vector):
        super().__init__()
        self.type = "human"
        self.tilepos = Vector(x, y)
        self.tilemap = tilemap
        self.movement_target = self.tilepos + direction
        self.direction = direction
        self.movement_target_amount = 0
        self.movement_speed = 1
        self.tilemap.set(*self.tilepos.tuple_int(), self)

        self.hunting = False

    def setup(self):
        self.anim = self.gameobj.get(Animation)

    def update(self):
        t = None
        if self.movement_target != self.tilepos:
            self.anim.set_state("move", loop=True)
            if self.movement_target.x < self.tilepos.x:
                self.anim.flipx = True
            elif self.movement_target.x > self.tilepos.x:
                self.anim.flipx = False

            self.movement_target_amount += self.movement_speed * Time.delta_time
            t = self.tilepos.lerp(self.movement_target, self.movement_target_amount)

            if self.movement_target_amount >= 1:
                self.tilepos = self.movement_target.clone()
                self.anim.set_state("idle")
                self.movement_target_amount = 0

                new = self.tilepos + self.direction
                if not self.tilemap.checkbounds(*new):
                    self.direction = self.direction * -1
                    new = self.tilepos + self.direction

                def set_target():
                    self.movement_target = new
                    self.tilemap.set(*self.tilepos.tuple_int(), None)

                if (tile := self.tilemap.get(*self.tilepos.tuple_int())) is not None and tile.type == "frog":
                    print("Frog caught!")

                self.tilemap.set(*self.tilepos.tuple_int(), self)

                if not self.hunting:
                    Time.delayed_call(750, set_target)
                else:
                    set_target()

        if not self.hunting:
            self.see()

        self.gameobj.pos = self.tilemap.to_world(*(t or self.tilepos))

    def hunt(self):
        self.hunting = not self.hunting
        if self.hunting:
            self.movement_speed = 10
            Time.delayed_call(4000, self.hunt)
        else:
            self.movement_speed = 1

    def see(self):
        direction = self.direction.normalized()
        i = 1
        while self.tilemap.checkbounds(*((self.tilepos + (direction * i)).tuple_int())):
            if (tile := self.tilemap.get(*((self.tilepos +
                                            (direction * i)).tuple_int()))) is not None and tile.type == "frog":
                self.hunt()
                return
            i += 1
