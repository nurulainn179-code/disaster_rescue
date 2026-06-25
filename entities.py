import pygame
import math
import os

# ── Colours ─────────────────────────────────────────────────────
RIVER_BLUE    = ( 30, 120, 200)
DEEP_BLUE     = ( 20,  80, 160)
WAVE_BLUE     = ( 60, 160, 230)
LAND_GREEN    = ( 80, 160,  60)
DARK_GREEN    = ( 40,  90,  30)
SAND          = (210, 180, 110)
RED           = (200,  40,  40)
DARK_RED      = (140,  20,  20)
ORANGE        = (220, 130,  30)
YELLOW        = (240, 210,  50)
WHITE         = (255, 255, 255)
BLACK         = (  0,   0,   0)
GRAY          = (130, 130, 130)
LIGHT_GRAY    = (200, 200, 200)
SKIN          = (220, 170, 110)
DARK_BROWN    = ( 80,  50,  15)
BROWN         = (140,  90,  40)
GREEN_VEST    = ( 50, 130,  50)
BOAT_BROWN    = (160, 100,  40)
BOAT_DARK     = (100,  60,  20)

# Night palette (Level 2)
NIGHT_SKY     = ( 15,  20,  45)
NIGHT_RIVER   = ( 15,  50,  90)
NIGHT_WAVE    = ( 25,  80, 130)
NIGHT_LAND    = ( 25,  55,  30)
NIGHT_LAND_DK = ( 15,  35,  18)
MOON_GLOW     = (235, 235, 200)

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "images")


