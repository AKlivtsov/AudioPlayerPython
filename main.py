from pygame import mixer as audio
import time 

audio.init()

audio.music.load("assets/music_samples/blah.mp3")
audio.music.play()

time.sleep(3)
audio.music.pause()
time.sleep(1)
audio.music.unpause()
time.sleep(99)

print("Done!")