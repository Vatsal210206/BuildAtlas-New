PLOT_DIMENSION_BOUNDS = {
    "house": {"min": 20, "max": 300},
    "villa": {"min": 30, "max": 2500},
    "duplex": {"min": 20, "max": 300},
    "apartment": {"min": 40, "max": 3000},
    "resort": {"min": 100, "max": 5000},
    "commercial": {"min": 30, "max": 3000},
    "office": {"min": 30, "max": 3000},
    "warehouse": {"min": 50, "max": 5000},
}


PROJECT_TYPES = {
    "house": {
        "key": "house",
        "name": "House",
        "icon": "🏠",
        "description": "Family home concept with personal and shared zones",
        "schema": "house",
    },
    "villa": {
        "key": "villa",
        "name": "Villa",
        "icon": "🏡",
        "description": "Luxury private residence with amenity zones",
        "schema": "villa",
    },
    "duplex": {
        "key": "duplex",
        "name": "Duplex",
        "icon": "🏘️",
        "description": "Multi-level family dwelling with two stacked units",
        "schema": "duplex",
    },
    "apartment": {
        "key": "apartment",
        "name": "Apartment",
        "icon": "🏢",
        "description": "Multi-unit residential building concept",
        "schema": "apartment",
    },
    "resort": {
        "key": "resort",
        "name": "Resort",
        "icon": "🌴",
        "description": "Boutique hospitality experience with privacy zoning",
        "schema": "resort",
    },
    "commercial": {
        "key": "commercial",
        "name": "Commercial Building",
        "icon": "🏬",
        "description": "Retail and service-led multi-use building concept",
        "schema": "commercial",
    },
    "office": {
        "key": "office",
        "name": "Office",
        "icon": "💼",
        "description": "Workplace zoning for people, meetings, and services",
        "schema": "office",
    },
    "warehouse": {
        "key": "warehouse",
        "name": "Warehouse",
        "icon": "🏭",
        "description": "Storage and logistics planning with circulation clarity",
        "schema": "warehouse",
    },
}


def get_project_type_config(project_type: str):
    return PROJECT_TYPES.get(project_type, PROJECT_TYPES["house"])


def get_plot_dimension_bounds(project_type: str):
    return PLOT_DIMENSION_BOUNDS.get(project_type, PLOT_DIMENSION_BOUNDS["house"])
