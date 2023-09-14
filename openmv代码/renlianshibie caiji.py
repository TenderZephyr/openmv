import sensor, image, pyb
RED_LED_PIN = 1
BLUE_LED_PIN = 3
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B128X128)
sensor.set_windowing((92,112))
sensor.skip_frames(10)
sensor.skip_frames(time = 2000)
num = 4
n = 20
while(n):
    pyb.LED(RED_LED_PIN).on()
    sensor.skip_frames(time = 3000)
    pyb.LED(RED_LED_PIN).off()
    pyb.LED(BLUE_LED_PIN).on()
    print(n)
    sensor.snapshot().save("renlianshibie/s%s/%s.pgm" % (num, n) )
    n -= 1
    pyb.LED(BLUE_LED_PIN).off()
    print("Done! Reset the camera to see the saved image.")
