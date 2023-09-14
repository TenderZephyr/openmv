import sensor, time, image, pyb
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B128X128)
sensor.set_windowing((92,112))
sensor.skip_frames(10)
sensor.skip_frames(time = 5000)
NUM_SUBJECTS = 2
NUM_SUBJECTS_IMGS = 20
img = sensor.snapshot()
d0 = img.find_lbp((0, 0, img.width(), img.height()))
img = None
pmin = 999999
num=0
def min(pmin, a, s):
    global num
    if a<pmin:
        pmin=a
        num=s
    return pmin
for s in range(1, NUM_SUBJECTS+1):
    dist = 0
    for i in range(2, NUM_SUBJECTS_IMGS+1):
        img = image.Image("renlianshibie/s%d/%d.pgm"%(s, i))
        d1 = img.find_lbp((0, 0, img.width(), img.height()))
        dist += image.match_descriptor(d0, d1)
    print("Average dist for subject %d: %d"%(s, dist/NUM_SUBJECTS_IMGS))
    pmin = min(pmin, dist/NUM_SUBJECTS_IMGS, s)
    print(pmin)
print(num)
