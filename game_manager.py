import pygame
import sys
import math
import random
import os
from level import Level
from entities import (RIVER_BLUE, DEEP_BLUE, WAVE_BLUE, LAND_GREEN,
                      DARK_GREEN, SAND, RED, ORANGE, YELLOW,
                      WHITE, BLACK, GRAY, LIGHT_GRAY,
                      BOAT_BROWN, SKIN, GREEN_VEST, Obstacle,
                      NIGHT_SKY, NIGHT_RIVER, NIGHT_WAVE,
                      NIGHT_LAND, NIGHT_LAND_DK, MOON_GLOW)

SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")

TEXT = {
    "EN": {
        "title":      "Disaster Rescue",
        "subtitle":   "River Crossing Puzzle",
        "start":      "Start Game",
        "instr":      "Instructions",
        "exit":       "Exit",
        "score":      "Score",
        "time":       "Time",
        "crossings":  "Crossings",
        "pause":      "PAUSED",
        "resume":     "P - Resume",
        "restart":    "R - Restart",
        "next":       "N - Next Level",
        "win":        "Everyone Safe!",
        "gameover":   "Mission Complete!",
        "timeup":     "TIME'S UP!",
        "failed":     "Mission Failed — try again!",
        "killer_lose":"MEDICAL KIT DESTROYED!",
        "killer_failed": "The Killer got to it. Mission Failed.",
        "expired_lose": "MEDICAL KIT EXPIRED!",
        "expired_failed": "It wasn't moved in time. Mission Failed.",
        "play_again": "Play Again",
        "send":       "SPACE - Send Boat",
        "click":      "Click entity to board/disembark",
        "lang":       "Bahasa Melayu",
        "how1":       "Click an entity on the shore to board the boat",
        "how2":       "Click an entity on the boat to disembark it",
        "how3":       "Press SPACE to send the boat across the river",
        "how4":       "The boat needs at least 1 Rescuer to move",
        "how5":       "Rules only apply on the Danger Zone shore",
        "how6":       "Never leave a Killer alone with a Medical Kit on the Danger Zone!",
        "how7":       "While crossing, use UP/DOWN arrows to dodge obstacles",
        "how8":       "Hitting an obstacle bounces the boat back and costs 10 points",
        "back":       "Press any key to return",
        "left":       "Danger Zone",
        "right":      "Safe Zone",
        "nav":        "UP/DOWN to select, ENTER to confirm",
        "story_title":"The Mission",
        "story_continue": "Press ENTER to begin",
        "summary_title": "Mission Summary",
        "summary_total":  "Total Score",
        "summary_continue": "Press ENTER to continue",
        "final_title": "All Levels Complete!",
    },
    "BM": {
        "title":      "Penyelamat Bencana",
        "subtitle":   "Teka-Teki Menyeberangi Sungai",
        "start":      "Mula Permainan",
        "instr":      "Arahan",
        "exit":       "Keluar",
        "score":      "Markah",
        "time":       "Masa",
        "crossings":  "Perjalanan",
        "pause":      "BERHENTI",
        "resume":     "P - Teruskan",
        "restart":    "R - Mula Semula",
        "next":       "N - Tahap Seterusnya",
        "win":        "Semua Selamat!",
        "gameover":   "Misi Selesai!",
        "timeup":     "MASA TAMAT!",
        "failed":     "Misi Gagal — cuba lagi!",
        "killer_lose":"KIT PERUBATAN DIROSAKKAN!",
        "killer_failed": "Pembunuh telah merosakkannya. Misi Gagal.",
        "expired_lose": "KIT PERUBATAN TAMAT MASA!",
        "expired_failed": "Tidak dipindahkan tepat masa. Misi Gagal.",
        "play_again": "Main Semula",
        "send":       "SPACE - Hantar Bot",
        "click":      "Klik entiti untuk naik/turun bot",
        "lang":       "English",
        "how1":       "Klik entiti di tebing untuk naikkan ke bot",
        "how2":       "Klik entiti di bot untuk turunkannya",
        "how3":       "Tekan SPACE untuk hantar bot menyeberang sungai",
        "how4":       "Bot perlukan sekurang-kurangnya 1 Penyelamat untuk bergerak",
        "how5":       "Peraturan hanya berkuat kuasa di Zon Bahaya",
        "how6":       "Jangan tinggalkan Pembunuh bersama Kit Perubatan di Zon Bahaya!",
        "how7":       "Semasa menyeberang, guna anak panah ATAS/BAWAH untuk elak halangan",
        "how8":       "Terkena halangan membuat bot terpantul balik dan tolak 10 markah",
        "back":       "Tekan mana-mana kekunci untuk kembali",
        "left":       "Zon Bahaya",
        "right":      "Zon Selamat",
        "nav":        "ATAS/BAWAH untuk pilih, ENTER untuk sahkan",
        "story_title":"Misi Ini",
        "story_continue": "Tekan ENTER untuk mula",
        "summary_title": "Ringkasan Misi",
        "summary_total":  "Jumlah Markah",
        "summary_continue": "Tekan ENTER untuk teruskan",
        "final_title": "Semua Tahap Selesai!",
    },
}

