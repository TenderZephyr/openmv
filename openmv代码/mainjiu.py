import sensor, image, time
from pyb import UART
from pyb import millis

output_str = ""
output_str_red = ""
x = 0
y = 0
command = '0'
red_threshold  = (96, 100, -1, 0, -8, 92)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((400,400))
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()
uart = UART(3, 115200)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob = blob
            max_size = blob.pixels()
    return max_blob
while(True):
    #clock.tick()
    if uart.any():
        command = uart.read().decode()
        if command == '1':
            while(True):
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
                if uart.any():
                    stop = uart.read().decode()
                    if stop == '2':
                        command = '2'
                        break
        if command == '2':
            while(True):
                img = sensor.snapshot()
                histogram = img.get_histogram()
                Thresholds = histogram.get_threshold()
                v = Thresholds.value()
                img.binary([(0,v)])
                for r in img.find_rects(roi = (60, 60, 300, 300), threshold = 40000):#
                    img.draw_rectangle(r.rect(), color = (255, 0, 0))
                    output_str=""
                    for p in r.corners():
                        img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
                        img.draw_string(p[0], p[1], str(p[0]) + ',' + str(p[1]), color = (255, 0, 0))
                        output_str += ("%.3d%.3d" % (p[0], p[1]))
                    print(output_str)
                if output_str != "":
                    uart.write('A' + output_str + '\r' + '\n')
                if uart.any():
                    stop = uart.read().decode()
                    if stop == '1':
                        command = '1'
                        break
       # print(clock.fps())

