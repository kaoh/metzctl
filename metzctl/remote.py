import wakeonlan
from getmac import get_mac_address
from pip._vendor import requests

PORT = 49200
""" Port of the remote service. Actually the device and port could be resolved by a SSDP
but the port seems to be static nowadays."""

SERVICE_PATH = "/services/rcr/control/RCRService"
SOAP_ACTION = "urn:metz.de:service:RCRService:1#SendKeyCode"

SEND_KEY_XML = """<?xml version="1.0" encoding="utf-8"?>
 <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
   <s:Body>
     <u:SendKeyCode xmlns:u="urn:metz.de:service:RCRService:1">
       <KeyCode>{}</KeyCode>
       <DestinationDevice>0</DestinationDevice>
       <ButtonHold>0</ButtonHold>
     </u:SendKeyCode>
   </s:Body>
 </s:Envelope>"""

KEY_CODE_POWER = 11
KEY_CODE_CH_UP = 47
KEY_CODE_CH_DOWN = 47
KEY_CODE_VOLUME_UP = 28
KEY_CODE_VOLUME_DOWN = 27
KEY_CODE_MUTE = 35
KEY_CODE_OK = 39


class MacLookUpException(Exception):
    """MAC could not be resolved"""
    pass


class Remote:
    """Remote access class for Metz television.
    """
    def __init__(self, ip):
        """Constructor

        :param ip: The IP address of the television. The IP could be resolved by SSDP, but in case multiple
        televisions are in the network this would be not unique.
        """
        self.ip = ip

    def power_on(self):
        """Powers one the television by a Wake-On-LAN packet using the MAC address.
        :return: None
        """
        mac = get_mac_address(ip=self.ip)
        if mac:
            wakeonlan.create_magic_packet(mac)
        else:
            raise MacLookUpException()

    def __send__(self, key_code: int):
        xml = SEND_KEY_XML.format(key_code)
        requests.post(self.ip + ":" + PORT + SERVICE_PATH, data=xml, headers={"SOAPAction": SOAP_ACTION,
                                                                              "Content-Type": 'text/xml; charset="utf-8"'})

    def volume_up(self):
        """Turns up the volume.

        :return: None
        """
        self.__send__(KEY_CODE_VOLUME_UP)

    def volume_down(self):
        """Turns down the volume.

        :return: None
        """
        self.__send__(KEY_CODE_VOLUME_DOWN)

    def mute(self):
        """Mute.

        :return: None
        """
        self.__send__(KEY_CODE_MUTE)

    def unmute(self):
        """Unmute.

        :return: None
        """
        self.__send__(KEY_CODE_MUTE)

    def ch_up(self):
        """Channel up.

        :return: None
        """
        self.__send__(KEY_CODE_CH_UP)

    def ch_down(self):
        """Channel down.

        :return: None
        """
        self.__send__(KEY_CODE_CH_DOWN)

    def power(self):
        """Power.

        :return: None
        """
        self.__send__(KEY_CODE_POWER)

    def ok(self):
        """Sends OK.

        :return: None
        """
        self.__send__(KEY_CODE_OK)

    def channel(self, channel: int):
        """Sends a channel number.

        :return: None
        """
        self.__send__(channel)


