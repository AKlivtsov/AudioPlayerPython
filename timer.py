import time

def timer(x,song_length):

	cur_time = 0.00

	while cur_time <= float(song_length):

		cur_time = float(cur_time) + 0.01
		cur_time = float("%.2f" % cur_time)

		cur_time_lbl = str(cur_time).replace('.',':')
		print(cur_time_lbl)
		x.setText(str(cur_time_lbl))
		time.sleep(1)
