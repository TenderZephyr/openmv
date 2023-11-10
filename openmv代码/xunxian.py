THRESHOLD = (0, 41, -128, 127, -128, 127)#(120, 34, 35, 66, 5, 54) # Grayscale threshold for dark things...
import sensor, image, time
from pyb import LED
from pid import PID
from pyb import UART
rho_pid = PID(p=0.4, i=0)
theta_pid = PID(p=0.001, i=0)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

uart = UART(3, 115200)#P4、5  TX、RX
while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD])
    line = img.get_regression([(100,100)], robust = True)
    if (line):
        rho_err = abs(line.rho())-img.width()/2 #截距偏移
        if line.theta()>90:
            theta_err = line.theta()-180    #角度偏移
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 127)#画标志线

        if line.magnitude()>8:
            output_str="[%d,%d]" % (rho_err,theta_err) #方式1
            print(rho_err,theta_err)
            uart.write(output_str+'\r\n')
        pass
