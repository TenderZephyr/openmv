import sensor, image, time
from pyb import UART
import lcd
output_str_green="[0,0]"
output_str_red="[0,0]"
output_str_blue="[0,0]"
output_str_brown="[0,0]"
output_str_yellow="[0,0]"
x = 0
y = 0
green_threshold  = (   3,   39,  -29,   2,   1,   25)
red_threshold	= (   28,   40,  51,   65,   22,   50)
orange_threshold = (   23,   39,  19,   42,   13,   31)
blue_threshold  = (   50,   56,  -14,   1,   -31,   -13)
brown_threshold  = (   22,   30,  1,   17,   8,   25)
yellow_threshold  = (   53,   58,  -7,   3,   58,   63)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.set_windowing((240,240))
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()
lcd.init()

uart = UART(3, 115200)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob
def detect(max_blob):
    shape=0
    if max_blob.solidity()>0.90 or max_blob.density()>0.84:
        img.draw_rectangle(max_blob.rect(),color=(255,255,255))
        shape=1
    elif max_blob.density()>0.6:
        img.draw_circle((max_blob.cx(), max_blob.cy(),int((max_blob.w()+max_blob.h())/4)))
        shape=2
    elif max_blob.density()>0.4:
        img.draw_rectangle(max_blob.rect(),color=(0,0,0))
        shape=3
    return shape
while(True):
    img = sensor.snapshot()
    #lcd.display(sensor.snapshot())
    blobs_green = img.find_blobs([green_threshold])
    blobs_red = img.find_blobs([red_threshold])
    blobs_blue = img.find_blobs([blue_threshold])
    blobs_brown = img.find_blobs([brown_threshold])
    blobs_yellow = img.find_blobs([yellow_threshold])
    if blobs_green:
        max_blob_green=find_max(blobs_green)
        shape_green=detect(max_blob_green)
        img.draw_cross(max_blob_green.cx(), max_blob_green.cy(),color=(0,255,0))
        output_str_green="[%.3d,%.3d,%d]" % (max_blob_green.cx(),max_blob_green.cy(),shape_green)
        print('green:',output_str_green)
    else:
        print('not found green!')
    if blobs_red:
        max_blob_red=find_max(blobs_red)
        shape_red=detect(max_blob_red)
        img.draw_cross(max_blob_red.cx(), max_blob_red.cy(),color=(255,0,0))
        output_str_red="[%d,%d,%d]" % (max_blob_red.cx(),max_blob_red.cy(),shape_red)

        print('red:',output_str_red)
    else:
        print('not found red !')
    if blobs_blue:
        max_blob_blue=find_max(blobs_blue)
        shape_blue=detect(max_blob_blue)
        img.draw_cross(max_blob_blue.cx(), max_blob_blue.cy(),color=(0,0,255))
        output_str_blue="[%d,%d,%d]" % (max_blob_blue.cx(),max_blob_blue.cy(),shape_blue)
        print('blue:',output_str_blue)
    else:
        print('not found blue !')
    if blobs_brown:
        max_blob_brown=find_max(blobs_brown)
        shape_brown=detect(max_blob_brown)
        img.draw_cross(max_blob_brown.cx(), max_blob_brown.cy(),color=(205,133,63))
        output_str_brown="[%d,%d,%d]" % (max_blob_brown.cx(),max_blob_brown.cy(),shape_brown)
        print('brown:',output_str_brown)
    else:
        print('not found brown !')
    if blobs_yellow:
        max_blob_yellow=find_max(blobs_yellow)
        shape_yellow=detect(max_blob_yellow)
        img.draw_cross(max_blob_yellow.cx(), max_blob_yellow.cy(),color=(255,255,0))
        output_str_yellow="[%d,%d,%d]" % (max_blob_yellow.cx(),max_blob_yellow.cy(),shape_yellow)
        print('yellow:',output_str_yellow)
    else:
        print('not found yellow !')
    uart.write('@' + output_str_green + '#' + '%'+ '\r\n')
    #print(clock.fps())
