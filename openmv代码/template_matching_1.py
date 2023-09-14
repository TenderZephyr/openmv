# Template Matching Example - Normalized Cross Correlation (NCC)
#
# This example shows off how to use the NCC feature of your OpenMV Cam to match
# image patches to parts of an image... expect for extremely controlled enviorments
# NCC is not all to useful.
#
# WARNING: NCC supports needs to be reworked! As of right now this feature needs
# a lot of work to be made into somethin useful. This script will reamin to show
# that the functionality exists, but, in its current state is inadequate.

import time, sensor, image
from image import SEARCH_EX, SEARCH_DS
import time
from pyb import UART

uart = UART(3, 19200)
# Reset sensor
sensor.reset()

# Set sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
# Max resolution for template matching with SEARCH_EX is QQVGA
sensor.set_framesize(sensor.QQVGA)
# You can set windowing to reduce the search image.
#sensor.set_windowing(((640-80)//2, (480-60)//2, 80, 60))
sensor.set_pixformat(sensor.GRAYSCALE)

# Load template.
# Template should be a small (eg. 32x32 pixels) grayscale image.
template1 = image.Image("/1.pgm")
template2 = image.Image("/2.pgm")
template3 = image.Image("/3.pgm")
template4 = image.Image("/4.pgm")
template5 = image.Image("/5.pgm")
template6 = image.Image("/6.pgm")
template7 = image.Image("/7.pgm")
template8 = image.Image("/8.pgm")

clock = time.clock()

# Run template matching
while (True):
    clock.tick()
    img = sensor.snapshot()

    # find_template(template, threshold, [roi, step, search])
    # ROI: The region of interest tuple (x, y, w, h).
    # Step: The loop step used (y+=step, x+=step) use a bigger step to make it faster.
    # Search is either image.SEARCH_EX for exhaustive search or image.SEARCH_DS for diamond search
    #
    # Note1: ROI has to be smaller than the image and bigger than the template.
    # Note2: In diamond search, step and ROI are both ignored.
    r1 = img.find_template(template1, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r1:
        img.draw_rectangle(r1)
        print(1)
    r2 = img.find_template(template2, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r2:
        img.draw_rectangle(r2)
        print(2)
    r3 = img.find_template(template3, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r3:
        img.draw_rectangle(r3)
        print(3)
    r4 = img.find_template(template4, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r4:
        img.draw_rectangle(r4)
        print(4)
    r5 = img.find_template(template5, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r5:
        img.draw_rectangle(r5)
        print(5)
    r6 = img.find_template(template6, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r6:
        img.draw_rectangle(r6)
        print(6)
    r7 = img.find_template(template7, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r7:
        img.draw_rectangle(r7)
        print(7)
    r8 = img.find_template(template8, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    if r8:
        img.draw_rectangle(r8)
        print(8)
        uart.write("8\r")
    #time.sleep_ms(1000)
    #print(clock.fps())