STORY_LINES = {
    "EN": [
        [  # Level 1
            "A flash flood has struck the village.",
            "Survivors and critical medical supplies",
            "are trapped on the Danger Zone shore.",
            "A lurking Killer threatens anyone left",
            "unprotected — especially medical kits.",
            "As the Rescue Team, guide everyone",
            "safely across the river.",
        ],
        [  # Level 2
            "The disaster struck again — this time at night.",
            "Darkness blankets the river as the Rescue",
            "Team returns to save more victims and",
            "medical supplies trapped on the shore.",
            "The Killer still lurks in the shadows.",
            "Cross carefully — obstacles are harder",
            "to see in the dark.",
        ],
        [  # Level 3
            "Time is running out. This Medical Kit",
            "is critically needed and won't last long",
            "out in the open.",
            "You have only 45 seconds to get it",
            "across before it expires.",
            "Move fast, dodge obstacles, and don't",
            "let the Killer near it either!",
        ],
    ],
    "BM": [
        [
            "Banjir kilat melanda kampung.",
            "Mangsa dan bekalan perubatan kritikal",
            "terperangkap di tebing Zon Bahaya.",
            "Seorang Pembunuh mengancam sesiapa yang",
            "ditinggalkan tanpa perlindungan.",
            "Sebagai Pasukan Penyelamat, bawa semua",
            "menyeberangi sungai dengan selamat.",
        ],
        [
            "Bencana melanda sekali lagi — kali ini waktu malam.",
            "Kegelapan menyelubungi sungai ketika Pasukan",
            "Penyelamat kembali untuk menyelamatkan lagi",
            "mangsa dan bekalan perubatan.",
            "Pembunuh masih mengintai dalam bayang-bayang.",
            "Seberang dengan berhati-hati — halangan lebih",
            "sukar dilihat dalam gelap.",
        ],
        [
            "Masa semakin suntuk. Kit Perubatan ini",
            "amat diperlukan dan tidak akan bertahan",
            "lama jika terdedah.",
            "Anda hanya ada 45 saat untuk membawanya",
            "menyeberang sebelum ia tamat tempoh.",
            "Bergerak cepat, elak halangan, dan jangan",
            "biar Pembunuh menghampirinya!",
        ],
    ],
}

STATE_MENU    = "menu"
STATE_STORY   = "story"
STATE_INSTR   = "instr"
STATE_PLAYING = "playing"
STATE_PAUSED  = "paused"
STATE_WIN     = "win"          # level cleared, show per-level summary
STATE_END     = "end"          # all levels cleared
STATE_LOSE    = "lose"

MAX_LEVELS = 3


