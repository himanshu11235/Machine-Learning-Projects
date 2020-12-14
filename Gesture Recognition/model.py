
import tensorflow as tf
import numpy as np
import operator
import cv2
import sys, os
import vlc

#update this variable with path of the .hdf5 filwe downloaded by you
weights_addr = "/home/lucy/Desktop/m_3_3.h5"

model = tf.keras.models.load_model(weights_addr)
# Category dictionary
dct = {'P' : 0, 'F' : 1, 'G' : 2, 'K': 3, 'L':4, 'Y':5, 'nothing':6}
arr = ['P', 'F', 'G', 'K', 'L', 'Y','nothing']

Gesture_meanings = {'P' : 'play', 'F' : 'seek_forwards', 'G' : 'pause', 'K' : 'vol down', 'L' : 'vol up', 'Y' : 'seek_backwards', 'nothing':'nothing'}

play_state = 1
seek_time = 5000
volume_change = 20

cont = 1


idx = int(input("Enter the camera Index :"))
idx = 0
video = cv2.VideoCapture(idx)

path = input("Enter the path to media  file :")
path = "/home/lucy/test.mkv"
player = vlc.MediaPlayer(path)

if(player.will_play() != 0):
	print("cant play your media")
	cont = 0

a = player.play()

if(a != 0):
	print("could not open the media")
	cont = 0

#player.set_fullscreen()
# audio_get_volume, audio_set_volume, audio_get_mute, audio_set_mute
#player.set_mute(0)
index_prev = 0
delta_t = 0
thresh_delta_t = 20
while cont:
    
	#print("Mplayer_state: ", player.get_state())
	
	_, frame = video.read()
    
	x1 = int(0.5*frame.shape[1])
	y1 = 10
	x2 = frame.shape[1]-10
	y2 = int(0.5*frame.shape[1])

	cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)

	roi = frame[y1:y2, x1:x2]

	# Resizing the ROI so it can be fed to the model for prediction
	roi = cv2.resize(roi, (64, 64)) 
	#roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	roi = roi/127 -1 
	#roi = np.concatenate((roi, roi, roi), axis = -1)   
	#_, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
	#cv2.imshow("test", test_image)

	result = model.predict(roi.reshape(1, 64, 64, 3))
	prediction = result[0]
	index = np.argmax(prediction)
	print(index)
	if(index == index_prev):
		delta_t += 1
	else:
		delta_t = 0
	index_prev = index
	if(delta_t > thresh_delta_t):

		if (index == 0):
			a = player.play()
			if(a == 0):
				print(index, arr[index] ,"played")
				play_state = 1			
			else:
				print("could not play :")
				cont = 0
			delta_t = 0
		elif (index == 1):
			current_time = player.get_time()
			next_time = min(player.get_length() - 50, current_time + seek_time)
			player.set_time(next_time)
			print(index, arr[index] ,"seek forward")
			delta_t = 0
		
		elif (index == 2):
			if(play_state == 1):
				player.pause()
				play_state = 0
			print(index, arr[index] ,"paused")
			delta_t = 0
				
		elif (index == 4):
			current_vol = player.audio_get_volume()
			next_volume = current_vol + volume_change
			if(next_volume > 200):
				next_volume = 200
			player.audio_set_volume(next_volume)
			delta_t = 0
			print(index, arr[index] ,"vol up")
		elif (index == 5):
			current_time = player.get_time()
			next_time = max(50, current_time - seek_time)
			player.set_time(next_time)
			print(index, arr[index] ,"seek backward")
			delta_t = 0
		elif (index == 3):
			current_vol = player.audio_get_volume()
			next_volume = current_vol - volume_change
			if(next_volume < 0):
				next_volume = 0
			player.audio_set_volume(next_volume)
			delta_t = 0
			print(index, arr[index] ,"vol down")
		elif (index == 6):
			print(index, arr[index] , "no action")
	
	cv2.imshow("Frame", frame)
	
	interrupt = cv2.waitKey(10)
	if interrupt & 0xFF == 27: # esc key
		break
		
 
video.release()
cv2.destroyAllWindows()
