from dataclasses import dataclass, field
from typing import List, Tuple, Dict


@dataclass
class Room:
    name: str
    w: float
    h: float
    x: float = 0.0
    y: float = 0.0
    room_type: str = "General"
    color: str = "#ffffff"
    furniture: List[Dict] = field(default_factory=list)
    doors: List[Dict] = field(default_factory=list)
    windows: List[Dict] = field(default_factory=list)
    openings: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        self.validate()
        self.furniture = self.furniture or []
        self.doors = self.doors or []
        self.windows = self.windows or []
        self.openings = self.openings or []

    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def label(self) -> str:
        return f"{self.name} ({self.room_type})"

    def validate(self):
        if self.w <= 0 or self.h <= 0:
            raise ValueError(f"Invalid room dimensions for {self.name}: {self.w} x {self.h}")
        if self.area <= 0:
            raise ValueError(f"Invalid room area for {self.name}: {self.area}")
        if self.furniture is None:
            self.furniture = []
        if self.doors is None:
            self.doors = []
        if self.windows is None:
            self.windows = []
        if self.openings is None:
            self.openings = []

    def add_furniture(self, item: Dict):
        self.furniture.append(item)

    def add_opening(self, item: Dict):
        self.openings.append(item)
        if item.get("type") == "door":
            self.doors.append(item)
        elif item.get("type") == "window":
            self.windows.append(item)

    def populate_furniture(self):
        self.furniture.clear()
        pad = 1.0
        min_space_w = max(pad, self.w - 2 * pad)
        min_space_h = max(pad, self.h - 2 * pad)

        def clamp_position(value, size, limit):
            return max(pad, min(value, limit - size - pad))

        if self.room_type == "Master Bedroom":
            bed_w = min(10.0, min_space_w * 0.6)
            bed_h = min(8.0, min_space_h * 0.4)
            self.add_furniture({"type": "bed", "x": clamp_position(1.0, bed_w, self.w), "y": clamp_position(1.0, bed_h, self.h), "w": bed_w, "h": bed_h})
            self.add_furniture({"type": "wardrobe", "x": self.w - 3.5, "y": 1.0, "w": 3.0, "h": 2.0})
            self.add_furniture({"type": "table", "x": clamp_position(self.w * 0.25, 3.0, self.w), "y": self.h - 2.5, "w": 3.0, "h": 1.5})
        elif self.room_type == "Bedroom":
            bed_w = min(9.0, min_space_w * 0.6)
            bed_h = min(7.0, min_space_h * 0.35)
            self.add_furniture({"type": "bed", "x": clamp_position(1.0, bed_w, self.w), "y": 1.0, "w": bed_w, "h": bed_h})
            self.add_furniture({"type": "wardrobe", "x": self.w - 3.0, "y": 1.0, "w": 2.5, "h": 1.8})
            if self.w >= 12 and self.h >= 10:
                self.add_furniture({"type": "desk", "x": clamp_position(self.w * 0.15, 3.0, self.w), "y": self.h - 2.0, "w": 3.0, "h": 1.5})
        elif self.room_type == "Living":
            sofa_w = min(10.0, min_space_w * 0.7)
            sofa_h = min(3.0, min_space_h * 0.2)
            self.add_furniture({"type": "sofa", "x": clamp_position(1.0, sofa_w, self.w), "y": self.h - sofa_h - 1.0, "w": sofa_w, "h": sofa_h})
            self.add_furniture({"type": "table", "x": clamp_position((self.w - 4.0) / 2, 4.0, self.w), "y": clamp_position((self.h - 2.5) / 2, 2.5, self.h), "w": 4.0, "h": 2.5})
            self.add_furniture({"type": "tv", "x": self.w - 5.0, "y": 1.0, "w": 4.0, "h": 2.0})
        elif self.room_type == "Kitchen":
            counter_h = min(3.0, min_space_h * 0.25)
            self.add_furniture({"type": "counter", "x": 1.0, "y": 1.0, "w": self.w - 2.0, "h": counter_h})
            self.add_furniture({"type": "sink", "x": 1.5, "y": 1.5, "w": 1.5, "h": 1.2})
            self.add_furniture({"type": "stove", "x": self.w - 3.5, "y": 1.5, "w": 2.0, "h": 1.2})
            self.add_furniture({"type": "refrigerator", "x": self.w - 2.5, "y": self.h - 3.0, "w": 2.0, "h": 2.5})
        elif self.room_type == "Dining":
            table_w = min(6.0, self.w - 2.0)
            table_h = min(4.0, self.h - 2.0)
            self.add_furniture({"type": "table", "x": clamp_position((self.w - table_w) / 2, table_w, self.w), "y": clamp_position((self.h - table_h) / 2, table_h, self.h), "w": table_w, "h": table_h})
            self.add_furniture({"type": "chair", "x": 1.0, "y": self.h / 2 - 0.75, "w": 1.0, "h": 1.0})
            self.add_furniture({"type": "chair", "x": self.w - 2.0, "y": self.h / 2 - 0.75, "w": 1.0, "h": 1.0})
        elif self.room_type in {"Study", "Amenity"}:
            desk_w = min(5.0, self.w - 2.0)
            desk_h = min(2.5, self.h * 0.25)
            self.add_furniture({"type": "desk", "x": clamp_position(1.0, desk_w, self.w), "y": 1.0, "w": desk_w, "h": desk_h})
            self.add_furniture({"type": "chair", "x": 1.5, "y": desk_h + 1.5, "w": 1.0, "h": 1.0})
            self.add_furniture({"type": "bookshelf", "x": self.w - 1.0, "y": 1.0, "w": 0.8, "h": min(5.0, self.h - 2.0)})
        elif self.room_type == "Bathroom":
            self.add_furniture({"type": "toilet", "x": self.w - 2.5, "y": 1.0, "w": 1.5, "h": 1.5})
            self.add_furniture({"type": "sink", "x": 1.0, "y": 1.0, "w": 1.5, "h": 1.2})
            self.add_furniture({"type": "shower", "x": clamp_position(self.w - 3.0, 3.0, self.w), "y": self.h - 2.5, "w": 3.0, "h": 2.0})
        elif self.room_type == "Pooja":
            self.add_furniture({"type": "table", "x": clamp_position((self.w - 3.0) / 2, 3.0, self.w), "y": self.h * 0.2, "w": 3.0, "h": 1.5})
        else:
            self.add_furniture({"type": "table", "x": clamp_position(1.0, 3.0, self.w), "y": clamp_position(1.0, 2.0, self.h), "w": 3.0, "h": 2.0})

    def generate_openings(self, plot_width: float, plot_length: float, front_setback: float, rear_setback: float, side_setback: float):
        self.doors.clear()
        self.windows.clear()
        self.openings.clear()

        def add_window(wall, pos, length=20):
            self.add_opening({"type": "window", "wall": wall, "pos": pos})

        def add_door(wall, x, y):
            self.add_opening({"type": "door", "wall": wall, "x": x, "y": y})

        wall = "bottom"
        if self.room_type in ["Living", "Hallway", "Entrance", "Dining"]:
            wall = "top"
        elif self.room_type in ["Kitchen", "Utility", "Pooja"]:
            wall = "left"
        elif self.room_type in ["Bedroom", "Master Bedroom", "Study", "Bathroom"]:
            wall = "right" if self.x < plot_width / 2 else "left"

        door_x = self.w * 0.25 if wall in ["top", "bottom"] else self.w * 0.05
        door_y = self.h * 0.5 if wall in ["left", "right"] else self.h * 0.25
        add_door(wall, door_x, door_y)

        if self.x <= side_setback + 0.1:
            add_window("left", min(max(self.h * 0.4, 1.0), self.h - 1.0))
        if self.x + self.w >= plot_width - side_setback - 0.1:
            add_window("right", min(max(self.h * 0.4, 1.0), self.h - 1.0))
        if self.y <= front_setback + 0.1:
            add_window("top", min(max(self.w * 0.4, 1.0), self.w - 1.0))
        if self.y + self.h >= plot_length - rear_setback - 0.1:
            add_window("bottom", min(max(self.w * 0.4, 1.0), self.w - 1.0))


