import requests
from datetime import datetime
import geoip2.database
import sqlite3
from collections import defaultdict

class TrojanSensor:
    def __init__(self):
        self.geoip_reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        self.conn = sqlite3.connect('threatmap.db')
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trojan_attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_ip TEXT,
                source_country TEXT,
                source_city TEXT,
                target_ip TEXT,
                target_country TEXT,
                target_city TEXT,
                timestamp DATETIME,
                variant TEXT,
                severity INTEGER
            )
        ''')
        self.conn.commit()
        
    def process_log_entry(self, log_entry):
        # Parse log entry (format depends on your sensor data)
        source_ip = log_entry['source_ip']
        target_ip = log_entry['target_ip']
        variant = log_entry.get('variant', 'Unknown')
        severity = log_entry.get('severity', 2)  # 1-3 scale
        
        try:
            source_loc = self.geoip_reader.city(source_ip)
            target_loc = self.geoip_reader.city(target_ip)
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO trojan_attacks 
                (source_ip, source_country, source_city, target_ip, target_country, target_city, timestamp, variant, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                source_ip,
                source_loc.country.name,
                source_loc.city.name,
                target_ip,
                target_loc.country.name,
                target_loc.city.name,
                datetime.now(),
                variant,
                severity
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error processing entry: {e}")
            return False

    def get_recent_attacks(self, hours=24):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM trojan_attacks 
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
        ''', (f'-{hours} hours',))
        return cursor.fetchall()