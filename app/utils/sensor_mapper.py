from app.sensors.mapping import SENSOR_MAPPING

def map_sensor_names(raw_sensors: dict):
    mapped = {}

    for key, value in raw_sensors.items():
        # If mapping exists → use human-readable name
        if key in SENSOR_MAPPING:
            mapped_name = SENSOR_MAPPING[key]
        else:
            # Otherwise → use the original key
            mapped_name = key

        mapped[mapped_name] = value

    return mapped
