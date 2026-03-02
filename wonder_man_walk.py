import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Wonder Man")

        # Position
        self.x = 80
        self.y = 85
        self.speed = 0.4
        self.vx = 0

        # Vertical movement
        self.vy = 0
        self.gravity = 0.5
        self.jump_strength = -5
        self.ground_y = 85
        self.on_ground = True

        # Borders
        self.min_x = 6
        self.max_x = 160 - 6

        # Facing
        self.facing = 1

        # Punch
        self.punch_timer = 0
        self.punch_length = 6
        self.punch_duration = 4

        # Animation
        self.walk_frame = 0
        self.anim_speed = 6

        # Page system
        self.page = 0

        pyxel.run(self.update, self.draw)

    # ---------- WORLD SYSTEM ----------
    def current_world(self):
        return self.page // 5   # 0=normal, 1=rain, 2=desert

    # ---------- UPDATE ----------
    def update(self):
        world = self.current_world()
        moving = False

        # Movement power by world
        if world == 2:
            move_power = self.speed * 0.6
        else:
            move_power = self.speed

        if pyxel.btn(pyxel.KEY_LEFT):
            self.vx -= move_power
            self.facing = -1
            moving = True

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.vx += move_power
            self.facing = 1
            moving = True

        # Friction by world
        if world == 1:
            friction = 0.88
        elif world == 2:
            friction = 0.70
        else:
            friction = 0.75

        self.vx *= friction
        self.x += self.vx

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

        # Page switch
        if self.x >= self.max_x:
            self.page += 1
            self.x = self.min_x + 10
            self.vx = 0

        if self.x <= self.min_x and self.page > 0:
            self.page -= 1
            self.x = self.max_x - 10
            self.vx = 0

    # ---------- DRAW ----------
    def draw(self):
        pyxel.cls(0)
        world = self.current_world()

        # SKY
        if world == 1:
            pyxel.rect(0, 0, 160, 80, 5)
        elif world == 2:
            pyxel.rect(0, 0, 160, 80, 4)
        else:
            pyxel.rect(0, 0, 160, 80, 6)

        # GROUND
        if world == 2:
            pyxel.rect(0, 80, 160, 40, 10)  # sand
            pyxel.rect(0, 96, 160, 8, 4)    # brown path
        else:
            pyxel.rect(0, 80, 160, 40, 11)  # grass
            pyxel.rect(0, 96, 160, 8, 10)   # path
            for i in range(0, 160, 16):
                pyxel.line(i, 96, i, 103, 0)

        # SUN
        if world == 0:
            pyxel.circ(140, 20, 10, 10)
            pyxel.circ(140, 20, 12, 10)
        elif world == 2:
            pyxel.circ(140, 20, 10, 9)
            pyxel.circ(140, 20, 12, 9)

        # WEATHER
        if world == 1:  # rain
            for i in range(0, 160, 8):
                y = (pyxel.frame_count * 3 + i) % 80
                pyxel.line(i, y, i + 2, y + 6, 7)

        if world == 2:  # sandstorm
            for i in range(0, 160, 6):
                x = (160 - (pyxel.frame_count * 2 + i * 3)) % 160
                y = (i * 7 + pyxel.frame_count) % 80
                pyxel.pset(x, y, 10)

        # TREES / CACTI
        if world == 2:
            if self.page % 2 == 1:
                self.draw_cactus_big(40, 80)
                self.draw_cactus_tall(110, 80)
            else:
                self.draw_cactus_tall(75, 80)
        else:
            if self.page % 2 == 1:
                self.draw_tree(30, 70)
                self.draw_tree(120, 70)
            else:
                self.draw_tree(78, 70)

        # CHARACTER
        x = self.x
        y = self.y

        pyxel.line(x, y + 2, x, y + 8, 8)
        pyxel.circ(x, y, 2, 4)
        pyxel.pset(x + self.facing, y - 1, 0)

        walking_phase = (self.walk_frame // self.anim_speed) % 2

        # ARMS
        if self.punch_timer > 0:
            pyxel.line(x, y + 4, x + self.facing * 6, y + 4, 8)
        else:
            if walking_phase == 0:
                pyxel.line(x, y + 4, x + self.facing * 3, y + 6, 8)
                pyxel.line(x, y + 4, x - self.facing * 2, y + 3, 8)
            else:
                pyxel.line(x, y + 4, x + self.facing * 2, y + 3, 8)
                pyxel.line(x, y + 4, x - self.facing * 3, y + 6, 8)

        # LEGS
        if walking_phase == 0:
            pyxel.line(x, y + 8, x - 2, y + 12, 1)
            pyxel.line(x, y + 8, x + 2, y + 12, 1)
        else:
            pyxel.line(x, y + 8, x - 3, y + 12, 1)
            pyxel.line(x, y + 8, x + 3, y + 12, 1)

        pyxel.text(5, 5, f"STAGE {self.page + 1}", 0)

    # ---------- HELPERS ----------
    def draw_tree(self, x, y):
        pyxel.rect(x, y, 4, 10, 4)
        pyxel.circ(x + 2, y - 4, 6, 3)

    # Big fork cactus (wide, chunky)
    def draw_cactus_big(self, x, y):
        pyxel.rect(x, y - 20, 5, 20, 3)
        # LEFT ARM (higher)
        pyxel.rect(x - 4, y - 15, 4, 4, 3)
        pyxel.rect(x - 4, y - 19, 3, 4, 3)
        # RIGHT ARM (lower + longer → asymmetry)
        pyxel.rect(x + 5, y - 10, 4, 4, 3)
        pyxel.rect(x + 7, y - 14, 3, 4, 3)
        # texture dots
        pyxel.pset(x + 2, y - 17, 11)
        pyxel.pset(x - 3, y - 13, 11)
        pyxel.pset(x + 8, y - 9, 11)

    # Tall fork cactus (thinner version)
    def draw_cactus_tall(self, x, y):
        pyxel.rect(x, y - 22, 3, 22, 3)
        # LEFT ARM (lower)
        pyxel.rect(x - 3, y - 11, 3, 3, 3)
        pyxel.rect(x - 3, y - 15, 2, 4, 3)
        # RIGHT ARM (higher)
        pyxel.rect(x + 3, y - 16, 3, 3, 3)
        pyxel.rect(x + 5, y - 20, 2, 4, 3)
        # texture dots
        pyxel.pset(x + 1, y - 19, 11)
        pyxel.pset(x - 2, y - 10, 11)
        pyxel.pset(x + 4, y - 14, 11)


App()