def load_image(filename, size=None):
    """
    Try to load an image from assets/images/filename.
    Returns a pygame Surface, or None if the file doesn't exist yet.
    Drop your own PNGs into assets/images/ using these exact filenames
    and they will be used automatically instead of the drawn shapes.
    """
    path = os.path.join(ASSET_DIR, filename)
    if os.path.isfile(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.smoothscale(img, size)
            return img
        except Exception:
            return None
    return None


class Entity:
    """Base class for all game entities."""
    def __init__(self, name, entity_type):
        self.name        = name
        self.entity_type = entity_type
        self.on_boat     = False
        self.side        = "left"
        self.image       = None   # cached loaded image, set by subclasses

    def __repr__(self):
        return f"{self.name}({self.side})"

    def draw(self, screen, x, y, size=48):
        pass


class Rescuer(Entity):
    """Rescue team member — required to operate the boat."""
    IMG_FILE = "rescuer.png"

    def __init__(self, name):
        super().__init__(name, "rescuer")

    def draw(self, screen, x, y, size=48):
        img = load_image(self.IMG_FILE, (size, size))
        if img:
            screen.blit(img, (x, y))
        else:
            self._draw_default(screen, x, y, size)
        font = pygame.font.SysFont(None, 12)
        lbl  = font.render(self.name, True, WHITE)
        screen.blit(lbl, (x + size//2 - lbl.get_width()//2, y + size + 2))

    def _draw_default(self, screen, x, y, s):
        pygame.draw.rect(screen, GREEN_VEST,
                         (x+s//4, y+s//2, s//2, s//2-4), border_radius=3)
        pygame.draw.circle(screen, SKIN, (x+s//2, y+s//3), s//5)
        pygame.draw.ellipse(screen, ORANGE,
                            (x+s//3, y+s//6, s//3, s//5))
        pygame.draw.rect(screen, ORANGE,
                         (x+s//3-2, y+s//4, s//3+4, s//10))
        pygame.draw.circle(screen, BLACK, (x+s//2-4, y+s//3-2), 2)
        pygame.draw.circle(screen, BLACK, (x+s//2+4, y+s//3-2), 2)
        pygame.draw.rect(screen, GRAY,
                         (x+s*3//4-4, y+s//2+2, 6, 10), border_radius=1)
        pygame.draw.rect(screen, DARK_BROWN,
                         (x+s//3,   y+s*3//4, s//7, s//4))
        pygame.draw.rect(screen, DARK_BROWN,
                         (x+s//2+2, y+s*3//4, s//7, s//4))


class Victim(Entity):
    """Disaster victim — must be transported to safety."""
    IMG_FILE = "victim.png"

    def __init__(self, name):
        super().__init__(name, "victim")

    def draw(self, screen, x, y, size=48):
        img = load_image(self.IMG_FILE, (size, size))
        if img:
            screen.blit(img, (x, y))
        else:
            self._draw_default(screen, x, y, size)
        font = pygame.font.SysFont(None, 12)
        lbl  = font.render(self.name, True, WHITE)
        screen.blit(lbl, (x + size//2 - lbl.get_width()//2, y + size + 2))

    def _draw_default(self, screen, x, y, s):
        pygame.draw.rect(screen, (180, 100, 80),
                         (x+s//4, y+s//2, s//2, s//2-4), border_radius=3)
        pygame.draw.circle(screen, SKIN, (x+s//2, y+s//3), s//5)
        pygame.draw.line(screen, WHITE,
                         (x+s//4, y+s//2+6), (x+s*3//4, y+s//2+6), 2)
        pygame.draw.circle(screen, BLACK, (x+s//2-4, y+s//3-2), 2)
        pygame.draw.circle(screen, BLACK, (x+s//2+4, y+s//3-2), 2)
        pygame.draw.arc(screen, BLACK,
                        (x+s//2-6, y+s//3+4, 12, 8), math.pi, 2*math.pi, 2)
        pygame.draw.rect(screen, DARK_BROWN,
                         (x+s//3,   y+s*3//4, s//7, s//4))
        pygame.draw.rect(screen, DARK_BROWN,
                         (x+s//2+2, y+s*3//4, s//7, s//4))


class MedKit(Entity):
    """Medical kit — must be transported to safety before it expires (if timed)."""
    IMG_FILE = "medkit.png"

    def __init__(self, name, expire_frames=None):
        super().__init__(name, "medkit")
        self.expire_frames = expire_frames   # None = no expiry
        self.frames_left   = expire_frames
        self.destroyed      = False

    def tick(self):
        """Call once per frame while NOT yet on the safe side."""
        if self.expire_frames is not None and not self.destroyed:
            if self.frames_left > 0:
                self.frames_left -= 1
            else:
                self.destroyed = True

    def seconds_left(self):
        if self.expire_frames is None:
            return None
        return max(0, self.frames_left // 60)

    def draw(self, screen, x, y, size=48):
        img = load_image(self.IMG_FILE, (size, size))
        if img:
            screen.blit(img, (x, y))
        else:
            self._draw_default(screen, x, y, size)
        font = pygame.font.SysFont(None, 12)
        lbl  = font.render(self.name, True, WHITE)
        screen.blit(lbl, (x + size//2 - lbl.get_width()//2, y + size + 2))

        secs = self.seconds_left()
        if secs is not None:
            badge_col = (255, 60, 60) if secs <= 10 else (255, 200, 50)
            pygame.draw.circle(screen, badge_col, (x+size-6, y+6), 10)
            pygame.draw.circle(screen, WHITE, (x+size-6, y+6), 10, 1)
            bfont = pygame.font.SysFont(None, 16)
            bl = bfont.render(str(secs), True, BLACK)
            screen.blit(bl, (x+size-6-bl.get_width()//2, y+6-bl.get_height()//2))

    def _draw_default(self, screen, x, y, s):
        pad = s // 6
        pygame.draw.rect(screen, RED,
                         (x+pad, y+pad+4, s-pad*2, s-pad*2-4), border_radius=4)
        pygame.draw.rect(screen, DARK_RED,
                         (x+pad, y+pad+4, s-pad*2, s-pad*2-4), 2, border_radius=4)
        cw = s // 6
        cx = x + s // 2
        cy = y + s // 2 + 4
        pygame.draw.rect(screen, WHITE,
                         (cx - cw//2, cy - s//5, cw, s*2//5))
        pygame.draw.rect(screen, WHITE,
                         (cx - s//5, cy - cw//2, s*2//5, cw))
        pygame.draw.rect(screen, DARK_RED,
                         (x+s//3, y+pad, s//3, s//6), border_radius=2)


class Killer(Entity):
    """Hostile entity — destroys MedKits if left alone without a Rescuer."""
    IMG_FILE = "killer.png"

    def __init__(self, name):
        super().__init__(name, "killer")

    def draw(self, screen, x, y, size=48):
        img = load_image(self.IMG_FILE, (size, size))
        if img:
            screen.blit(img, (x, y))
        else:
            self._draw_default(screen, x, y, size)
        font = pygame.font.SysFont(None, 12)
        lbl  = font.render(self.name, True, (255, 80, 80))
        screen.blit(lbl, (x + size//2 - lbl.get_width()//2, y + size + 2))

    def _draw_default(self, screen, x, y, s):
        pygame.draw.rect(screen, (40, 40, 50),
                         (x+s//4, y+s//2, s//2, s//2-4), border_radius=3)
        pygame.draw.circle(screen, (30, 30, 35), (x+s//2, y+s//3), s//4)
        pygame.draw.circle(screen, (60, 55, 60), (x+s//2, y+s//3+2), s//6)
        pygame.draw.circle(screen, (220, 30, 30), (x+s//2-4, y+s//3), 2)
        pygame.draw.circle(screen, (220, 30, 30), (x+s//2+4, y+s//3), 2)
        pygame.draw.line(screen, (180, 180, 190),
                         (x+s*3//4, y+s//2), (x+s-4, y+s*3//4), 3)
        pygame.draw.circle(screen, (100, 60, 30), (x+s*3//4, y+s//2), 3)
        pygame.draw.rect(screen, (30, 30, 35),
                         (x+s//3,   y+s*3//4, s//7, s//4))
        pygame.draw.rect(screen, (30, 30, 35),
                         (x+s//2+2, y+s*3//4, s//7, s//4))


class Boat:
    """The rescue boat — carries entities across the river."""
    MAX_CAPACITY  = 2
    BASE_SPEED    = 0.012
    SPEED_FACTOR  = 0.6   # slowed down per user request

    def __init__(self, screen_w, screen_h):
        self.side       = "left"
        self.moving     = False
        self.progress   = 0.0
        self.speed      = self.BASE_SPEED * self.SPEED_FACTOR
        self.passengers = []
        self.sw         = screen_w
        self.sh         = screen_h
        self.wave_tick  = 0
        self.left_x     = 140
        self.right_x    = screen_w - 230
        self.y          = screen_h // 2 - 20
        self.image      = load_image("boat.png", (90, 50))

    @property
    def x(self):
        if not self.moving:
            return self.left_x if self.side == "left" else self.right_x
        if self.side == "left":
            return int(self.left_x + (self.right_x - self.left_x) * self.progress)
        else:
            return int(self.right_x - (self.right_x - self.left_x) * self.progress)

    def can_board(self):
        return len(self.passengers) < self.MAX_CAPACITY

    def board(self, entity):
        if self.can_board():
            self.passengers.append(entity)
            entity.on_boat = True
            return True
        return False

    def disembark(self, entity):
        if entity in self.passengers:
            self.passengers.remove(entity)
            entity.on_boat = False
            entity.side = self.side
            return True
        return False

    def start_crossing(self):
        if self.passengers and not self.moving:
            if any(p.entity_type == "rescuer" for p in self.passengers):
                self.moving   = True
                self.progress = 0.0
                return True
        return False

    def move_vertical(self, dy, river_top=80, river_bottom=520):
        """Move boat up/down while crossing to dodge obstacles."""
        if self.moving:
            new_y = self.y + dy
            self.y = max(river_top, min(river_bottom - 36, new_y))

    def update(self):
        self.wave_tick += 1
        if self.moving:
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.moving   = False
                self.side     = "right" if self.side == "left" else "left"
                self.y        = self.sh // 2 - 20
                for p in self.passengers:
                    p.side = self.side
                return True
        return False

    def draw(self, screen):
        bx = self.x
        by = self.y
        w, h = 90, 36
        wo = int(4 * math.sin(self.wave_tick * 0.08))

        if self.image:
            screen.blit(self.image, (bx - 5, by - 4 + wo))
        else:
            hull_pts = [
                (bx,      by+h+wo),
                (bx+w,    by+h+wo),
                (bx+w+10, by+h//2+wo),
                (bx-10,   by+h//2+wo),
            ]
            pygame.draw.polygon(screen, BOAT_BROWN, hull_pts)
            pygame.draw.polygon(screen, BOAT_DARK,  hull_pts, 2)
            pygame.draw.rect(screen, (180, 120, 50),
                             (bx, by+4+wo, w, h//2), border_radius=3)
            pygame.draw.rect(screen, WHITE,  (bx+w//2-8, by+8+wo, 16, 16))
            pygame.draw.rect(screen, RED,    (bx+w//2-3, by+8+wo,  6, 16))
            pygame.draw.rect(screen, RED,    (bx+w//2-8, by+13+wo, 16,  6))

        font = pygame.font.SysFont(None, 16)
        cap  = font.render(f"{len(self.passengers)}/{self.MAX_CAPACITY}", True, WHITE)
        screen.blit(cap, (bx + w//2 - cap.get_width()//2, by - 16))

        pw = w // (self.MAX_CAPACITY + 1)
        for i, p in enumerate(self.passengers):
            px = bx + pw * (i+1) - 16
            py = by - 28 + wo
            p.draw(screen, px, py, size=32)


class Obstacle:
    """Floating obstacle in the river — drifts top to bottom, boat must avoid."""
    IMG_FILES = {"rock": "rock.png", "log": "log.png"}

    def __init__(self, x, y, speed, obstacle_type='rock'):
        self.x     = x
        self.y     = y
        self.speed = speed   # now used as VERTICAL speed (top -> bottom)
        self.obstacle_type = obstacle_type
        self.w = 36 if obstacle_type == 'rock' else 44
        self.h = 24 if obstacle_type == 'rock' else 60
        self.active = True
        self.image  = load_image(self.IMG_FILES.get(obstacle_type, ""), (self.w, self.h))

    def update(self, river_top, river_bottom):
        self.y += self.speed
        # Wrap around: reappear at top once it drifts past the bottom
        if self.y > river_bottom:
            self.y = river_top - self.h
        elif self.y + self.h < river_top:
            self.y = river_bottom

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen):
        if not self.active:
            return
        if self.image:
            screen.blit(self.image, (self.x, self.y))
            return
        if self.obstacle_type == 'rock':
            pygame.draw.ellipse(screen, (100, 90, 80), (self.x, self.y, self.w, self.h))
            pygame.draw.ellipse(screen, (130, 120, 110), (self.x+4, self.y+3, self.w-12, self.h-8))
            pygame.draw.ellipse(screen, (80, 70, 60), (self.x, self.y, self.w, self.h), 2)
        else:
            pygame.draw.rect(screen, (120, 70, 30), (self.x, self.y, self.w, self.h), border_radius=6)
            pygame.draw.rect(screen, (90, 50, 15), (self.x, self.y, self.w, self.h), 2, border_radius=6)
            for ry in [self.y+8, self.y+self.h//2, self.y+self.h-8]:
                pygame.draw.line(screen, (90, 50, 15), (self.x+4, ry), (self.x+self.w-4, ry), 1)
