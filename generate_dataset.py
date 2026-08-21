import pandas as pd
import numpy as np

np.random.seed(42)

n = 1200  # number of rows

cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai"]
project_types = ["Residential", "Commercial", "Industrial"]
material_quality = np.random.choice(["Low", "Medium", "High"])
labor_cost_index = np.random.uniform(0.8, 1.3)

city_multiplier = {
    "Delhi": 1.1,
    "Mumbai": 1.3,
    "Bangalore": 1.2,
    "Hyderabad": 1.05,
    "Pune": 1.08,
    "Chennai": 1.12
}

type_rate = {
    "Residential": 2500,
    "Commercial": 3500,
    "Industrial": 2200
}

data = []

for _ in range(n):
    size = np.random.randint(1, 10000)   # sqm
    floors = np.random.randint(1, 12)
    city = np.random.choice(cities)
    project_type = np.random.choice(project_types)

    base_rate = type_rate[project_type]
    multiplier = city_multiplier[city]

    # realistic cost formula + noise
    cost = size * floors * base_rate * multiplier
    noise = np.random.uniform(0.9, 1.15)   # variation
    cost = cost * noise

    data.append([size, floors, project_type, city, int(cost)])

df = pd.DataFrame(data, columns=["size", "floors", "project_type", "city", "cost"])

df.to_csv("construction_dataset.csv", index=False)

print("✅ Dataset generated: construction_dataset.csv")