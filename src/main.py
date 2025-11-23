# main.py
import time
import halcon as ha
from hardware_setup import setup_gpu, setup_camera, camera_calibration
from modbus_interface import ModbusInterface
from image_processor import ImageProcessor
from config import *

def main():
    # Initialize hardware
    print("Initializing hardware...")
    gpu_handle = setup_gpu()
    camera_handle, camera_id = setup_camera()
    
    if not camera_handle:
        print("Camera initialization failed!")
        return
    
    # Camera calibration
    width, height, timeout, zoffset, zscale = camera_calibration(camera_handle)
    print(f"Camera calibrated: {width}x{height}")
    
    # Initialize Modbus
    modbus = ModbusInterface()
    modbus.connect()
    
    # Initialize image processor
    processor = ImageProcessor(width, height)
    
    # Start image acquisition
    start_time = time.time()
    ha.grab_image_start(camera_handle, -1)
    end_time = time.time()
    
    time_complexity = end_time - start_time
    print("Acquisition started")
    print(f"Initialization time: {time_complexity:.2f} seconds")
    
    # Main processing loop
    try:
        while True:
            # Capture image
            image = ha.grab_image_async(camera_handle, -1)
            
            # Preprocess image
            image = ha.mirror_image(image, 'column')
            image = ha.convert_image_type(image, 'real')
            image = ha.scale_image(image, zscale, zoffset)
            
            # Process image
            processor.analyze_blob_objects(image)
            
    except KeyboardInterrupt:
        print("Processing stopped by user")
    except Exception as e:
        print(f"Error in main loop: {e}")
    finally:
        # Cleanup
        ha.close_framegrabber(camera_handle)
        print("Application terminated")

if __name__ == "__main__":
    main()
