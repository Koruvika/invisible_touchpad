import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    return volume.GetMasterVolumeLevelScalar()


# Example usage
current_volume = get_volume()
print(f"Current volume: {current_volume}")