# image_processor.py
import halcon as ha
import time
from config import *

class ImageProcessor:
    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.prev_regions = ha.gen_empty_region()
        self.counter = 0
        self.index = 0
        
        # Initialize tiled image
        self.tiled_image = ha.gen_image_const(
            'real', 
            self.image_width, 
            self.image_height * MAX_IMAGES_REGIONS
        )
    
    def analyze_blob_objects(self, image):
        """Main image processing pipeline for blob analysis"""
        # Thresholding
        curr_regions = ha.threshold(image, THRESHOLD_MIN, THRESHOLD_MAX)
        
        # Region merging for line scan
        curr_merged_regions, prev_merged_regions = ha.merge_regions_line_scan(
            curr_regions, self.prev_regions, self.image_height, 
            'top', MAX_IMAGES_REGIONS
        )
        
        # Object detection and selection
        object_candidates = ha.connection(prev_merged_regions)
        selected_objects = ha.select_shape(
            object_candidates, 'area', 'and', AREA_MIN, AREA_MAX
        )
        
        # Area and center calculation
        area, row, column = ha.area_center(selected_objects)
        object_count = ha.tuple_length(row)
        
        # Process detected objects
        if object_count > 0:
            self._process_objects(selected_objects, row, column, image)
        
        # Update regions and tiled image
        self._update_regions_and_image(curr_merged_regions, selected_objects, image)
        
        self.counter += 1
        self.index += 1
    
    def _process_objects(self, selected_objects, rows, columns, image):
        """Process individual detected objects"""
        for n in range(len(rows)):
            object_selected = ha.select_obj(selected_objects, n + 1)
            mean, deviation = ha.intensity(object_selected, image)
            
            if len(mean) > 0:
                mean_val = float(mean[0])
                depth = self._calculate_depth(mean_val)
                
                # Print object information
                print(f"{self.index}, {rows[n] * X_SCALE_FACTOR}, "
                      f"{columns[n] * Y_SCALE_FACTOR}, {mean_val}")
                
                time.sleep(0.2)  # Optional delay
    
    def _calculate_depth(self, mean_value):
        """Calculate depth based on mean intensity value"""
        if mean_value < 880:
            return (mean_value - 879) * 2
        else:
            return mean_value - 879
    
    def _update_regions_and_image(self, curr_merged_regions, selected_objects, image):
        """Update regions and maintain tiled image"""
        # Move regions for tiled image coordinates
        object_tiled_coords = ha.move_region(
            selected_objects, 
            (MAX_IMAGES_REGIONS - 1) * self.image_height, 
            0
        )
        
        # Update previous regions
        self.prev_regions = ha.copy_obj(curr_merged_regions, 1, -1)
        
        # Update tiled image
        tiled_minus_oldest = ha.crop_part(
            self.tiled_image, 
            self.image_height, 0, 
            self.image_width, 
            (MAX_IMAGES_REGIONS - 1) * self.image_height
        )
        
        images_to_tile = ha.concat_obj(tiled_minus_oldest, image)
        self.tiled_image = ha.tile_images_offset(
            images_to_tile, 
            [0, (MAX_IMAGES_REGIONS - 1) * self.image_height],
            [0, 0], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
            self.image_width, 
            MAX_IMAGES_REGIONS * self.image_height
        )
