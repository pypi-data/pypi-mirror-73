# Defaults
DEVELOPMENT_SERVER = "https://redfish-development.merantix.de"

API_VERSION = 1

# Urls
API_BASE_URL = f"/public_api/v{API_VERSION}"
API_LOGIN_URL = f"{API_BASE_URL}/auth/login"
API_QUERY_URL = f"{API_BASE_URL}/segments"

METRICS_INFO_URL = f"{API_BASE_URL}/metrics_info"
SEGMENT_GPS_COORDINATES_URL = f"{API_BASE_URL}/drives/<drive_id>/gps/coordinates"
SEGMENT_CAMERA_SENSORS_NAMES_URL = f"{API_BASE_URL}/drives/<drive_id>/cameras/list"
SEGMENT_CAMERA_FRAMES_URL = f"{API_BASE_URL}/drives/<drive_id>/cameras/<camera_id>"
SEGMENT_METADATA_URL = f"{API_BASE_URL}/drives/<drive_id>/metadata"
