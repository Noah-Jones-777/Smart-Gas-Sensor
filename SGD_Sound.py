from pygame import mixer
mixer.init()
sound = mixer.Sound("gentex_cammander_3_code_3_horn-Brandon-938131891.wav")
def play_annoying_sound():
	sound.play()
