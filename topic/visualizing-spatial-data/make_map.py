import geopandas as gpd
import pandas as pd

# Load the 2020 Connecticut-only county boundaries
ct_counties = gpd.read_file(
    "data/ct_county_boundaries/ct_counties_2020.shp"
)

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
fig.subplots_adjust(bottom=0.22)

cax = fig.add_axes([0.20, 0.11, 0.60, 0.025])

ct_counties.plot(
column="population_density",
ax=ax,
legend=True,
cax=cax,
edgecolor="black",
linewidth=0.8,
legend_kwds={
"orientation": "horizontal",
"label": "People per square mile",
"format": "%.0f"
}
)

cax.tick_params(labelsize=8)
cax.xaxis.label.set_size(9)

ax.set_title("Connecticut Population Density, 2020", fontsize=14, pad=12)
ax.set_axis_off()

plt.tight_layout()
plt.savefig("ct_population_density.png", dpi=300)
plt.show()