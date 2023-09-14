import sensor, image, time
import lcd
thresholds = [(30, 100, 15, 127, 15, 127),
			  (30, 100, -64, -8, -32, 32),
			  (0, 15, 0, 40, -80, -20)]
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
clock = time.clock()
lcd init()
while(True):
	clock.tick()
	img = sensor.snapshot()
	lcd.display(sensor.snapshot())
	for blob in img.find_blobs(thresholds, pixels_threshold=2000, area_threshold=3000, merge=True):
		if blob.code() == 3:
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.cx(), blob.cy())
			img.draw_string(blob.x() + 2, blob.y() + 2, "r/g")
		if blob.code() == 5:
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.cx(), blob.cy())
			img.draw_string(blob.x() + 2, blob.y() + 2, "r/b")
		if blob.code() == 6:
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.cx(), blob.cy())
			img.draw_string(blob.x() + 2, blob.y() + 2, "g/b")
		if blob.code() == 7:
			img.draw_rectangle(blob.rect())
			img.draw_cross(blob.cx(), blob.cy())
			img.draw_string(blob.x() + 2, blob.y() + 2, "r/g/b")
	print(clock.fps())