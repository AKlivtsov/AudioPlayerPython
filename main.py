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
	s_timer = QtCore.pyqtSignal(float)

	def  __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)

	def run(self):

		while MainWindow.is_music_play:
			cur_time = mixer.music.get_pos()
			cur_time = cur_time / 1000 /60
			cur_time = float("%.2f" % cur_time)
			print(cur_time)
			self.s_timer.emit(cur_time)
			self.msleep(500)


# основное окно
class MainWindow(QtWidgets.QMainWindow, mainUI.Ui_MainWindow, QtCore.QTimer, QDialog):
	s_mainWin = QtCore.pyqtSignal(bool)

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
			self.lengh_of_track(0)
			self.track_num += 1
			self.is_music_play = True

		elif self.is_music_play == True:
			mixer.music.pause()
			self.is_music_play = False

		elif self.is_music_play == False:
			mixer.music.unpause()
			self.is_music_play = True

	def change_track(self):

		if self.playlist:

			if self.track_num == 0:
				mixer.music.load(self.playlist[self.track_num])
				self.lengh_of_track(self.track_num)
				self.track_num += 1
				mixer.music.play()

			else:
				try:
					mixer.music.load(self.playlist[self.track_num])
					self.lengh_of_track(self.track_num)
					self.track_num += 1
					mixer.music.play()

				except IndexError:
					mixer.music.load(self.playlist[0])
					self.lengh_of_track(0)
					self.track_num = 1
					mixer.music.play()

	def lengh_of_track(self, x):

		a = mixer.Sound(self.playlist[x])
		song_length = a.get_length() / 60
		round(song_length, 3)

		song_length = float("%.2f" % song_length)
		print(song_length)
		self.pb_timeline.setRange(0, song_length)
		
		song_lenght_str = str(song_length).replace('.',':')

		self.lbl_endTime.setText(song_lenght_str)

		if self.is_music_play:
			self.thread.start()
			self.s_mainWin.emit(self.is_music_play)
		else:
			pass
			
	def pb_time(self, cur_time):
		self.pb_timeline.setValue(cur_time)

	@classmethod
	def is_music_play(cls):
		return self.is_music_play



if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()	
    sys.exit(app.exec())
