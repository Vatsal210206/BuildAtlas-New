REQUIREMENT_SCHEMAS = {
    "house": {
        "sections": [
            {"title": "🧍 Family & Lifestyle", "fields": [
                {"key": "family_size", "label": "Family size", "type": "number", "min": 1, "max": 12, "default": 4, "required": True},
                {"key": "family_composition", "label": "Composition", "type": "text", "default": "2 adults, 2 kids, 1 elderly parent", "required": False},
                {"key": "floors", "label": "Number of floors", "type": "number", "min": 1, "max": 4, "default": 2, "required": True},
                {"key": "work_from_home", "label": "Dedicated work-from-home setup", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
            {"title": "🛏 Accommodation", "fields": [
                {"key": "bedrooms", "label": "Bedrooms", "type": "number", "min": 1, "max": 8, "default": 3, "required": True},
                {"key": "bathrooms", "label": "Bathrooms", "type": "number", "min": 1, "max": 6, "default": 2, "required": True},
                {"key": "parking", "label": "Parking bays", "type": "number", "min": 1, "max": 6, "default": 2, "required": True},
                {"key": "garden_priority", "label": "Garden/open space priority", "type": "slider", "min": 0, "max": 10, "default": 6, "required": False},
            ]},
            {"title": "💸 Budget & Style", "fields": [
                {"key": "budget_range", "label": "Budget range", "type": "select", "options": ["Mid", "Premium", "Luxury"], "default": "Premium", "required": False},
                {"key": "style", "label": "Preferred style", "type": "select", "options": ["Modern", "Traditional", "Minimalist", "Indo-colonial"], "default": "Modern", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "study_room", "label": "Study/office nook", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
            {"key": "guest_room", "label": "Guest room", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
        ],
    },
    "villa": {
        "sections": [
            {"title": "🏡 Villa Brief", "fields": [
                {"key": "bedrooms", "label": "Bedrooms", "type": "number", "min": 3, "max": 10, "default": 4, "required": True},
                {"key": "bathrooms", "label": "Bathrooms", "type": "number", "min": 2, "max": 8, "default": 4, "required": True},
                {"key": "car_bays", "label": "Car bays", "type": "number", "min": 2, "max": 8, "default": 4, "required": True},
                {"key": "pool", "label": "Swimming pool", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
            {"title": "🌿 Outdoor Amenities", "fields": [
                {"key": "garden_extent", "label": "Landscaped garden extent", "type": "slider", "min": 0, "max": 10, "default": 7, "required": False},
                {"key": "home_theatre", "label": "Home theatre", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "gym", "label": "Private gym", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "guest_suite", "label": "Guest suite", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "staff_quarters", "label": "Staff quarters", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
            {"key": "terrace_use", "label": "Terrace / rooftop use", "type": "text", "default": "Garden leisure and sunset lounge", "required": False},
        ],
    },
    "duplex": {
        "sections": [
            {"title": "🏘️ Duplex Planning", "fields": [
                {"key": "family_mode", "label": "Two-family or single-family acros floors", "type": "select", "options": ["Single family", "Two family"], "default": "Single family", "required": False},
                {"key": "independent_entrances", "label": "Independent entrances per floor", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "shared_utilities", "label": "Shared utilities", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
                {"key": "bedrooms_per_floor", "label": "Bedroom split across floors", "type": "text", "default": "2 on first floor, 2 on second floor", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "parking", "label": "Parking bays", "type": "number", "min": 1, "max": 6, "default": 2, "required": True},
            {"key": "style", "label": "Preferred style", "type": "select", "options": ["Modern", "Traditional", "Minimalist"], "default": "Modern", "required": False},
        ],
    },
    "apartment": {
        "sections": [
            {"title": "🏢 Apartment Mix", "fields": [
                {"key": "units_per_floor", "label": "Units per floor", "type": "number", "min": 2, "max": 10, "default": 4, "required": True},
                {"key": "total_floors", "label": "Total floors", "type": "number", "min": 2, "max": 30, "default": 8, "required": True},
                {"key": "parking_ratio", "label": "Parking ratio per unit", "type": "number", "min": 0.5, "max": 3.0, "default": 1.0, "required": True},
                {"key": "security_gate", "label": "Security / gate provisions", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
            {"title": "✨ Common Amenities", "fields": [
                {"key": "lobby", "label": "Lobby", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "lift", "label": "Lift", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "clubhouse", "label": "Clubhouse", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
                {"key": "gym", "label": "Gym", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "kids_area", "label": "Kids play area", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
            {"key": "visitor_parking", "label": "Visitor parking", "type": "number", "min": 0, "max": 20, "default": 4, "required": True},
        ],
    },
    "resort": {
        "sections": [
            {"title": "🌴 Resort Capacity", "fields": [
                {"key": "cottages", "label": "Number of cottages / villas", "type": "number", "min": 1, "max": 30, "default": 3, "required": True},
                {"key": "guest_capacity", "label": "Guest capacity target", "type": "number", "min": 10, "max": 500, "default": 40, "required": True},
                {"key": "restaurant_capacity", "label": "Restaurant seating capacity", "type": "number", "min": 20, "max": 400, "default": 60, "required": True},
                {"key": "parking_capacity", "label": "Parking capacity", "type": "number", "min": 8, "max": 150, "default": 24, "required": True},
            ]},
            {"title": "💧 Guest Amenities", "fields": [
                {"key": "pool_main", "label": "Main pool", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "pool_kids", "label": "Kids pool", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
                {"key": "conference_capacity", "label": "Conference / banquet capacity", "type": "number", "min": 20, "max": 300, "default": 50, "required": True},
                {"key": "spa", "label": "Spa / wellness block", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "staff_quarters", "label": "Staff quarters", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            {"key": "landscape_style", "label": "Landscape style", "type": "select", "options": ["Beachfront", "Forest", "Hillside", "Lakefront"], "default": "Beachfront", "required": False},
        ],
    },
    "commercial": {
        "sections": [
            {"title": "🛍 Commercial Mix", "fields": [
                {"key": "units_count", "label": "Shops / units", "type": "number", "min": 1, "max": 50, "default": 10, "required": True},
                {"key": "shop_frontage", "label": "Typical shop frontage size", "type": "text", "default": "15 ft wide frontage", "required": False},
                {"key": "parking", "label": "Parking provision", "type": "number", "min": 0, "max": 100, "default": 20, "required": True},
                {"key": "loading_bay", "label": "Loading / unloading bay", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
            {"title": "⚙️ Services", "fields": [
                {"key": "food_court", "label": "Food court", "type": "select", "options": ["Yes", "No"], "default": "No", "required": False},
                {"key": "signage_zone", "label": "Signage / facade zone", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "fire_egress", "label": "Fire safety egress requirement", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            ]},
        ],
        "advanced": [],
    },
    "office": {
        "sections": [
            {"title": "💼 Office Capacity", "fields": [
                {"key": "headcount", "label": "Target headcount", "type": "number", "min": 10, "max": 600, "default": 120, "required": True},
                {"key": "open_plan_ratio", "label": "Open-plan vs cabin ratio", "type": "slider", "min": 0, "max": 10, "default": 6, "required": False},
                {"key": "meeting_rooms", "label": "Meeting rooms", "type": "number", "min": 1, "max": 20, "default": 4, "required": True},
                {"key": "parking_ratio", "label": "Parking per employee ratio", "type": "number", "min": 0.1, "max": 2.0, "default": 0.4, "required": True},
            ]},
            {"title": "🧰 Core Needs", "fields": [
                {"key": "pantry", "label": "Pantry / cafeteria", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "server_room", "label": "Server / IT room", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
                {"key": "floors", "label": "Floors", "type": "number", "min": 1, "max": 20, "default": 4, "required": True},
            ]},
        ],
        "advanced": [],
    },
    "warehouse": {
        "sections": [
            {"title": "🏭 Warehouse Logic", "fields": [
                {"key": "storage_split", "label": "Storage vs admin split", "type": "slider", "min": 0, "max": 10, "default": 7, "required": False},
                {"key": "dock_count", "label": "Loading dock count", "type": "number", "min": 1, "max": 12, "default": 3, "required": True},
                {"key": "clear_span", "label": "Clear span requirement", "type": "number", "min": 20, "max": 80, "default": 40, "required": True},
                {"key": "rack_type", "label": "Racking type", "type": "select", "options": ["Selective", "Drive-in", "Push-back"], "default": "Selective", "required": False},
            ]},
        ],
        "advanced": [
            {"key": "fire_safety", "label": "Fire safety arrangements", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
            {"key": "ventilation", "label": "Ventilation requirement", "type": "select", "options": ["Yes", "No"], "default": "Yes", "required": False},
        ],
    },
}


def get_requirement_schema(project_type: str):
    return REQUIREMENT_SCHEMAS.get(project_type, REQUIREMENT_SCHEMAS["house"])
