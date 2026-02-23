import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Wonder Man")

        # Position
        self.x = 80
        self.y = 74
        self.speed = 2

        # Vertical movement
        self.vy = 0
        self.gravity = 0.5
        self.jump_strength = -5
        self.ground_y = 74
        self.on_ground = True

        # Borders
        self.min_x = 6
        self.max_x = 160 - 6

        # Facing direction
        self.facing = 1

        # Punch
        self.punch_timer = 0
        self.punch_length = 10
        self.punch_duration = 4

        # Walking animation
        self.walk_frame = 0
        self.anim_speed = 6

        # Page system
        self.page = 0

        pyxel.run(self.update, self.draw)

    def update(self):

        moving = False

        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
            self.facing = -1
            moving = True

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
            self.facing = 1
            moving = True

        # Clamp inside screen
        self.x = max(self.min_x, min(self.x, self.max_x))

        # Walking animation
        if moving and self.on_ground:
            self.walk_frame += 1
        else:
            self.walk_frame = 0

        # Jump
        if pyxel.btnp(pyxel.KEY_SPACE) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False

        # Gravity
        self.vy += self.gravity
        self.y += self.vy

        if self.y > self.ground_y:
            self.y = self.ground_y
            self.vy = 0
            self.on_ground = True

        # Punch
        if pyxel.btnp(pyxel.KEY_Z):
            self.punch_timer = self.punch_duration

        if self.punch_timer > 0:
            self.punch_timer -= 1

        # ----- PAGE SWITCHING -----
        if self.x >= self.max_x:
            self.page += 1
            self.x = self.min_x + 10   # spawn clearly inside next screen

        if self.x <= self.min_x and self.page > 0:
            self.page -= 1
            self.x = self.max_x - 10   # spawn clearly inside previous screen

    def draw(self):
        pyxel.cls(0)

        # Sky
        pyxel.rect(0, 0, 160, 80, 6)

        # Grass
        pyxel.rect(0, 80, 160, 40, 11)

        # Path
        pyxel.rect(0, 96, 160, 8, 10)

        for i in range(0, 160, 16):
            pyxel.line(i, 96, i, 103, 0)

        # ---- SUN ----
        pyxel.circ(140, 20, 10, 10)
        pyxel.circ(140, 20, 12, 9)

        # ---- BACKGROUND BY ODD / EVEN PAGE ----
        if self.page % 2 == 1:
            # ODD pages → TWO TREES

            # Tree left
            pyxel.rect(30, 70, 4, 10, 4)
            pyxel.circ(32, 66, 6, 3)
            pyxel.circ(28, 68, 5, 3)
            pyxel.circ(36, 68, 5, 3)

            # Tree right
            pyxel.rect(120, 70, 4, 10, 4)
            pyxel.circ(122, 66, 6, 3)
            pyxel.circ(118, 68, 5, 3)
            pyxel.circ(126, 68, 5, 3)

        else:
            # EVEN pages → ONE CENTER TREE

            pyxel.rect(78, 70, 4, 10, 4)
            pyxel.circ(80, 66, 6, 3)
            pyxel.circ(76, 68, 5, 3)
            pyxel.circ(84, 68, 5, 3)

        x = self.x
        y = self.y

        # Body
        pyxel.line(x, y + 4, x, y + 14, 8)

        # Head
        pyxel.circ(x, y, 4, 4)

        # Face
        pyxel.pset(x + self.facing * 1, y - 1, 0)
        mouth_start = x + self.facing * 1
        mouth_end = mouth_start + self.facing * 2
        pyxel.line(mouth_start, y + 1, mouth_end, y + 1, 0)

        walking_phase = (self.walk_frame // self.anim_speed) % 2

        # Arms
        if self.punch_timer > 0:
            pyxel.line(x, y + 8, x + self.facing * self.punch_length, y + 8, 8)
            pyxel.line(x, y + 8, x - self.facing * 6, y + 12, 8)
        else:
            if walking_phase == 0:
                pyxel.line(x, y + 8, x + self.facing * 6, y + 12, 8)
                pyxel.line(x, y + 8, x - self.facing * 4, y + 6, 8)
            else:
                pyxel.line(x, y + 8, x + self.facing * 4, y + 6, 8)
                pyxel.line(x, y + 8, x - self.facing * 6, y + 12, 8)

        # Legs
        if walking_phase == 0:
            pyxel.line(x, y + 14, x - 4, y + 22, 1)
            pyxel.line(x, y + 14, x + 4, y + 22, 1)
        else:
            pyxel.line(x, y + 14, x - 6, y + 22, 1)
            pyxel.line(x, y + 14, x + 6, y + 22, 1)

        # Page label
        pyxel.text(5, 5, f"STAGE {self.page}", 0)


App()