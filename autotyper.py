#!/usr/bin/python3
#
#
###############################################################
#	
#	Auto typing bot for typeracer.com made by CABREX
#	Takes screenshot of the region with the text to type,
#	converts it into text using Computer Vision and tesseract 
# 	engine. 
#	
#	Make sure the Blue Box having the text and the text box 
#	to type is close to the bottom of the screen 
#	(1cm / 39 pixels preferrably).
#	
###############################################################
#
#



from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Listener as MouseListener
from pynput import keyboard as Keyboard
import time
import pyscreenshot as ImageGrab
import sys
import os

import argparse

import cv2
import pytesseract

keyboard = KeyboardController()

delay = 0.01
iterations_count = 0
char_count = 0
debug_mode = False

# Command line argument options
description = "A bot that automates inputs for typeracer.com"


# Sends keyboard inputs
def typer(string):
	global iterations_count, char_count

	for c in string:
		char_count = char_count + len(c)
		for ch in c:

			if ch == '|' or ch == '||':
				keyboard.press("I")
				keyboard.release("I")

			elif ch == "\n":
				keyboard.press(" ")
				keyboard.release(" ")

			elif ch != "|":
				keyboard.type(ch)
			
			try:
				time.sleep(delay)
			except KeyboardInterrupt:
				print("keyboard interrupt detected")
				stats()
				exit(0)



# Gets the cropped screenshot of the place
def screenshawn():

	x1 = 450
	y1 = 716
	x2 = 1449
	y2 = 889

	# part of the screen
	im=ImageGrab.grab(bbox=(x1, y1, x2, y2))
	# im.show()

	# Saving cropped image to file
	im.save('sample.png')


# Converting sample.png to text by using computer vision and tesseract OCR engine
def refined_message_to_string():
	pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


	img = cv2.imread('sample.png')
	 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	 

	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
	                                                 cv2.CHAIN_APPROX_NONE)

	im2 = img.copy()

	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
	     
	    # Drawing a rectangle on copied image
		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	     
	    # Cropping the text block for giving input to OCR
		cropped = im2[y:y + h, x:x + w]
	     
		# Open a clean file
		if debug_mode:
			with open("recognized.txt", "w") as file:
				file.write("")
	     
		# Apply OCR on the cropped image
		try:
			text = pytesseract.image_to_string(cropped)
		except pytesseract.pytesseract.TesseractNotFoundError:
			print("[ERROR]- Pytesseract not found. Please install")
			exit(0)

	     
		# Appending the text into file
		
		if debug_mode:
			with open("recognized.txt", "a") as file_handle:
				file_handle.write(text)

		yield text


def on_press(key):

	if key == Keyboard.Key.ctrl_r:
		return False



def fetch_coords(x, y, button, pressed):
	coords = mouse.position
	print(x, y)

def callibrate():
	with MouseListener(on_click=fetch_coords) as listener:
		try:
			listener.join()
		except KeyboardInterrupt:
			listener.stop()


def stats():
	print("Stats for the run:")
	print(f"1) Number of iterations: {iterations_count}")
	print(f"2) Total number of characters typed: {char_count}")

def debug_setter(string):
	if string.lower() == "true":
		return True
	elif string.lower() == "false":
		return False
	else:
		return -1




if __name__ == "__main__":

	print("Auto typer bot by CABREX (https://github.com/0xcabrex)")

	# Initialize parser
	parser = argparse.ArgumentParser(description = description)
	parser.add_argument('-d', '--delay', help = "Changes the delay per character (default = 0.01)")
	parser.add_argument('-s', '--setdebug', help = "Toggles debug mode, outputs the cropped image and converted code to file (default False)")
	args = parser.parse_args()

	if args.delay:
		try:
			delay = float(args.delay)
			print(f"Delay has been set to {args.delay}")
		except ValueError:
			print(f"Delay value '{args.delay}' is invalid, please enter a number")
			exit(0)
	if args.setdebug:
		#debug_mode = True if args.setdebug.lower() == "true" else False
		debug_mode = debug_setter(args.setdebug)
		if debug_mode == -1:
			print(f"True and False are only accepted, '{args.setdebug}' is invalid")
			exit(0)
		print(f"Debug mode is set to {debug_mode}")


	print("Bot is running...\n")
	while True:
		print("to exit, ctrl+c and then right control")

		with Keyboard.Listener(on_press=on_press) as listener:
		    try:
		        listener.join()
		        print(f'right control was pressed, image has been captured')
		    except KeyboardInterrupt:
		        print(f"Keyboard interrupt detected")
		        print("\n\n")
		        stats()
		        exit(0)


		screenshawn()


		string = refined_message_to_string()


		with Keyboard.Listener(on_press=on_press) as listener:
			try:
				listener.join()
				print(f'right click was pressed. Auto-typing...')
			except KeyboardInterrupt:
				print(f"Keyboard interrupt detected")
				stats()
				exit(0)

		typer(string)
		print("Done\n")
		if not debug_mode:
			os.remove('sample.png')
		iterations_count += 1

