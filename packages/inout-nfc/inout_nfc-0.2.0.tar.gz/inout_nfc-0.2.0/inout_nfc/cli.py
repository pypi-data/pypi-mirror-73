'''
Console script for inout_scan.
'''

# import sys
import click
from inout_nfc import inout_nfc

DEFAULT_USB_PORT = 'usb'


@click.group()
@click.version_option()
def main():
    """Gather bar codes from a scanner connected to the serial port and pass
       them to the InOut API. A local cache is maintained to be able to handle
       communication problems. Use the flush command to communicate unsubmitted
       bar codes."""


@main.command()
@click.option('--usb_port',
              default=DEFAULT_USB_PORT,
              type=click.Choice(['tl', 'bl', 'tr', 'br'], case_sensitive=False),
              help='USB port (top left, bottom left, etc)  the NFC reader is'
              ' connected to.')
@click.option('--api_url',
              required=True,
              help='InOut API url.')
@click.option('--api_key',
              help='InOut API key.')
@click.option('--scanner',
              required=True,
              help='Unique scanner name, ie: "reception1".')
def scan(usb_port, api_url, api_key, scanner):
    """Listen for chip cards to be scanned with an nfc reader/writer
    and make an API call to InOut for each detected chip-id."""
    app = inout_nfc.InOutNfc()
    app.set_api(api_details={
        'api_url': api_url,
        'api_key': api_key,
    })
    app.set_scanner(scanner)
    app.set_usb_port(usb_port)
    app.scan()


if __name__ == '__main__':
    main(auto_envvar_prefix='INOUT')
