import rasterio

# Function to get value from GeoTIFF based on latitude and longitude
def get_value_by_lat_lon(file_path, latitude, longitude):
    try:
        with rasterio.open(file_path) as dataset:
            # Get bounds and check if coordinates are within bounds
            bounds = dataset.bounds
            if not (bounds.left <= longitude <= bounds.right and bounds.bottom <= latitude <= bounds.top):
                return f"Coordinates ({latitude}, {longitude}) are out of bounds."

            # Get NoData value
            nodata_value = dataset.nodata

            # Convert latitude and longitude to row and column indices
            row, col = dataset.index(longitude, latitude)

            # Check if row and column are valid
            if 0 <= row < dataset.height and 0 <= col < dataset.width:
                # Read the value from the raster
                value = dataset.read(1)[row, col]
                return f"Value at ({latitude}, {longitude}): {value}" if value != nodata_value else "Value is NoData."
            else:
                return f"Coordinates ({latitude}, {longitude}) are out of the raster bounds."
    except Exception as e:
        return f"Error: {e}"

# Test coordinates for both GeoTIFFs
test_coordinates = [
    (39.7, -104.9),  # Within bounds for both files
    (39.68, -104.94),  # Within bounds for both files
    (40.0, -105.0),  # Out of bounds
]

file_1_path = "MYD11A1.061_QC_Day_doy2024228_aid0001.tif"
file_2_path = "MYD11A1.061_LST_Day_1km_doy2024228_aid0001.tif"

# Run tests for both files
results_file_1 = {f"Lat: {lat}, Lon: {lon}": get_value_by_lat_lon(file_1_path, lat, lon) for lat, lon in test_coordinates}
results_file_2 = {f"Lat: {lat}, Lon: {lon}": get_value_by_lat_lon(file_2_path, lat, lon) for lat, lon in test_coordinates}

print("Results 1: ", results_file_1)
print("Results 2: ", results_file_2)
