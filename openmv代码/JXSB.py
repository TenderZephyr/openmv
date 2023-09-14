from pyb import UART

uart = UART(3, 9600)

def Recognition_Rectangle():
    output_str = "0,0"
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
