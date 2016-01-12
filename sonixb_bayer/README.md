# Description

This program demonstrates how to decode RAW data taken from a camera via L4l2 interface. Pygame camera module is used to grab the raw data as getting the processed image consistently crashed my Python. RAW image data which is in Bayer pattern is then converted to RGB or BW using a  couple of selectable filters.

## Disclaimer

The program works with a specific model of a USB camera on Raspberry Pi. There is no guarantee that this program will work with any other hardware/driver combination.

## Camera driver

sonixb

## Pixel formats advertised by the camera

- S910
- BA81

## Camera image width/height

160x120 - at least I could not make the driver to get anything better

## Usage

`python3 cambayer.py`

After starting the program wait a couple of seconds for the image to settle. When the image is constantly flashing between bright and dark for longer than 10 seconds chances are that something happened to the driver(?) and yyou need to restart RPi.

When the program is running and you see the image from the camera, you can press numerical keys to select one of RAW Bayer processing filters. Press space to take a screenshot as BMP (PNG had swapped R and B channels on my machine). Press ESC to exit.




