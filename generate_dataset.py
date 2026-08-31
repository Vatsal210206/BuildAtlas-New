import pandas as pd
import numpy as np

np.random.seed(42)

# Prototype training locations. Costs are synthetic and are not market rates.
cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Bangalore": (12.9716, 77.5946),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Ghaziabad": (28.6692, 77.4538),
    "Dehradun": (30.3165, 78.0322),
    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Vadodara": (22.3072, 73.1812),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Nagpur": (21.1458, 79.0882),
    "Patna": (25.5941, 85.1376),
    "Bhubaneswar": (20.2961, 85.8245),
    "Ranchi": (23.3441, 85.3096),
    "Guwahati": (26.1445, 91.7362),
    "Kochi": (9.9312, 76.2673),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Coimbatore": (11.0168, 76.9558),
    "Mysuru": (12.2958, 76.6394),
    "Vijayawada": (16.5062, 80.6480),
    "Visakhapatnam": (17.6868, 83.2185),
    "Chandigarh": (30.7333, 76.7794),
    "Amritsar": (31.6340, 74.8723),
    "Varanasi": (25.3176, 82.9739),
    "Agra": (27.1767, 78.0081),
}

n = 2400
project_types = ["Residential", "Commercial", "Industrial"]

type_rate = {
    "Residential": 2500,
    "Commercial": 3500,
    "Industrial": 2200
}

data = []

for _ in range(n):
    size = np.random.randint(1, 10000)   # sqm
    floors = np.random.randint(1, 12)
    city = np.random.choice(list(cities))
    latitude, longitude = cities[city]
    project_type = np.random.choice(project_types)

    base_rate = type_rate[project_type]
    # Synthetic geographic variation gives the prototype a learnable location signal.
    regional_factor = (
        1.0
        + 0.18 * (longitude - 78.0) / 14.0
        + 0.10 * (latitude - 20.0) / 13.0
    )

    cost = size * floors * base_rate * regional_factor
    noise = np.random.uniform(0.9, 1.15)   # variation
    cost = cost * noise

    data.append([size, floors, project_type, city, latitude, longitude, int(cost)])

df = pd.DataFrame(
    data,
    columns=["size", "floors", "project_type", "city", "latitude", "longitude", "cost"],
)

df.to_csv("construction_dataset.csv", index=False)

print("✅ Dataset generated: construction_dataset.csv")