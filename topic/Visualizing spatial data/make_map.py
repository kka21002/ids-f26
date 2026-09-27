import geopandas as gpd
import pandas as pd

# Load county boundaries
counties = gpd.read_file(
    "data/county_boundaries/cb_2020_us_county_500k.shp"
)

# Keep only Connecticut
ct_counties = counties[counties["STATEFP"] == "09"].copy()

# Load population and land-area data
data = pd.read_csv(
    "data/ct_county_data.csv",
    dtype={"GEOID": str}
)

# Make sure GEOID is treated as text
ct_counties["GEOID"] = ct_counties["GEOID"].astype(str)
data["GEOID"] = data["GEOID"].astype(str)

# Combine the geographic and population data
ct_counties = ct_counties.merge(data, on="GEOID")

# Convert land area from square meters to square miles
ct_counties["land_area_sq_mi"] = (
    ct_counties["land_area_sq_m"] / 2_589_988.11
)

# Calculate population density
ct_counties["population_density"] = (
    ct_counties["population"] / ct_counties["land_area_sq_mi"]
)

print(ct_counties[["county", "population", "population_density"]])

import matplotlib.pyplot as plt

# Create the choropleth map
fig, ax = plt.subplots(figsize=(8, 8))

ct_counties.plot(
    column="population_density",
    ax=ax,
    legend=True,
    edgecolor="black",
    linewidth=0.8
)

ax.set_title("Connecticut Population Density, 2020")
ax.set_axis_off()

plt.tight_layout()
plt.savefig("ct_population_density.png", dpi=300)
plt.show()