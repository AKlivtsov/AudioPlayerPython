# база
import sys
from PyQt6 import QtWidgets, QtCore 
from PyQt6.QtWidgets import QDialog, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QThread

# аудио
from pygame import mixer
from mutagen.mp3 import MP3

# окно 
import mainUI

# поток отсчета времени трека
class TimerThread(QtCore.QThread):
	s_timer = QtCore.pyqtSignal(int)

	def  __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)

		self.is_music_play = None

	def run(self):

		while self.is_music_play == True:
			cur_time = mixer.music.get_pos()
			cur_time = cur_time / 1000
			print(round(cur_time))

			self.s_timer.emit(round(cur_time))
			self.sleep(1)

	def change_state_True(self):
		self.is_music_play = True

	def change_state_False(self):
		self.is_music_play = False


# основное окно
class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow, QtCore.QTimer, QDialog):

	def __init__(self):
		super(MainWindow, self).__init__()
		self.setupUi(self)

		# настройки окна
		self.setWindowTitle("AudioThing")
		self.pb_timeline.setValue(0)

		# кнопки
		self.btn_next.clicked.connect(self.change_track)
		self.btn_prev.clicked.connect(self.change_track)
		self.btn_pause.clicked.connect(self.play)

		# потоки
		self.thread = TimerThread()
		self.thread.s_timer.connect(self.pb_time)

		# аудио
		mixer.init()
		global is_music_play
		self.is_music_play = None
		self.track_num = 0
		self.playlist = ["assets/music_samples/blah.mp3", "assets/music_samples/edamame.mp3"]

	def play(self):

		if self.is_music_play == None:
			mixer.music.load(self.playlist[0])
			mixer.music.play()
			self.track_num += 1
			self.is_music_play = True
			self.thread.change_state_True()
			self.lengh_of_track(0)

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
				self.track_num += 1
				mixer.music.play()

			else:
				try:
					self.thread.change_state_True()
					mixer.music.load(self.playlist[self.track_num])
					self.lengh_of_track(self.track_num)
					self.track_num += 1
					mixer.music.play()

				except IndexError:
					self.thread.change_state_True()
					mixer.music.load(self.playlist[0])
					self.lengh_of_track(0)
					self.track_num = 1
					mixer.music.play()

	def lengh_of_track(self, x):

		a = mixer.Sound(self.playlist[x])
		song_length = a.get_length()
		print(round(song_length))
		
		# поулчаем продолжительность трека
		minutes, seconds = divmod(song_length, 60)
		minutes = round(minutes)
		seconds = round(seconds)

		self.pb_timeline.setRange(0, round(song_length))
		print('{:02d}:{:02d}'.format(minutes, seconds))

		self.lbl_endTime.setText('{:02d}:{:02d}'.format(minutes, seconds))

		self.thread.start()

	def pb_time(self, cur_time):
		self.pb_timeline.setValue(cur_time)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()	
    sys.exit(app.exec())
