import csv
from convertor.temperature import (
    celsius_to_fahrenheit as to_F,
    fahrenheit_to_celsius as to_C
)
from convertor.distance import (
    meters_to_feet as to_ft,
    feet_to_meters as to_m
)


def convert_data(input_file, output_file, target_temp_unit="C", target_dist_unit="m"):
    """
    Converts temperature and distance measurements in a CSV file to specified units.

    This function reads a CSV file with columns for date, distance, and temperature readings.
    It converts distances between meters and feet and temperatures between Celsius and Fahrenheit
    according to the specified target units. The converted data is then written to a new CSV file.

    The input CSV format should be:
        Date,Distance,Reading
        2024-01-01,"41m","10°C"
        ...
    where Distance can end in 'm' for meters or 'ft' for feet, and Reading ends in '°C' or '°F'.

    Parameters:
    - input_file (str): The path to the input CSV file containing the original measurements.
    - output_file (str): The path where the converted measurements will be written.
    - target_temp_unit (str, optional): The target temperature unit ('C' for Celsius or 'F' for Fahrenheit).
                                        Defaults to 'C'.
    - target_dist_unit (str, optional): The target distance unit ('m' for meters or 'f' for feet).
                                        Defaults to 'm'.

    Returns:
    - None: The function writes directly to a file and does not return any value.

    Example usage:
    convert_data('input.csv', 'output_converted.csv', 'C', 'm')

    Note:
    The function handles encoding issues related to special characters in temperature readings and
    ensures correct parsing of distance units that might be incorrectly formatted in the input data.
    It assumes that the input file is UTF-8 encoded to properly handle special characters like the degree symbol.
    """

    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        writer.writerow(header)

        # Extract needed values and units
        for row in reader:
            date, distance, reading = row
            if distance[-2:].lower() == "ft":
                dist_value, dist_unit = distance[:-2], "ft"
            else:
                dist_value, dist_unit = distance[:-1], distance[-1]

            temp_value, temp_unit = reading.split("°")
            # Ensure unit is correctly attached and stripped of whitespace
            temp_unit = "°" + temp_unit.strip()

            # Convert distance
            if target_dist_unit == "m" and dist_unit == "ft":
                converted_distance = to_m(float(dist_value))
                new_distance = f"{converted_distance:.2f}m"
            elif target_dist_unit == "f" and dist_unit == "m":
                converted_distance = to_ft(float(dist_value))
                new_distance = f"{converted_distance:.2f}ft"
            else:
                new_distance = distance

            # Convert temperature
            if target_temp_unit == "C" and "F" in temp_unit:
                converted_temp = to_C(float(temp_value))
                new_reading = f"{converted_temp:.2f}°C"
            elif target_temp_unit == "F" and "C" in temp_unit:
                converted_temp = to_F(float(temp_value))
                new_reading = f"{converted_temp:.2f}°F"
            else:
                new_reading = reading

            writer.writerow([date, new_distance, new_reading])

# Example usage
# convert_data('input.csv', 'output_converted.csv', 'C', 'm')
