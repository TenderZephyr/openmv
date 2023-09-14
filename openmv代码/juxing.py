import sensor, image, time
from pyb import UART

output_str="0,0"

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240,240))
sensor.skip_frames(time = 2000)
clock = time.clock()

uart = UART(3, 9600)

while(True):
    clock.tick()
    img = sensor.snapshot()

    # 下面的`threshold`应设置为足够高的值，以滤除在图像中检测到的具有
    # 低边缘幅度的噪声矩形。最适用与背景形成鲜明对比的矩形。

    for r in img.find_rects(threshold = 30000):#roi为感兴趣区域
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        output_str=""
        for p in r.corners():
            img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
            img.draw_string(p[0], p[1], str(p[0]) + ',' + str(p[1]))
            output_str += ("%.3d%.3d" % (p[0], p[1]))
        print(output_str)#从左下角（x ，y）坐标开始逆时针顺序

    uart.write('@' + output_str + '\r' + '\n')
    print("FPS %f" % clock.fps())
