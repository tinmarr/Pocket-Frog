from __future__ import annotations
from typing import TYPE_CHECKING
from rubato import Vector, GameObject, Raster, Surface

if TYPE_CHECKING:
    from .frog import Frog
    from .human import Human


class Tilemap:

    def __init__(self, w, h, tilesize):
        self.w = w
        self.h = h
        self.tilesize = tilesize
        self.tiles: list[list[None | Frog | Human]] = [[None for _ in range(w)] for __ in range(h)]

    def set(self, x, y, obj):
        if self.checkbounds(x, y):
            self.tiles[y][x] = obj

    def get(self, x, y):
        if self.checkbounds(x, y):
            return self.tiles[y][x]
        return None

    def checkbounds(self, x, y):
        return x >= 0 and x < self.w and y >= 0 and y < self.h

    def to_world(self, x, y):
        return Vector(x * self.tilesize, y * self.tilesize) + (self.tilesize // 2)

    def to_tile(self, x, y):
        return Vector(x // self.tilesize, y // self.tilesize)

    def make_go(self, ground: Surface):
        go = GameObject("Tilemap")
        for y in range(self.h):
            for x in range(self.w):
                r = Raster(offset=self.to_world(x, y))
                r.surf = ground.clone()
                go.add(r)
        return go
