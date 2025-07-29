import geoip2.database
import logging
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeoIPProcessor:
    def __init__(self, geoip_db_path: str = "GeoLite2-City.mmdb"):
        try:
            self.reader = geoip2.database.Reader(geoip_db_path)
        except FileNotFoundError:
            logger.error(f"GeoIP database not found at {geoip_db_path}")
            raise

    def get_location(self, ip_address: str) -> Optional[Dict[str, str]]:
        """Returns geolocation data for an IP or None if failed."""
        try:
            response = self.reader.city(ip_address)
            return {
                "ip": ip_address,
                "country": response.country.name,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "isp": "Unknown"  # MaxMind doesn't provide ISP; use IPAPI for this.
            }
        except Exception as e:
            logger.warning(f"Failed to process IP {ip_address}: {str(e)}")
            return None

    def __del__(self):
        if hasattr(self, "reader"):
            self.reader.close()