"""InOutScan"""
import json
import sqlite3
import sys
import time
import binascii
from gpiozero import pi_info
import requests
import nfc
import pyudev

from . import __version__


class InOutNfc():
    """
    InOutNfc - Publish incoming chip-ids to an API
    """

    def __init__(self):
        self.database = 'inout_scan.db'
        self.init_local_database()
        self.usb_port = None
        self.api_details = None
        self.scanner = None

    def set_api(self, api_details):
        """
        Set API configuration
        """
        self.api_details = api_details

    def set_usb_port(self, usb_label):
        """
        Set usb port
        """
        self.usb_port = None
        all_ports = {
            '2B':  {
                'tl': '1-1.2',
                'bl': '1-1.3',
                'tr': '1-1.4',
                'br': '1-1.5'
                },
            '3B+': {
                'tl': '1-1.1.2',
                'bl': '1-1.1.3',
                'tr': '1-1.3',
                'br': '1-1.2'
                },
            }

        try:
            ports = all_ports[pi_info().model]
        except:
            print("No usb port information available of this raspberry pi model")
            return

        try:
            device_path = ports[usb_label]
        except:
            print("Could not find USB device path for given connector location")

        self.usb_port = self.get_usb_address(device_path, '72f/2200/214')

    def get_usb_address(self, usbport, product):
        """
        Determine the usb address given the usb device path
        """
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb', DEVTYPE='usb_device'):
            if device.get('PRODUCT') == product:
                devpath = device.get('DEVPATH')
                if devpath.endswith('/' + usbport):
                    return "usb:" + device.get('BUSNUM') + ":" + device.get('DEVNUM')
        return None


    def set_scanner(self, scanner):
        """
        Set scanner name
        """
        self.scanner = scanner

    def init_local_database(self):
        """
        creates a local sqlite database
        """
        try:
            self.sqlite_connection = sqlite3.connect(self.database)
            sqlite_create_table_query = '''CREATE TABLE inout_events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                badge TEXT NOT NULL,
                                timestamp INTEGER,
                                scanner TEXT NOT NULL,
                                sentToApi BOOLEAN
                                );'''
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            print("Successfully created the "
                  "sqlite database {}".format(self.database))
        except sqlite3.Error:
            pass

    def on_connect(self, tag):
        """
        Handle badge connect event
        """
        identifier = binascii.hexlify(tag.identifier)
        data = {
            'badge': identifier.decode("utf-8"),
            'timestamp': int(time.time()),
            'scanner': self.scanner,
        }
        sent_to_api = self.publish(data)
        data.update({'sentToApi': sent_to_api})
        self.write_to_localdb(data)
        return True

    def scan(self):
        """Handle presented badges"""
        config = {
                'interval': 0.35,
                'beep-on-connect': True,
                'on-connect': self.on_connect
                }

        clf = nfc.ContactlessFrontend(self.usb_port)

        while True:
            ret = clf.connect(rdwr=config)

            if ret is None:
                pass
            elif not ret:
                print("NFC connection terminated due to an exception")
                break
            else:
                pass
        clf.close()



    def publish(self, data):
        """Publish string to API"""
        success = False
        try:
            response = requests.post(
                url=self.api_details['api_url'],
                headers={
                    'Authorization': 'Basic {}'.format(
                        self.api_details['api_key']),
                    'User-Agent': 'inout_scan/{version}'.format(
                        version=__version__),
                    'Content-type': 'application/json'},
                data=json.dumps(data),
                timeout=1
                )
            response.raise_for_status()
            success = True
        except requests.exceptions.ConnectionError:
            # failed to submit data
            print("Could not connect to API")
            success = False
        except requests.exceptions.HTTPError:
            # failed to submit data
            print("An HTTP error occurred")
            success = False
        except Exception as e:
            print("Something went wrong", e)
            success = False

        return success

    def write_to_localdb(self, data):
        """
        write events to a local sqlite database
        """
        if "id" in data:
            query = """UPDATE inout_events
                       SET
                          sentToApi = 1
                       WHERE
                          id = :id
                    """
        else:
            query = """INSERT INTO inout_events
                          (badge,  timestamp,  scanner,  sentToApi)
                       VALUES
                          (:badge, :timestamp, :scanner, :sentToApi)
                    """

        cursor = self.sqlite_connection.cursor()
        cursor.execute(query, data)
        self.sqlite_connection.commit()


def main():
    """
    main
    """
    sys.exit(0)


if __name__ == "__main__":
    main()