class FreeSpace:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class ValidationEngine:
    @staticmethod
    def check_overlap(rooms: List[Room]) -> Tuple[bool, str]:
        for i, r1 in enumerate(rooms):
            for r2 in rooms[i + 1:]:
                if not (r1.x + r1.w <= r2.x or r2.x + r2.w <= r1.x or r1.y + r1.h <= r2.y or r2.y + r2.h <= r1.y):
                    return False, f"Overlap detected between {r1.name} and {r2.name}."
        return True, "No overlaps."

    @staticmethod
    def check_boundaries(rooms: List[Room], plot_width: float, plot_length: float) -> Tuple[bool, str]:
        for r in rooms:
            if r.x < 0 or r.y < 0 or r.x + r.w > plot_width or r.y + r.h > plot_length:
                return False, f"{r.name} exceeds plot boundaries."
        return True, "All rooms strictly within plot bounds."

    @staticmethod
    def check_min_size(rooms: List[Room]) -> Tuple[bool, str]:
        for r in rooms:
            if r.w < 3.0 or r.h < 3.0:
                return False, f"{r.name} is too small (Min 3x3 ft)."
        return True, "All rooms meet minimum structural dimensions."

    @staticmethod
    def check_accessibility(rooms: List[Room]) -> Tuple[bool, str]:
        has_public = any(r.room_type in ["Public", "Entrance", "Hallway"] for r in rooms)
        if not has_public:
            return False, "Layout lacks core accessible routing block."
        return True, "Layout is accessible."

    @staticmethod
    def check_aspect_ratio(rooms: List[Room]) -> Tuple[bool, str]:
        for r in rooms:
            ratio = max(r.w / r.h, r.h / r.w) if r.h and r.w else float("inf")
            if ratio > 3.0:
                return False, f"{r.name} has an unrealistic aspect ratio ({r.w:.1f}x{r.h:.1f})."
        return True, "All rooms have realistic proportions."

    @staticmethod
    def final_layout_validation(rooms: List[Room], plot_width: float, plot_length: float) -> Tuple[bool, str]:
        checks = [
            ValidationEngine.check_boundaries(rooms, plot_width, plot_length),
            ValidationEngine.check_overlap(rooms),
            ValidationEngine.check_min_size(rooms),
            ValidationEngine.check_aspect_ratio(rooms),
            ValidationEngine.check_accessibility(rooms),
        ]
        for is_valid, msg in checks:
            if not is_valid:
                return False, msg
        return True, "Layout Fully Validated."


