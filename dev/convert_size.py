import ctypes, comtypes
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#
# def set_volume(volume_level):
#     volume_level = max(0, min(volume_level, 1))  # Ensure volume is within 0-1 range
#
#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
#     volume = interface.QueryInterface(IAudioEndpointVolume)
#     volume.SetMasterVolumeLevelScalar(volume_level, None)
#
# # Example usage to set volume to 50%
# set_volume(1)

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    return volume.GetMasterVolumeLevelScalar()

# Example usage
current_volume = get_volume()
print(f"Current volume: {current_volume}")