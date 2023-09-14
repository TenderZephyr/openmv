import sensor, image, time
from pid import PID
from pyb import Servo
pan_servo=Servo(1)
tilt_servo=Servo(2)
pan_servo.calibration(950,2300,500)
tilt_servo.calibration(700,2200,500)
red_threshold  = (52, 90, 12, 21, 0, 10)
pan_pid = PID(p=0.1, i=0, imax=90)
tilt_pid = PID(p=0.1, i=0, imax=90)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
clock = time.clock()
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob
while(True):
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([red_threshold],pixels_threshold=20, area_threshold=20, merge=False)
    if blobs:
        max_blob = find_max(blobs)
        pan_error = max_blob.cx()-img.width()/2
        tilt_error = max_blob.cy()-img.height()/2
        print("pan_error: ", pan_error)
        img.draw_rectangle(max_blob.rect())
        img.draw_cross(max_blob.cx(), max_blob.cy())
        pan_output=pan_pid.get_pid(pan_error,1)/2
        tilt_output=tilt_pid.get_pid(tilt_error,1)
        print("pan_output",pan_output)
        pan_servo.angle(pan_servo.angle()-pan_output)
        tilt_servo.angle(tilt_servo.angle()-tilt_output)
