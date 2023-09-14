import sensor, image, time
from pyb import UART

output_str = "0,0"

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)  # 可根据需求调整分辨率
sensor.skip_frames(Time = 2000)
sensor.set_windowing((240,240))
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_whitebal(False)  # 关闭白平衡
clock = time.clock()

uart = UART(3, 9600)

# 初始化显示屏幕
#lcd = sensor.get_display()

while True:
    clock.tick()
    img = sensor.snapshot()         # Take a picture and return the image.
    # to the IDE. The FPS should increase once disconnected.
    histogram = img.get_histogram()
    Thresholds = histogram.get_threshold()
    #l = Thresholds.l_value()
    #a = Thresholds.a_value()
    #b = Thresholds.b_value()
    #print(Thresholds)
    v = Thresholds.value()
    img.binary([(0,v)])
    for r in img.find_rects(roi = (60, 100, 150, 150), threshold = 40000):#roi为感兴趣区域
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        output_str=""
        for p in r.corners():
            img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
            img.draw_string(p[0], p[1], str(p[0]) + ',' + str(p[1]), color = (255, 0, 0))
            output_str += ("%.3d%.3d" % (p[0], p[1]))
        print(output_str)#从左下角（x ，y）坐标开始逆时针顺序

    uart.write('@' + output_str + '\r' + '\n')
    print("FPS %f" % clock.fps())

    #lcd.display(img)  # 在显示屏上显示二值化后的图像
