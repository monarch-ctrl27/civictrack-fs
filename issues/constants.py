"""
Shared reference data for the CivicTrack FS app.

Keeping this in one place means the model choices, the AI-assisted
categorisation helper (ai.py), the map layout, and the chart colours
(charts.py) all stay in sync automatically.
"""

# Each category has an id (stored in the DB), a human label, a colour used
# for badges/charts, and a list of keywords used by the lightweight
# rule-based classifier in ai.py.
CATEGORIES = [
    {
        "id": "roads",
        "label": "Roads & Potholes",
        "color": "#A6532D",
        "keywords": [
            "pothole", "potholes", "road", "roads", "tar", "tarred",
            "speed bump", "pavement", "street", "crack", "gravel",
        ],
    },
    {
        "id": "water",
        "label": "Water & Sanitation",
        "color": "#3B6E91",
        "keywords": [
            "water", "leak", "leaking", "burst", "pipe", "sewage", "sewer",
            "tap", "drain", "sanitation", "toilet",
        ],
    },
    {
        "id": "electricity",
        "label": "Electricity & Power",
        "color": "#C6921B",
        "keywords": [
            "electricity", "power", "outage", "transformer", "cable",
            "streetlight", "streetlights", "light", "lights", "substation",
            "load shedding", "loadshedding",
        ],
    },
    {
        "id": "safety",
        "label": "Safety & Crime",
        "color": "#8C2F39",
        "keywords": [
            "crime", "theft", "stolen", "robbery", "unsafe", "hijack",
            "mugging", "gang", "break-in", "breakin", "assault", "danger",
            "dangerous",
        ],
    },
    {
        "id": "dumping",
        "label": "Illegal Dumping",
        "color": "#6B7F3A",
        "keywords": [
            "dump", "dumping", "rubbish", "trash", "litter", "waste",
            "garbage", "refuse", "landfill",
        ],
    },
    {
        "id": "infra",
        "label": "Infrastructure & Facilities",
        "color": "#6B5B95",
        "keywords": [
            "building", "facility", "clinic", "hall", "park", "fence",
            "bridge", "sidewalk", "playground", "stadium", "library",
        ],
    },
    {
        "id": "other",
        "label": "Other / Service Delivery",
        "color": "#566573",
        "keywords": [],
    },
]

CATEGORY_CHOICES = [(c["id"], c["label"]) for c in CATEGORIES]
CATEGORY_MAP = {c["id"]: c for c in CATEGORIES}

# Real Free State district municipalities, with an illustrative bounding
# box (x1, y1, x2, y2) used to lay them out on the 600x500 SVG map and to
# scatter each report's marker within its district.
DISTRICTS = [
    {
        "id": "feziledabi",
        "name": "Fezile Dabi",
        "towns": "Sasolburg \u00b7 Parys \u00b7 Kroonstad",
        "box": (150, 26, 420, 150),
    },
    {
        "id": "lejweleputswa",
        "name": "Lejweleputswa",
        "towns": "Welkom \u00b7 Bothaville \u00b7 Odendaalsrus",
        "box": (20, 150, 230, 330),
    },
    {
        "id": "thabomofutsanyana",
        "name": "Thabo Mofutsanyana",
        "towns": "Bethlehem \u00b7 Harrismith \u00b7 Phuthaditjhaba",
        "box": (390, 140, 580, 330),
    },
    {
        "id": "mangaung",
        "name": "Mangaung Metro",
        "towns": "Bloemfontein \u00b7 Botshabelo \u00b7 Thaba Nchu",
        "box": (235, 235, 400, 375),
    },
    {
        "id": "xhariep",
        "name": "Xhariep",
        "towns": "Trompsburg \u00b7 Zastron \u00b7 Fauresmith",
        "box": (120, 375, 420, 480),
    },
]

DISTRICT_CHOICES = [(d["id"], d["name"]) for d in DISTRICTS]
DISTRICT_MAP = {d["id"]: d for d in DISTRICTS}

# Ordered so templates can render a simple progress-style status list.
STATUS_CHOICES = [
    ("reported", "Reported"),
    ("under_review", "Under Review"),
    ("in_progress", "In Progress"),
    ("resolved", "Resolved"),
]
STATUS_COLORS = {
    "reported": "#2B4570",
    "under_review": "#C6921B",
    "in_progress": "#A6532D",
    "resolved": "#4E7A54",
}
STATUS_SOFT_COLORS = {
    "reported": "#DCE4F0",
    "under_review": "#F3E3B8",
    "in_progress": "#F0DCCF",
    "resolved": "#DDEADB",
}

AUTO_CATEGORY_VALUE = "auto"
