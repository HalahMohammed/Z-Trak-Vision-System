# Z-Trak-Vision-System
Depth-based object detection and routing for robotic arm integration  A real-time 3D vision processing system using Z-Trak cameras for depth-based object detection and intelligent routing to robotic workcells.

## Overview

This system performs real-time blob analysis on images captured from a GigE Vision camera, with integrated Modbus communication for industrial automation.

## Features

- Real-time image acquisition and processing
- GPU-accelerated Halcon operations
- Modbus TCP communication
- Blob detection and analysis
- Depth calculation from intensity values
- Tiled image processing for line scan applications

## Hardware Requirements

- NVIDIA GPU (RTX 4060 tested)
- GigE Vision compatible camera
- Modbus TCP compatible device

## Dependencies

- Halcon Python library
- Custom Modbus worker module 