class ConstraintEngine:
    def __init__(self, plot_width: float, plot_length: float, vastu_mode: str):
        self.pw = plot_width
        self.pl = plot_length
        self.vastu_mode = vastu_mode

    def evaluate_vastu_score(self, room_type: str, x: float, y: float, w: float, h: float) -> int:
        if self.vastu_mode == "Ignore":
            return 10

        cx, cy = x + w / 2, y + h / 2
        score = 10

        if room_type == "Kitchen":
            if cx > self.pw * 0.5 and cy > self.pl * 0.5:
                score += 50
            else:
                score -= 20
        elif room_type == "Master Bedroom":
            if cx < self.pw * 0.5 and cy > self.pl * 0.5:
                score += 50
            else:
                score -= 20
        elif room_type == "Pooja":
            if cx > self.pw * 0.5 and cy < self.pl * 0.5:
                score += 50
            else:
                score -= 20
        elif room_type in {"Entrance", "Public"}:
            if cy < self.pl * 0.5 or cx > self.pw * 0.5:
                score += 30

        return score if self.vastu_mode == "Strict" else (score // 2)


class LayoutSolver:
    def __init__(self, plot_width: float, plot_length: float, bedrooms: int, bathrooms: int, amenities: List[str], vastu_mode: str):
        self.pw = plot_width
        self.pl = plot_length
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.amenities = amenities
        self.vastu_mode = vastu_mode

    def estimate_room_dimensions(self, room_type: str) -> Tuple[float, float]:
        defaults = {
            "Master Bedroom": (16.0, 14.0),
            "Bedroom": (13.0, 11.0),
            "Kitchen": (13.0, 11.0),
            "Living": (16.0, 14.0),
            "Dining": (12.0, 11.0),
            "Bathroom": (8.0, 6.5),
            "Hallway": (10.0, 8.0),
            "Utility": (10.0, 9.0),
            "Pooja": (9.0, 7.0),
            "Study": (11.0, 10.0),
            "Home Theatre": (14.0, 12.0),
            "Amenity": (12.0, 10.0),
            "Entrance": (8.0, 6.0),
            "General": (12.0, 12.0),
        }
        return defaults.get(room_type, defaults["General"])

    def _new_room(self, name: str, room_type: str, color: str) -> Room:
        w, h = self.estimate_room_dimensions(room_type)
        return Room(name=name, w=w, h=h, x=0.0, y=0.0, room_type=room_type, color=color)

    def solve(self) -> Tuple[List[Room], List[str]]:
        front_setback = max(10, self.pl * 0.15)
        rear_setback = max(5, self.pl * 0.08)
        side_setback = max(3, self.pw * 0.05)

        bw = self.pw - (side_setback * 2)
        bl = self.pl - (front_setback + rear_setback)

        cw = [bw * 0.35, bw * 0.30, bw * 0.35]
        rh = [bl * 0.35, bl * 0.30, bl * 0.35]

        zones = [[[] for _ in range(3)] for _ in range(3)]

        zones[0][1].append(self._new_room("Entrance Foyer", room_type="Entrance", color="rgba(149, 165, 166, 0.1)"))
        zones[1][1].append(self._new_room("Living Room", room_type="Living", color="rgba(0, 229, 176, 0.15)"))
        zones[1][2].append(self._new_room("Dining Area", room_type="Dining", color="rgba(241, 196, 15, 0.15)"))
        zones[2][2].append(self._new_room("Kitchen", room_type="Kitchen", color="rgba(91, 141, 238, 0.15)"))
        zones[2][0].append(self._new_room("Master Bedroom", room_type="Master Bedroom", color="rgba(255, 107, 53, 0.15)"))

        if self.bathrooms > 0:
            zones[2][0].append(self._new_room("Master Bath", room_type="Bathroom", color="rgba(41, 128, 185, 0.2)"))
        if self.bathrooms > 1:
            zones[1][0].append(self._new_room("Common Bath", room_type="Bathroom", color="rgba(41, 128, 185, 0.2)"))
        if self.bathrooms > 2:
            zones[0][0].append(self._new_room("Guest Bath", room_type="Bathroom", color="rgba(41, 128, 185, 0.2)"))

        bed_prefs = [(0, 0), (2, 1), (0, 2), (1, 0)]
        for i in range(self.bedrooms - 1):
            r, c = bed_prefs[i % 4]
            zones[r][c].append(self._new_room(f"Bedroom {i + 2}", room_type="Bedroom", color="rgba(255, 107, 53, 0.15)"))

        for amenity in self.amenities:
            if amenity == "Pooja Room":
                zones[0][2].append(self._new_room(amenity, room_type="Pooja", color="rgba(46, 213, 115, 0.2)"))
            elif amenity == "Study Room":
                zones[0][2].append(self._new_room(amenity, room_type="Study", color="rgba(155, 89, 182, 0.2)"))
            elif amenity == "Home Gym":
                zones[1][0].append(self._new_room(amenity, room_type="Amenity", color="rgba(230, 126, 34, 0.2)"))
            elif amenity == "Home Theatre":
                zones[0][0].append(self._new_room(amenity, room_type="Home Theatre", color="rgba(192, 57, 43, 0.2)"))
            elif amenity == "Guest Suite":
                zones[0][0].append(self._new_room(amenity, room_type="Amenity", color="rgba(121, 85, 72, 0.2)"))
            elif amenity == "Servant Room":
                zones[1][0].append(self._new_room(amenity, room_type="Amenity", color="rgba(127, 140, 141, 0.2)"))
            elif amenity == "Terrace Garden":
                zones[0][2].append(self._new_room(amenity, room_type="Amenity", color="rgba(46, 204, 113, 0.2)"))
            elif amenity == "Backyard Garden":
                zones[2][1].append(self._new_room(amenity, room_type="Amenity", color="rgba(26, 188, 156, 0.2)"))

        if not zones[0][0]:
            zones[0][0].append(self._new_room("Guest Lounge", room_type="Living", color="rgba(0, 229, 176, 0.1)"))
        if not zones[0][2]:
            zones[0][2].append(self._new_room("Study Room", room_type="Study", color="rgba(155, 89, 182, 0.2)"))
        if not zones[1][0]:
            zones[1][0].append(self._new_room("Corridor", room_type="Hallway", color="rgba(189, 195, 199, 0.2)"))
        if not zones[2][1]:
            zones[2][1].append(self._new_room("Store Room", room_type="Utility", color="rgba(127, 140, 141, 0.2)"))

        placed_rooms = []
        y_curr = front_setback

        for row in range(3):
            x_curr = side_setback
            for col in range(3):
                cell_rooms = zones[row][col]
                z_w, z_h = cw[col], rh[row]

                if len(cell_rooms) == 1:
                    cell_rooms[0].x, cell_rooms[0].y, cell_rooms[0].w, cell_rooms[0].h = x_curr, y_curr, z_w, z_h
                    placed_rooms.append(cell_rooms[0])
                elif len(cell_rooms) > 1:
                    sub_h = z_h / len(cell_rooms)
                    for idx, r in enumerate(cell_rooms):
                        r.x, r.y, r.w, r.h = x_curr, y_curr + idx * sub_h, z_w, sub_h
                        placed_rooms.append(r)
                x_curr += z_w
            y_curr += z_h

        for r in placed_rooms:
            if r.w <= 0 or r.h <= 0:
                raise ValueError(f"Invalid room dimensions: {r.name} ({r.w}x{r.h})")
            r.validate()

        valid_layout, validation_msg = ValidationEngine.final_layout_validation(placed_rooms, self.pw, self.pl)
        if not valid_layout:
            raise ValueError(f"Layout validation failed: {validation_msg}")

        for r in placed_rooms:
            r.populate_furniture()
            r.generate_openings(self.pw, self.pl, front_setback, rear_setback, side_setback)

        outdoor_amenities = [am for am in self.amenities if am in ["Swimming Pool", "Backyard Garden", "Front Lawn", "Kids Play Area", "EV Charging Station", "Covered Parking"]]
        return placed_rooms, outdoor_amenities


def calculate_vastu_score(vastu_mode: str, plot_width: float, plot_length: float, rooms: List[Room]) -> int:
    if vastu_mode == "Ignore":
        return 10
    ce = ConstraintEngine(plot_width, plot_length, vastu_mode)
    raw_score = sum(ce.evaluate_vastu_score(r.room_type, r.x, r.y, r.w, r.h) for r in rooms)
    normalized = max(40, min(98, 50 + (raw_score / max(1, len(rooms))) * 2))
    return int(normalized)


def calculate_cost(buildup_area: float, amenities_list: List[str]) -> Tuple[int, int, int]:
    base_cost = buildup_area * 1800
    amenity_costs = {
        "Swimming Pool": 400000,
        "Home Theatre": 250000,
        "Terrace Garden": 150000,
        "Home Gym": 200000,
        "Study Room": 120000,
        "Office Room": 150000,
        "Servant Room": 100000,
        "Pooja Room": 60000,
    }
    amenity_cost = sum(amenity_costs.get(amenity, 0) for amenity in amenities_list)
    total_cost = int(base_cost + amenity_cost)
    duration_days = int((buildup_area / 100) * 3.5) + (len(amenities_list) * 5)
    return total_cost, amenity_cost, duration_days


def render_professional_floorplan(plot_width: float, plot_length: float, rooms: List[Room], outdoor_amenities: List[str], vastu_mode: str) -> str:
    for room in rooms:
        if room.w <= 0 or room.h <= 0:
            raise ValueError(f"Invalid room dimensions: {room}")

    max_canvas_width = max(600, plot_width * 4.5 + 120)
    max_canvas_height = max(600, plot_length * 4.5 + 100)
    scale = min((max_canvas_width - 120) / plot_width, (max_canvas_height - 100) / plot_length)
    scale = max(3.5, min(scale, 6.0))
    margin = 50

    svg_width = plot_width * scale + margin * 2
    svg_height = plot_length * scale + margin * 2

    def estimate_text_width(chars: int, font_size: float) -> float:
        return chars * font_size * 0.55

    def wrap_label_text(text: str, max_width: float, font_size: float, max_lines: int = 2) -> List[str]:
        words = text.split()
        if not words:
            return [text]

        lines: List[str] = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if estimate_text_width(len(candidate), font_size) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
                if len(lines) >= max_lines:
                    break
        lines.append(current)
        if len(lines) > max_lines:
            joined = " ".join(lines[:max_lines])
            if estimate_text_width(len(joined), font_size) <= max_width:
                lines = [joined]
            else:
                lines = [joined[:int(max_width / (font_size * 0.55))] + "..."]
        return lines

    def choose_font_and_lines(text: str, max_width: float, max_height: float) -> Tuple[float, List[str]]:
        font_size = min(18, max_width / max(1, len(text) * 0.55), max_height / 2.2)
        font_size = max(7, font_size)
        while font_size >= 7:
            lines = wrap_label_text(text, max_width, font_size)
            needed_height = len(lines) * font_size * 1.2 + font_size * 0.8
            if needed_height <= max_height or font_size <= 8:
                return font_size, lines
            font_size -= 0.5
        return 7, wrap_label_text(text, max_width, 7)

    svg = f'''<svg width="100%" height="100%" viewBox="0 0 {svg_width} {svg_height}"
        xmlns="http://www.w3.org/2000/svg" style="background: #08101d; font-family: 'Syne', sans-serif;">

        <!-- Blueprint Grid Background -->
        <defs>
            <pattern id="smallGrid" width="10" height="10" patternUnits="userSpaceOnUse">
                <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#142236" stroke-width="0.5"/>
            </pattern>
            <pattern id="largeGrid" width="50" height="50" patternUnits="userSpaceOnUse">
                <rect width="50" height="50" fill="url(#smallGrid)"/>
                <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#1e3151" stroke-width="1.2"/>
            </pattern>
        </defs>
        <rect width="{svg_width}" height="{svg_height}" fill="url(#largeGrid)"/>

        <!-- Title -->
        <text x="{svg_width/2}" y="32" text-anchor="middle" fill="#00d3a8" font-size="20" font-family="Syne" font-weight="700">
            ARCHITECTURAL FLOOR PLAN
        </text>

        <!-- Plot Boundary -->
        <rect x="{margin}" y="{margin}" width="{plot_width*scale}" height="{plot_length*scale}"
            fill="none" stroke="#24b483" stroke-width="2"/>
    '''

    for idx, room in enumerate(rooms):
        x_svg = margin + room.x * scale
        y_svg = margin + room.y * scale
        w_svg = room.w * scale
        h_svg = room.h * scale

        room_inset = 6
        label_box_width = max(40, w_svg - room_inset * 2)
        label_box_height = max(20, h_svg * 0.28)
        label_text = room.name.upper()
        label_font, label_lines = choose_font_and_lines(label_text, label_box_width, label_box_height)

        dim_text = f"{room.w:.0f}' x {room.h:.0f}'"
        dim_font = max(7, min(10, label_font * 0.72))

        label_area_height = len(label_lines) * label_font * 1.2 + dim_font + 8
        label_area_y = y_svg + max(room_inset, (h_svg - label_area_height) / 2)

        if room.furniture:
            furniture_centers = [(item['y'] + item['h'] / 2) * scale + y_svg for item in room.furniture]
            avg_furniture_y = sum(furniture_centers) / len(furniture_centers)
            room_center_y = y_svg + h_svg / 2
            if avg_furniture_y > room_center_y + 4:
                label_area_y = y_svg + room_inset
            elif avg_furniture_y < room_center_y - 4:
                label_area_y = y_svg + h_svg - label_area_height - room_inset
            label_area_y = min(max(label_area_y, y_svg + room_inset), y_svg + h_svg - label_area_height - room_inset)

        label_group_y = label_area_y + label_font
        dim_y = label_area_y + len(label_lines) * label_font * 1.2 + 6 + dim_font / 2

        svg += f'''
        <defs>
            <clipPath id="clip-room-{idx}">
                <rect x="{x_svg + 1}" y="{y_svg + 1}" width="{max(0, w_svg - 2)}" height="{max(0, h_svg - 2)}"/>
            </clipPath>
        </defs>
        <g clip-path="url(#clip-room-{idx})">
            <rect x="{x_svg}" y="{y_svg}" width="{w_svg}" height="{h_svg}"
                fill="{room.color}" stroke="#ecf0f1" stroke-width="3" rx="4"/>
            <rect x="{x_svg + 2}" y="{y_svg + 2}" width="{w_svg - 4}" height="{h_svg - 4}"
                fill="none" stroke="#7f8c9a" stroke-width="1" stroke-dasharray="6,4"/>
        '''

        for item in room.furniture:
            fx = x_svg + item['x'] * scale
            fy = y_svg + item['y'] * scale
            fw = item['w'] * scale
            fh = item['h'] * scale
            if item['type'] == "bed":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#bdc3c7" stroke-width="1.4" rx="3"/>'
                svg += f'<line x1="{fx + 4}" y1="{fy + fh * 0.35}" x2="{fx + fw - 4}" y2="{fy + fh * 0.35}" stroke="#bdc3c7" stroke-width="0.9"/>'
            elif item['type'] == "wardrobe":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#95a5a6" stroke-width="1"/>'
                svg += f'<line x1="{fx + fw * 0.2}" y1="{fy}" x2="{fx + fw * 0.2}" y2="{fy + fh}" stroke="#95a5a6" stroke-width="0.5"/>'
            elif item['type'] == "sofa":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#3a8ee6" stroke-width="1.5" rx="3"/>'
            elif item['type'] == "tv":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#ecf0f1" stroke="#2c3e50" stroke-width="1"/>'
            elif item['type'] == "table":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#f1c40f" stroke-width="1.2"/>'
                svg += f'<circle cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="{min(6, fw / 6)}" fill="none" stroke="#f1c40f" stroke-width="0.9"/>'
            elif item['type'] == "counter":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#bdc3c7" stroke-width="1.3"/>'
            elif item['type'] == "toilet":
                svg += f'<ellipse cx="{fx + fw / 2}" cy="{fy + fh / 2}" rx="{fw / 2}" ry="{fh / 2}" fill="none" stroke="#bdc3c7" stroke-width="1.4"/>'
            elif item['type'] == "sink":
                svg += f'<circle cx="{fx + fw / 2}" cy="{fy + fh / 2}" r="{min(fw, fh) / 2}" fill="none" stroke="#bdc3c7" stroke-width="1.4"/>'
            elif item['type'] == "shower":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#bdc3c7" stroke-width="1" stroke-dasharray="2,2"/>'
            elif item['type'] == "chair":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#f1c40f" stroke-width="1"/>'
            elif item['type'] == "desk":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#95a5a6" stroke-width="1.2"/>'
            elif item['type'] == "bookshelf":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#7f8c9a" stroke-width="1"/>'
            elif item['type'] == "stove":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#e74c3c" stroke-width="1"/>'
            elif item['type'] == "refrigerator":
                svg += f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="#3498db" stroke-width="1"/>'

        for op in room.openings:
            if op['type'] == "window":
                wx, wy, ww, wh = 0, 0, 0, 0
                if op['wall'] == 'left':
                    wx, wy, ww, wh = x_svg - 2, y_svg + op['pos'] * scale - 10, 4, 20
                elif op['wall'] == 'right':
                    wx, wy, ww, wh = x_svg + w_svg - 2, y_svg + op['pos'] * scale - 10, 4, 20
                elif op['wall'] == 'top':
                    wx, wy, ww, wh = x_svg + op['pos'] * scale - 10, y_svg - 2, 20, 4
                elif op['wall'] == 'bottom':
                    wx, wy, ww, wh = x_svg + op['pos'] * scale - 10, y_svg + h_svg - 2, 20, 4
                svg += f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#00e5b0"/>'
            elif op['type'] == "door":
                dx, dy = x_svg + op['x'] * scale, y_svg + op['y'] * scale
                svg += f'<path d="M {dx} {dy} A 15 15 0 0 1 {dx + 15} {dy - 15} L {dx} {dy - 15} Z" fill="none" stroke="#f39c12" stroke-width="1.5"/>'

        svg += f'''
            <text x="{x_svg + w_svg / 2}" y="{label_group_y}" text-anchor="middle" fill="#ecf0f1" font-size="{label_font}" font-family="Syne" font-weight="600">
        '''
        for line_index, line in enumerate(label_lines):
            y_line = label_group_y + line_index * label_font * 1.2
            svg += f'<tspan x="{x_svg + w_svg / 2}" y="{y_line}">{line}</tspan>'
        svg += f'''</text>
            <text x="{x_svg + w_svg / 2}" y="{dim_y}" text-anchor="middle" fill="#95a5a6" font-size="{dim_font}" font-family="JetBrains Mono" font-weight="500">
                {dim_text}
            </text>
        </g>
        '''

    svg += f'''
        <text x="{margin + plot_width * scale / 2}" y="{margin + plot_length * scale + 28}"
            text-anchor="middle" fill="#dde8f5" font-size="12" font-family="JetBrains Mono" font-weight="600">
            {plot_width:.0f} ft × {plot_length:.0f} ft | Scale 1:{int(max(1, round(1 / scale * 4.5)))}
        </text>
        <text x="{margin}" y="{svg_height - 8}" fill="#5a7090" font-size="8" font-family="JetBrains Mono">
            ■ Room Boundaries | ─ Windows | ⌢ Door Swings | 🚗 Parking
        </text>
    </svg>
    '''
    return svg
