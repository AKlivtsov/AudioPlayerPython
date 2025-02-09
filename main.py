import sys
import os
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QThread

# audio
from pygame import mixer
from mutagen.mp3 import MP3

# buttons, etc
import mainUI

# for slider
class TimerThread(QtCore.QThread):
	s_timer = QtCore.pyqtSignal(int)

	def  __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)

		self.is_music_play = None

	def run(self):

		while self.is_music_play == True:
			cur_time = mixer.music.get_pos()
			cur_time = cur_time / 1000

			self.s_timer.emit(round(cur_time))
			self.sleep(1)

	def change_state_True(self):
		self.is_music_play = True

	def change_state_False(self):
		self.is_music_play = False


class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow, QDialog):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		# window setting
		self.setWindowTitle("AudioThing")
		self.hs_timeline.setValue(0)

		# buttons
		self.btn_next.clicked.connect(self.change_track)
		self.btn_prev.clicked.connect(self.change_track)
		self.btn_pause.clicked.connect(self.play)
		self.hs_timeline.valueChanged.connect(self.wind_up_track)

		# threads
		self.thread = TimerThread()
		self.thread.s_timer.connect(self.hs_time)
		self.thread.s_timer.connect(self.end_await)
		self.thread.s_timer.connect(self.lbl_cur_time)

		# audio
		mixer.init()
		self.song_length = 0
		self.is_music_play = None
		self.track_num = 0
		self.playlist = ["assets/music_samples/blah.mp3", "assets/music_samples/edamame.mp3"]

	def play(self):

		if self.is_music_play == None:
			mixer.music.load(self.playlist[0])
			mixer.music.play()
			# mixer.music.rewind() # for absolute possition track in wind_up_track
			self.track_num += 1
			self.is_music_play = True
			self.thread.change_state_True()
			self.lengh_of_track(0)
			self.filename(0)

		elif self.is_music_play == True:
			mixer.music.pause()
			self.is_music_play = False
			self.thread.change_state_False()

		elif self.is_music_play == False:
			mixer.music.unpause()
			self.is_music_play = True
			self.thread.change_state_True()
			self.thread.start()

	def change_track(self):

		if self.playlist:

			if self.track_num == 0:
				self.thread.change_state_True()
				mixer.music.load(self.playlist[self.track_num])
				self.lengh_of_track(self.track_num)
				self.filename(self.track_num)
				self.track_num += 1
				mixer.music.play()

			else:
				try:
					self.thread.change_state_True()
					mixer.music.load(self.playlist[self.track_num])
					self.lengh_of_track(self.track_num)
					self.filename(self.track_num)
					self.track_num += 1
					mixer.music.play()

				except IndexError:
					self.thread.change_state_True()
					mixer.music.load(self.playlist[0])
					self.lengh_of_track(0)
					self.filename(0)
					self.track_num = 1
					mixer.music.play()

	def lengh_of_track(self, x):

		a = mixer.Sound(self.playlist[x])
		self.song_length = a.get_length()
		
		minutes, seconds = divmod(self.song_length, 60)
		minutes = round(minutes)
		seconds = round(seconds)

		self.hs_timeline.setRange(0, round(self.song_length))

		self.lbl_endTime.setText('{:02d}:{:02d}'.format(minutes, seconds))

		self.thread.start()

	def filename(self, x):
		trackname = os.path.basename(self.playlist[x]).split('.')[0]
		self.lbl_trackName.setText(trackname)

	def hs_time(self, cur_time):
		self.hs_timeline.setValue(cur_time)

	def lbl_cur_time(self, cur_time):
		minutes, seconds = divmod(cur_time, 60)
		minutes = round(minutes)
		seconds = round(seconds)

		self.lbl_curTime.setText('{:02d}:{:02d}'.format(minutes, seconds))

	def end_await(self, cur_time):
		minutes, seconds = divmod(self.song_length, 60)
		minutes = round(minutes * 60)
		seconds = round(seconds)
		act_time = minutes + seconds

		if cur_time + 1 == act_time:
			self.change_track()

	def wind_up_track(self, value):
		mixer.music.set_pos(value)

# pls, write it
class FileWindow(QtWidgets.QMainWindow,QDialog):
	pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()	
    sys.exit(app.exec())
