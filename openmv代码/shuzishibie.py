import sensor, image, time, os, tf, uos, gc
from pyb import LED
from pyb import UART
from pyb import millis
import time
import lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.set_windowing((160, 160))
sensor.skip_frames(time=2000)
net = None
labels = None
number1 = 0
number2 = 0
number3 = 0
flag = 0
try:
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')
try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')
clock = time.clock()
lcd.init()
uart = UART(3, 19200)
Time_Last = millis()
while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(sensor.snapshot())

    if (uart.any()):
        command = uart.read().decode()
        print(command)
        if command == 'identity numbers':
            while(True):
                lcd.display(sensor.snapshot())
                for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
                    print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
                    #img.draw_rectangle(obj.rect())
                    predictions_list = list(zip(labels, obj.output()))
                    for i in range(len(predictions_list)):

                        print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

                        if millis()-Time_Last > 1500:
                            Time_Last=millis()
                        if predictions_list[i][1] > 0.85:
                            numbernew = predictions_list[i][0]
                            #img.draw_rectangle(numbernew)
                            if 600 > millis()-Time_Last > 200:
                                number1 = numbernew
                            elif 1000 > millis()-Time_Last > 600:
                                number2 = numbernew
                            elif 1500 > millis()-Time_Last > 1000:
                                number3 = numbernew
                            if number1 != 0 and number2 != 0 and number3 != 0:
                                if (number1 == number2) and (number2 == number3):
                                    number = numbernew
                                    LED(2).on()
                                    time.sleep_ms(60)
                                    LED(2).off()
                                    print(number)
                                    img.draw_string(0, 0, "number is", color = (255, 0, 0))
                                    img.draw_string(0, 13, number, color = (255, 0, 0))
                                    uart.write(number)
                                    flag = 1
                                    #time.sleep_ms(1000)
                if flag == 1:
                    flag = 0
                    break

