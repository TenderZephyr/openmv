import sensor, image, time
import lcd
thresholds = [(69, 100, -49, -6, -17, 13)]
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
lcd.init()
while(True):
    clock.tick()
    img = sensor.snapshot()
    #lcd.display(sensor.snapshot())

    for blob in img.find_blobs(thresholds, pixels_threshold=2000, area_threshold=4000, merge=False):
            img.draw_rectangle(blob.rect(), color = (255, 0, 0))
            img.draw_cross(blob.cx(), blob.cy())
            img.draw_string(blob.x() + 2, blob.y() + 2, "r/g")
    print(clock.fps())
