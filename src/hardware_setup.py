# hardware_setup.py
import halcon as ha
from config import *

def setup_gpu():
    """Initialize and configure GPU for Halcon processing"""
    Device = ha.query_available_compute_devices()
    DeviceHandle = None
    
    for i in range(min(2, len(Device))):
        name = ha.get_compute_device_info_s(Device[i], 'name')
        vendor = ha.get_compute_device_info_s(Device[i], 'vendor')
        if vendor == GPU_VENDOR and name == GPU_NAME:
            DeviceHandle = ha.open_compute_device(Device[i])
            break
    
    if DeviceHandle:
        ha.init_compute_device(DeviceHandle, 'all')
        ha.set_compute_device_param(DeviceHandle, 'asynchronous_execution', 'true')
        print("GPU initialized successfully")
    else:
        print("Preferred GPU not found, using default device")
    
    return DeviceHandle

def setup_camera():
    """Initialize and configure camera"""
    Information, ValueList = ha.info_framegrabber(CAMERA_TYPE, 'device')
    AcqHandle = ha.open_framegrabber(
        CAMERA_TYPE, 0, 0, 0, 0, 0, 0, 'progressive', -1, 
        'default', -1, 'false', 'default', CAMERA_NAME, 0, -1
    )
    return AcqHandle, ValueList[0] if ValueList else None

def camera_calibration(AcqHandle):
    """Configure camera parameters and calibration"""
    ProfileRate = ha.get_framegrabber_param_s(AcqHandle, 'profileRateMax')
    Width = ha.get_framegrabber_param_s(AcqHandle, 'pointsPerProfile')
    Height = ha.get_framegrabber_param_s(AcqHandle, 'profilesPerScan')
    MinTimeout = (Height / ProfileRate) * 10000 * 10
    
    ha.set_framegrabber_param(AcqHandle, 'grab_timeout', MinTimeout)
    
    Xscale = ha.get_framegrabber_param_s(AcqHandle, 'uniformXStepSize')
    Xoffset = ha.get_framegrabber_param_s(AcqHandle, 'aoiFFOVStartX')
    Zscale = ha.get_framegrabber_param_s(AcqHandle, 'heightScaler')
    Zoffset = ha.get_framegrabber_param_s(AcqHandle, 'aoiZStart')
    
    ha.set_framegrabber_param(AcqHandle, 'counterReset', 1)
    
    return Width, Height, MinTimeout, Zoffset, Zscale
