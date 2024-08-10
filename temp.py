from onvif import ONVIFCamera
import zeep

# Disable strict mode on Zeep's XML parser (useful for some devices)
zeep.xsd.constants.MAX_LENGTH = 200000000
zeep.xsd.constants.MAX_NESTED = 200000000

# Function to discover ONVIF devices
def discover_onvif_devices():
    from onvif import ONVIFService
    discovery_service = ONVIFService(wsdl='https://www.onvif.org/ver10/device/wsdl/devicemgmt.wsdl')
    devices = discovery_service.GetDiscoveryMode()
    return devices

# Discover and print devices
devices = discover_onvif_devices()
for device in devices:
    print(f'Device: {device}')

# Example of connecting to a specific camera (replace with your camera details)
# camera = ONVIFCamera('192.168.1.100', 80, 'admin', 'password')
# media_service = camera.create_media_service()
# profiles = media_service.GetProfiles()
# for profile in profiles:
#     print(f'Profile: {profile.name}')