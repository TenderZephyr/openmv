import sensor, image, time
from pyb import UART

output_str_red="[0,0]"
x = 0
y = 0
red_threshold  = (97, 100, -2, 15, -8, 92)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240,240))
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()

uart = UART(3, 9600)

def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob

while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs_red = img.find_blobs([red_threshold])

    if blobs_red:
        max_blob_red=find_max(blobs_red)
        img.draw_cross(max_blob_red.cx(), max_blob_red.cy(),color = (0,255,0))
        cx = max_blob_red.cx()
        cy = max_blob_red.cy()
        img.draw_string(cx, cy, str(cx) + ',' + str(cy), color = (255, 0, 0))
        output_str_red = "%.3d%.3d" % (cx, cy)
        print('red:',output_str_red)
    else:
        print('not found red!')

    uart.write('@' + output_str_red + '\r' + '\n')
    print(clock.fps())