class GameManager:
    def __init__(self, screen, sw, sh):
        self.screen       = screen
        self.sw           = sw
        self.sh           = sh
        self.lang         = "EN"
        self.state        = STATE_MENU
        self.font_big     = pygame.font.SysFont(None, 64)
        self.font_med     = pygame.font.SysFont(None, 38)
        self.font_sml     = pygame.font.SysFont(None, 25)
        self.font_tiny    = pygame.font.SysFont(None, 20)

        self.level_num    = 0
        self.level        = None
        self.timer        = 0
        self.total_score  = 0
        self.level_scores = []     # score per completed level
        self.warning_tim  = 0
        self.warning_msg  = "warning"
        self.wave_tick    = 0
        self.cooldown     = 0
        self.obstacles    = []
        self.hit_timer    = 0
        self.lose_reason  = "timeup"
        self.menu_sel     = 0
        self.menu_opts    = ["start", "instr", "exit"]
        self.play_again_rect = None
        self.next_rect        = None

        self._init_sounds()

    # ── Sounds ───────────────────────────────────────────────────
    def _load_sound(self, filename, fallback_freq, fallback_ms, vol=0.25):
        """Load a .wav/.ogg from assets/sounds/filename if present,
        otherwise synthesize a simple beep as a fallback."""
        path = os.path.join(SOUND_DIR, filename)
        if os.path.isfile(path):
            try:
                s = pygame.mixer.Sound(path)
                s.set_volume(vol)
                return s
            except Exception:
                pass
        return self._beep(fallback_freq, fallback_ms, vol)

    def _beep(self, freq, ms, vol=0.2):
        import array, math as m
        try:
            sr = 22050
            n  = int(sr * ms / 1000)
            buf = array.array('h', [int(32767 * m.sin(2*m.pi*freq*i/sr)) for i in range(n)])
            s = pygame.sndarray.make_sound(buf)
            s.set_volume(vol)
            return s
        except Exception:
            return None

    def _init_sounds(self):
        self.snd_click = self._load_sound("click.wav",    440, 80)
        self.snd_cross = self._load_sound("cross.wav",    330, 200)
        self.snd_win   = self._load_sound("win.wav",      660, 400)
        self.snd_warn  = self._load_sound("warning.wav",  200, 150)
        self.snd_hit   = self._load_sound("hit.wav",      120, 250)

    def _play(self, snd):
        if snd:
            try: snd.play()
            except: pass

    def t(self, key):
        return TEXT[self.lang].get(key, key)

    # ── State changes ────────────────────────────────────────────
    def _go_menu(self):
        self.state    = STATE_MENU
        self.cooldown = 20

    def _go_story(self, level_num):
        self.pending_level = level_num
        self.state         = STATE_STORY
        self.cooldown      = 20

    def _start_level(self, num):
        self.level_num   = num
        self.level       = Level(num, self.sw, self.sh)
        self.timer       = 0
        self.warning_tim = 0
        self.state       = STATE_PLAYING
        self.cooldown    = 45
        self._init_obstacles(num)

    def _init_obstacles(self, level_num):
        self.obstacles = []
        river_top    = 90
        river_bottom = self.sh - 100
        counts = [3, 4, 5]
        n = counts[min(level_num, 2)]
        for i in range(n):
            otype = 'rock' if i % 2 == 0 else 'log'
            x     = random.randint(220, self.sw - 270)
            y     = random.randint(river_top, river_bottom - 40)
            # Vertical drift speed (top -> bottom), slowed per user request
            speed = random.choice([0.4, 0.5, 0.6]) * (1 + level_num * 0.25)
            self.obstacles.append(Obstacle(x, y, speed, otype))
        self.hit_timer = 0

    # ── Events ───────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type not in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            return
        if self.cooldown > 0:
            return

        if self.state == STATE_MENU:
            self._ev_menu(event)
        elif self.state == STATE_STORY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._start_level(self.pending_level)
        elif self.state == STATE_INSTR:
            if event.type == pygame.KEYDOWN:
                self._go_menu()
        elif self.state == STATE_PLAYING:
            self._ev_playing(event)
        elif self.state == STATE_PAUSED:
            self._ev_paused(event)
        elif self.state == STATE_WIN:
            self._ev_win(event)
        elif self.state == STATE_END:
            self._ev_end(event)
        elif self.state == STATE_LOSE:
            self._ev_lose(event)

    def _ev_menu(self, event):
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if key == pygame.K_UP:
            self.menu_sel = (self.menu_sel - 1) % len(self.menu_opts)
        elif key == pygame.K_DOWN:
            self.menu_sel = (self.menu_sel + 1) % len(self.menu_opts)
        elif key == pygame.K_RETURN:
            choice = self.menu_opts[self.menu_sel]
            if choice == "start":
                self.total_score  = 0
                self.level_scores = []
                self._go_story(0)
            elif choice == "instr":
                self.state    = STATE_INSTR
                self.cooldown = 20
            elif choice == "exit":
                pygame.quit(); sys.exit()
        elif key == pygame.K_l:
            self.lang = "BM" if self.lang == "EN" else "EN"

    def _ev_playing(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_p:
                self.state    = STATE_PAUSED
                self.cooldown = 20
            elif key == pygame.K_r:
                self._start_level(self.level_num)
            elif key == pygame.K_l:
                self.lang = "BM" if self.lang == "EN" else "EN"
            elif key == pygame.K_SPACE:
                if self.level.would_be_unsafe_after_departure():
                    self.warning_tim = 150
                    self.warning_msg = "blocked_warn"
                    self._play(self.snd_warn)
                else:
                    ok = self.level.send_boat()
                    if ok:
                        self._play(self.snd_cross)
                    else:
                        self._play(self.snd_warn)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_click(event.pos)

    def _ev_paused(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_p:
            self.state    = STATE_PLAYING
            self.cooldown = 20
        elif event.key == pygame.K_r:
            self._start_level(self.level_num)

    def _ev_win(self, event):
        """Per-level summary screen — Enter/click to continue to next level."""
        advance = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            advance = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_rect and self.next_rect.collidepoint(event.pos):
                advance = True
        if advance:
            self._go_story(self.level_num + 1)

    def _ev_end(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.total_score  = 0
            self.level_scores = []
            self._go_story(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_rect and self.play_again_rect.collidepoint(event.pos):
                self.total_score  = 0
                self.level_scores = []
                self._go_story(0)

    def _ev_lose(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._start_level(self.level_num)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_again_rect and self.play_again_rect.collidepoint(event.pos):
                self._start_level(self.level_num)

    def _handle_click(self, pos):
        lv   = self.level
        boat = lv.boat
        if boat.moving:
            return

        left_ents  = [e for e in lv.entities if e.side=="left"  and not e.on_boat]
        right_ents = [e for e in lv.entities if e.side=="right" and not e.on_boat]
        shore_ents = left_ents if boat.side=="left" else right_ents

        for i, entity in enumerate(shore_ents):
            if getattr(entity, "destroyed", False):
                continue
            ex, ey = self._shore_pos(i, entity.side)
            if pygame.Rect(ex, ey, 48, 60).collidepoint(pos):
                ok, _ = lv.board_entity(entity)
                if ok:
                    self._play(self.snd_click)
                return

        bx = boat.x
        by = boat.y
        pw = 90 // (boat.MAX_CAPACITY + 1)
        for i, p in enumerate(boat.passengers):
            px = bx + pw*(i+1) - 16
            py = by - 28
            if pygame.Rect(px, py, 32, 40).collidepoint(pos):
                lv.disembark_entity(p)
                self._play(self.snd_click)
                return

    # ── Update ───────────────────────────────────────────────────
    def update(self):
        self.wave_tick += 1
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.state != STATE_PLAYING:
            return

        self.timer += 1
        if self.warning_tim > 0:
            self.warning_tim -= 1

        river_top    = 90
        river_bottom = self.sh - 100
        boat = self.level.boat

        # MedKit countdown (Level 3)
        self.level.tick_medkits()

        # Arrow keys move boat up/down while crossing
        keys = pygame.key.get_pressed()
        if boat.moving:
            if keys[pygame.K_UP]:
                boat.move_vertical(-3, river_top=river_top, river_bottom=river_bottom)
            if keys[pygame.K_DOWN]:
                boat.move_vertical(3, river_top=river_top, river_bottom=river_bottom)

        arrived = self.level.boat.update()
        if arrived:
            violated = self.level.on_boat_arrival()
            if violated:
                self.warning_tim = 180
                self.warning_msg = "killer_warn" if self.level.medkit_lost > 0 else "warning"
                self._play(self.snd_warn)
        else:
            self.level.is_safe()   # re-check every frame for killer rule

        # Instant loss — Killer destroyed a MedKit
        if self.level.medkit_lost > 0 and self.state == STATE_PLAYING:
            self.lose_reason = "killer"
            self._play(self.snd_hit)
            self.cooldown = 30
            self.state = STATE_LOSE
            return

        # Instant loss — MedKit expired (Level 3)
        if self.level.medkit_expired > 0 and self.state == STATE_PLAYING:
            self.lose_reason = "expired"
            self._play(self.snd_hit)
            self.cooldown = 30
            self.state = STATE_LOSE
            return

        # Obstacles drift top -> bottom; check boat collision
        if self.hit_timer > 0:
            self.hit_timer -= 1
        for obs in self.obstacles:
            obs.update(river_top, river_bottom)
            if boat.moving and self.hit_timer == 0:
                bw, bh = 90, 36
                boat_rect = pygame.Rect(boat.x, boat.y+4, bw, bh)
                if boat_rect.colliderect(obs.get_rect()):
                    self.level.force_boat_back()
                    self.hit_timer   = 90
                    self.warning_tim = 150
                    self.warning_msg = "hit_warn"
                    self._play(self.snd_hit)
                    break

        # Time-up lose condition
        if self.level.is_time_up(self.timer) and self.state == STATE_PLAYING:
            self.lose_reason = "timeup"
            self._play(self.snd_hit)
            self.cooldown = 30
            self.state = STATE_LOSE
            return

        # Win check
        if self.level.all_on_right():
            sc = self.level.calc_score(self.timer)
            self.total_score += sc
            self.level_scores.append(sc)
            self._play(self.snd_win)
            self.cooldown = 30
            if self.level_num + 1 >= MAX_LEVELS:
                self.state = STATE_END
            else:
                self.state = STATE_WIN

    # ── Draw ─────────────────────────────────────────────────────
    def draw(self):
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_STORY:
            self._draw_story()
        elif self.state == STATE_INSTR:
            self._draw_instr()
        elif self.state == STATE_WIN:
            self._draw_level_summary()
        elif self.state == STATE_END:
            self._draw_final_summary()
        else:
            self._draw_game()
            if self.state == STATE_PAUSED:
                self._draw_overlay([self.t("pause"), self.t("resume"), self.t("restart")],
                                   [YELLOW, LIGHT_GRAY, LIGHT_GRAY])
            elif self.state == STATE_LOSE:
                self._draw_lose_screen()

    def _draw_menu(self):
        self.screen.fill(DEEP_BLUE)
        for i in range(10):
            wo = int(6 * math.sin(self.wave_tick * 0.05 + i * 0.8))
            pygame.draw.ellipse(self.screen, WAVE_BLUE,
                                (i*90-20, 350+wo, 130, 22))
        pygame.draw.rect(self.screen, LAND_GREEN, (0, 0, self.sw, 130))
        pygame.draw.rect(self.screen, DARK_GREEN,  (0, 118, self.sw, 14))

        t1 = self.font_big.render(self.t("title"),    True, YELLOW)
        t2 = self.font_sml.render(self.t("subtitle"), True, WHITE)
        self.screen.blit(t1, (self.sw//2 - t1.get_width()//2, 28))
        self.screen.blit(t2, (self.sw//2 - t2.get_width()//2, 94))

        for i, opt in enumerate(self.menu_opts):
            sel  = i == self.menu_sel
            col  = YELLOW if sel else LIGHT_GRAY
            bg   = (40, 100, 160) if sel else (20, 60, 110)
            surf = self.font_med.render(self.t(opt), True, col)
            bx   = self.sw//2 - 160
            by   = 210 + i * 75
            pygame.draw.rect(self.screen, bg,     (bx, by, 320, 55), border_radius=10)
            if sel:
                pygame.draw.rect(self.screen, YELLOW, (bx, by, 320, 55), 2, border_radius=10)
                pygame.draw.polygon(self.screen, YELLOW,
                    [(bx-20, by+27), (bx-8, by+20), (bx-8, by+34)])
            self.screen.blit(surf, (self.sw//2 - surf.get_width()//2, by+12))

        nav = self.font_tiny.render(self.t("nav"), True, GRAY)
        self.screen.blit(nav, (self.sw//2 - nav.get_width()//2, self.sh - 44))
        lh = self.font_tiny.render(f"L - {self.t('lang')}", True, GRAY)
        self.screen.blit(lh, (self.sw - lh.get_width() - 10, self.sh - 22))

    def _draw_story(self):
        self.screen.fill((20, 20, 35))
        for i in range(6):
            wo = int(4 * math.sin(self.wave_tick * 0.04 + i))
            pygame.draw.ellipse(self.screen, (30, 50, 80),
                                (i*150-50, 480+wo, 200, 30))

        title = self.font_big.render(self.t("story_title"), True, YELLOW)
        self.screen.blit(title, (self.sw//2 - title.get_width()//2, 36))

        lvl_lbl = self.font_sml.render(f"Level {self.pending_level + 1}", True, (140, 200, 255))
        self.screen.blit(lvl_lbl, (self.sw//2 - lvl_lbl.get_width()//2, 95))

        lines = STORY_LINES[self.lang][self.pending_level]
        for i, line in enumerate(lines):
            s = self.font_sml.render(line, True, WHITE)
            self.screen.blit(s, (self.sw//2 - s.get_width()//2, 145 + i*36))

        cont = self.font_sml.render(self.t("story_continue"), True, (120, 220, 140))
        if (self.wave_tick // 30) % 2 == 0:
            self.screen.blit(cont, (self.sw//2 - cont.get_width()//2, self.sh - 50))

    def _draw_instr(self):
        self.screen.fill(DEEP_BLUE)
        t = self.font_med.render(self.t("instr"), True, YELLOW)
        self.screen.blit(t, (self.sw//2 - t.get_width()//2, 30))
        keys = ["how1","how2","how3","how4","how5","how6","how7","how8"]
        for i, key in enumerate(keys):
            s = self.font_sml.render(f"• {self.t(key)}", True, WHITE)
            self.screen.blit(s, (50, 85 + i*46))
        back = self.font_sml.render(self.t("back"), True, LIGHT_GRAY)
        self.screen.blit(back, (self.sw//2 - back.get_width()//2, self.sh-40))

    def _shore_pos(self, idx, side):
        col = idx % 2
        row = idx // 2
        if side == "left":
            bx = 15 + col * 85
        else:
            bx = self.sw - 185 + col * 85
        by = 100 + row * 90
        return bx, by

    def _draw_game(self):
        if not self.level:
            return
        night = self.level.is_night

        sky_col   = NIGHT_SKY    if night else (135, 206, 235)
        river_col = NIGHT_RIVER  if night else RIVER_BLUE
        wave_col  = NIGHT_WAVE   if night else WAVE_BLUE
        land_col  = NIGHT_LAND   if night else LAND_GREEN
        land_dk   = NIGHT_LAND_DK if night else DARK_GREEN

        self.screen.fill(sky_col)

        if night:
            # Moon + stars
            pygame.draw.circle(self.screen, MOON_GLOW, (self.sw-80, 50), 28)
            pygame.draw.circle(self.screen, sky_col, (self.sw-70, 42), 24)
            random.seed(42)
            for _ in range(40):
                sx = random.randint(0, self.sw)
                sy = random.randint(0, 80)
                pygame.draw.circle(self.screen, WHITE, (sx, sy), 1)

        pygame.draw.rect(self.screen, river_col,
                         (195, 80, self.sw-390, self.sh-160))
        for i in range(7):
            wo = int(5 * math.sin(self.wave_tick * 0.06 + i*1.3))
            pygame.draw.ellipse(self.screen, wave_col,
                                (205 + i*75, 180+wo, 95, 16))
            pygame.draw.ellipse(self.screen, wave_col,
                                (230 + i*75, 300+wo, 85, 14))

        pygame.draw.rect(self.screen, land_col, (0, 0, 210, self.sh))
        pygame.draw.rect(self.screen, land_dk,  (198, 0, 14, self.sh))
        pygame.draw.rect(self.screen, land_col, (self.sw-210, 0, 210, self.sh))
        pygame.draw.rect(self.screen, land_dk,  (self.sw-212, 0, 14, self.sh))

        lz = self.font_sml.render(self.t("left"),  True, RED)
        rz = self.font_sml.render(self.t("right"), True, (DARK_GREEN if not night else (150,200,160)))
        self.screen.blit(lz, (10, 14))
        self.screen.blit(rz, (self.sw-200, 14))

        lv = self.level
        left_ents  = [e for e in lv.entities if e.side=="left"  and not e.on_boat]
        right_ents = [e for e in lv.entities if e.side=="right" and not e.on_boat]

        for i, e in enumerate(left_ents):
            ex, ey = self._shore_pos(i, "left")
            if lv.boat.side == "left" and not lv.boat.moving and not getattr(e, "destroyed", False):
                pygame.draw.rect(self.screen, (255,255,100),
                                 (ex-2, ey-2, 52, 52), 2, border_radius=4)
            if getattr(e, "destroyed", False):
                pygame.draw.rect(self.screen, (80,80,80), (ex, ey, 44, 44), border_radius=4)
                font = pygame.font.SysFont(None, 20)
                x_lbl = font.render("X", True, RED)
                self.screen.blit(x_lbl, (ex+44//2-6, ey+44//2-10))
            else:
                e.draw(self.screen, ex, ey, 44)

        for i, e in enumerate(right_ents):
            ex, ey = self._shore_pos(i, "right")
            if lv.boat.side == "right" and not lv.boat.moving and not getattr(e, "destroyed", False):
                pygame.draw.rect(self.screen, (255,255,100),
                                 (ex-2, ey-2, 52, 52), 2, border_radius=4)
            if not getattr(e, "destroyed", False):
                e.draw(self.screen, ex, ey, 44)

        for obs in self.obstacles:
            obs.draw(self.screen)

        if self.hit_timer > 0 and self.hit_timer % 10 < 5:
            flash = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
            flash.fill((255, 50, 50, 60))
            self.screen.blit(flash, (0, 0))

        lv.boat.draw(self.screen)

        # HUD
        pygame.draw.rect(self.screen, (20, 20, 60), (0, self.sh-52, self.sw, 52))
        secs_left = lv.time_remaining(self.timer)
        time_col  = RED if secs_left <= 10 else YELLOW
        title = lv.title_en if self.lang=="EN" else lv.title_bm

        s0 = self.font_tiny.render(title, True, YELLOW)
        self.screen.blit(s0, (10, self.sh-40))
        s1 = self.font_tiny.render(f"{self.t('time')}: {secs_left}s", True, time_col)
        self.screen.blit(s1, (10 + 195, self.sh-40))
        s2 = self.font_tiny.render(f"{self.t('crossings')}: {lv.crossings}", True, YELLOW)
        self.screen.blit(s2, (10 + 195*2, self.sh-40))
        s3 = self.font_tiny.render(f"{self.t('score')}: {lv.calc_score(self.timer)}", True, YELLOW)
        self.screen.blit(s3, (10 + 195*3, self.sh-40))

        hint = self.font_tiny.render(
            f"{self.t('click')}  |  SPACE: Send  |  UP/DOWN: Dodge  |  P: Pause  |  R: Restart",
            True, LIGHT_GRAY)
        self.screen.blit(hint, (self.sw//2 - hint.get_width()//2, self.sh-18))

        if self.warning_tim > 0:
            msg_key = self.warning_msg if self.warning_msg in TEXT[self.lang] else "warning"
            ws = self.font_sml.render(self.t(msg_key), True, RED)
            pygame.draw.rect(self.screen, (60,0,0),
                             (self.sw//2 - ws.get_width()//2 - 10,
                              self.sh//2 - 22, ws.get_width()+20, 38), border_radius=6)
            self.screen.blit(ws, (self.sw//2 - ws.get_width()//2, self.sh//2-14))

    # ── Lose screen ──────────────────────────────────────────────
    def _draw_lose_screen(self):
        if self.lose_reason == "killer":
            lines  = [self.t("killer_lose"), self.t("killer_failed")]
            colors = [RED, LIGHT_GRAY]
        elif self.lose_reason == "expired":
            lines  = [self.t("expired_lose"), self.t("expired_failed")]
            colors = [RED, LIGHT_GRAY]
        else:
            lines  = [self.t("timeup"), self.t("failed")]
            colors = [RED, LIGHT_GRAY]
        self._draw_overlay(lines, colors)
        self.play_again_rect = self._draw_button(self.t("play_again"),
                                                   self.sh//2 + 70, (180, 50, 50))

    # ── Per-level summary ─────────────────────────────────────────
    def _draw_level_summary(self):
        self.screen.fill((15, 30, 50))
        title = self.font_big.render(self.t("win"), True, YELLOW)
        self.screen.blit(title, (self.sw//2 - title.get_width()//2, 60))

        lv = self.level
        sc = self.level_scores[-1] if self.level_scores else 0
        lvl_title = lv.title_en if self.lang == "EN" else lv.title_bm
        lt = self.font_med.render(lvl_title, True, (180, 220, 255))
        self.screen.blit(lt, (self.sw//2 - lt.get_width()//2, 140))

        rows = [
            (f"{self.t('score')}", f"{sc}"),
            (f"{self.t('crossings')}", f"{lv.crossings}"),
            ("Obstacle Hits" if self.lang=="EN" else "Kena Halangan", f"{lv.obstacle_hits}"),
        ]
        for i, (label, val) in enumerate(rows):
            ls = self.font_sml.render(f"{label}:", True, LIGHT_GRAY)
            vs = self.font_sml.render(val, True, WHITE)
            y = 210 + i*40
            self.screen.blit(ls, (self.sw//2 - 140, y))
            self.screen.blit(vs, (self.sw//2 + 60, y))

        running_total = self.font_med.render(
            f"{self.t('summary_total')}: {self.total_score}", True, (255, 200, 60))
        self.screen.blit(running_total, (self.sw//2 - running_total.get_width()//2, 360))

        self.next_rect = self._draw_button(self.t("next").replace("N - ", ""), self.sh - 100, (40, 130, 70))

    # ── Final summary (all levels done) ───────────────────────────
    def _draw_final_summary(self):
        self.screen.fill((15, 30, 50))
        title = self.font_big.render(self.t("final_title"), True, YELLOW)
        self.screen.blit(title, (self.sw//2 - title.get_width()//2, 40))

        for i, sc in enumerate(self.level_scores):
            lvl_name = (Level.TITLES_EN[i] if self.lang=="EN" else Level.TITLES_BM[i])
            row = self.font_sml.render(f"{lvl_name}: {sc}", True, WHITE)
            self.screen.blit(row, (self.sw//2 - row.get_width()//2, 130 + i*42))

        total = self.font_big.render(f"{self.t('summary_total')}: {self.total_score}",
                                      True, (255, 200, 60))
        self.screen.blit(total, (self.sw//2 - total.get_width()//2, 290))

        self.play_again_rect = self._draw_button(self.t("play_again"), self.sh - 100, (40, 130, 70))

    # ── Shared UI helpers ───────────────────────────────────────────
    def _draw_overlay(self, lines, colours):
        surf = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 170))
        self.screen.blit(surf, (0, 0))
        for i, (txt, col) in enumerate(zip(lines, colours)):
            font = self.font_big if i == 0 else self.font_med
            s    = font.render(txt, True, col)
            self.screen.blit(s, (self.sw//2 - s.get_width()//2,
                                  self.sh//2 - 70 + i*60))

    def _draw_button(self, label, y, color):
        bw, bh = 220, 54
        bx = self.sw//2 - bw//2
        rect = pygame.Rect(bx, y, bw, bh)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, YELLOW, rect, 2, border_radius=10)
        s = self.font_med.render(label, True, WHITE)
        self.screen.blit(s, (self.sw//2 - s.get_width()//2, y + bh//2 - s.get_height()//2))
        return rect
