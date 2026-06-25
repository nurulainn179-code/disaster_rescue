import copy
from entities import Rescuer, Victim, MedKit, Killer, Boat


class Level:
    """
    Defines puzzle entities, rules, and win/lose validation.

    Rules (apply on the Danger Zone / left side ONLY — once an entity
    reaches the Safe Zone / right side, no rules apply to it anymore):
      1. A Killer left alone with a MedKit (no Rescuer present on the
         Danger Zone) will destroy the MedKit — instant loss.
      2. (Level 3 only) Each MedKit has a 45-second countdown. If it is
         not moved to the Safe Zone before the timer hits 0, it is
         destroyed — instant loss.
    """

    TIME_LIMITS   = [60, 120, 180]    # seconds: Level 1=1min, 2=2min, 3=3min
    MEDKIT_EXPIRE = 45 * 60           # Level 3 only: MedKits expire after 45s
    OBSTACLE_HIT_PENALTY = 10         # score penalty per obstacle hit
    BASE_SCORE    = 500

    @staticmethod
    def make_entities(level_num):
        configs = [
            # Level 1 — Basic Rescue
            [Rescuer("Rescuer 1"), Victim("Victim 1"),
             MedKit("Medical Kits 1"), Killer("Killer 1")],
            # Level 2 — Night Evacuation
            [Rescuer("Rescuer 1"), Rescuer("Rescuer 2"),
             Victim("Victim 1"), Victim("Victim 2"),
             MedKit("Medical Kits 1"), Killer("Killer 1")],
            # Level 3 — Critical Rescue (timed medkits)
            [Rescuer("Rescuer 1"), Victim("Victim 1"), Victim("Victim 2"),
             MedKit("Medical Kits 1", expire_frames=Level.MEDKIT_EXPIRE),
             Killer("Killer 1")],
        ]
        return copy.deepcopy(configs[level_num])

    TITLES_EN = ["Level 1 - Basic Rescue", "Level 2 - Night Evacuation", "Level 3 - Critical Rescue"]
    TITLES_BM = ["Tahap 1 - Penyelamatan Asas", "Tahap 2 - Pemindahan Malam", "Tahap 3 - Penyelamatan Kritikal"]
    DESCS_EN  = ["Get everyone across! Boat fits 2.",
                 "Darkness has fallen — cross carefully and watch for obstacles.",
                 "The Medical Kit won't last long. Move fast!"]
    DESCS_BM  = ["Bawa semua ke seberang! Bot muat 2.",
                 "Malam telah tiba — seberang dengan berhati-hati.",
                 "Kit Perubatan tidak akan bertahan lama. Bergerak cepat!"]

    def __init__(self, level_num, screen_w, screen_h):
        self.level_num   = level_num
        self.title_en    = self.TITLES_EN[level_num]
        self.title_bm    = self.TITLES_BM[level_num]
        self.desc_en     = self.DESCS_EN[level_num]
        self.desc_bm     = self.DESCS_BM[level_num]
        self.is_night    = (level_num == 1)   # Level 2 = night theme
        self.entities    = self.make_entities(level_num)
        for e in self.entities:
            e.side    = "left"
            e.on_boat = False

        self.boat            = Boat(screen_w, screen_h)
        self.crossings       = 0
        self.violations      = 0
        self.medkit_lost     = 0   # destroyed by killer
        self.medkit_expired  = 0   # expired countdown (Level 3)
        self.obstacle_hits   = 0   # number of times boat hit an obstacle
        self.time_limit      = self.TIME_LIMITS[level_num] * 60

    # ── MedKit expiry (Level 3 only) ──────────────────────────────
    def tick_medkits(self):
        """Call once per frame. Counts down any MedKit with an expiry
        timer as long as it has NOT yet reached the Safe Zone."""
        for e in self.entities:
            if e.entity_type == "medkit" and e.expire_frames is not None:
                if e.side != "right" and not e.destroyed:
                    was_destroyed = e.destroyed
                    e.tick()
                    if e.destroyed and not was_destroyed:
                        self.medkit_expired += 1

    # ── Queries ──────────────────────────────────────────────────
    def entities_on(self, side):
        return [e for e in self.entities if e.side == side and not e.on_boat]

    def rescuers_on(self, side):
        return [e for e in self.entities_on(side) if e.entity_type == "rescuer"]

    def victims_on(self, side):
        return [e for e in self.entities_on(side) if e.entity_type == "victim"]

    def killers_on(self, side):
        return [e for e in self.entities_on(side) if e.entity_type == "killer"]

    def medkits_on(self, side):
        return [e for e in self.entities_on(side)
                if e.entity_type == "medkit" and not getattr(e, "destroyed", False)]

    def all_on_right(self):
        return all(e.side == "right" and not e.on_boat
                    and not getattr(e, "destroyed", False)
                    for e in self.entities)

    # ── Rule validation ──────────────────────────────────────────
    def is_safe(self):
        """
        Killer + MedKit rule — applies ONLY on the Danger Zone (left).
        Once a MedKit reaches the Safe Zone (right), it is no longer
        at risk from the Killer.
        """
        safe = True
        side = "left"   # rule only applies to the Danger Zone
        r = len(self.rescuers_on(side))
        k = len(self.killers_on(side))
        m = self.medkits_on(side)

        if k > 0 and m and r == 0:
            for kit in m:
                if not getattr(kit, "destroyed", False):
                    kit.destroyed = True
                    self.medkit_lost += 1
            safe = False
        return safe

    def would_be_unsafe_after_departure(self):
        """Victim/Rescuer balance rule removed — boat may always depart
        as long as normal boarding rules (capacity, rescuer present) hold."""
        return False

    def check_violation(self):
        if not self.is_safe():
            self.violations += 1
            return True
        return False

    # ── Boat actions ─────────────────────────────────────────────
    def board_entity(self, entity):
        if getattr(entity, "destroyed", False):
            return False, "destroyed"
        if entity.side != self.boat.side:
            return False, "wrong_side"
        if entity.on_boat:
            return False, "already_on"
        if not self.boat.can_board():
            return False, "full"
        self.boat.board(entity)
        return True, "ok"

    def disembark_entity(self, entity):
        return self.boat.disembark(entity)

    def send_boat(self):
        if self.would_be_unsafe_after_departure():
            return False
        ok = self.boat.start_crossing()
        if ok:
            self.crossings += 1
        return ok

    def on_boat_arrival(self):
        return self.check_violation()

    def force_boat_back(self):
        """Called when the boat hits an obstacle — bounces back to the
        Danger Zone (left) and registers a score penalty."""
        boat = self.boat
        boat.moving   = False
        boat.progress = 0.0
        boat.side     = "left"
        for p in boat.passengers:
            p.side = "left"
        self.obstacle_hits += 1

    # ── Time ─────────────────────────────────────────────────────
    def time_remaining(self, elapsed_frames):
        remaining_frames = self.time_limit - elapsed_frames
        return max(0, remaining_frames // 60)

    def is_time_up(self, elapsed_frames):
        return elapsed_frames >= self.time_limit

    # ── Score ────────────────────────────────────────────────────
    def calc_score(self, time_frames):
        time_pen  = (time_frames // 60) * 2
        viol_pen  = self.violations * 50
        cross_pen = self.crossings * 5
        lost_pen  = (self.medkit_lost + self.medkit_expired) * 80
        hit_pen   = self.obstacle_hits * self.OBSTACLE_HIT_PENALTY
        return max(0, self.BASE_SCORE - time_pen - viol_pen - cross_pen
                   - lost_pen - hit_pen)
