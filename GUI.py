#GUI for out smoke detector

from light_utilities import *
from tkinter import *
import tkinter.font as font
from time import sleep
import webbrowser
from threading import Thread
from Gas_Detection_Test import *
import multiprocessing
import sys

f = open('DS.txt', 'r+')
f.truncate(15)
f.write("False")

green_lights=[18]
red_lights=[19,20]
set_up(green_lights)
set_up(red_lights)


root = Tk()
root.geometry("780x440")
root["bg"] = "grey5"




#main function that brings up main menu
#it first tries to get rid of the messag menu if it is up
def Main_GUI_Function():
    root.title("SSM")
    main_menu()
    loop()
    check()
	
#THIS DELETS THE MAIN MENU
#THEN IT BRINGS UP THE MESSAGE MENU
#ITS PRETTY MUCH THE 2ND MAIN FUNCTION 
def messageFAQs():
    global root2
    root2=Tk()
    root2.title("Message details")
    root2.geometry("780x440")
    root2["bg"] = "grey5"
    message_menu()
    loop2()
    #start_label("Explanation of our Message System", "deep sky blue" )
    

#functions for displaying the gas output
#function to continually display the gas output
def display_gas_output():
        global process3, checker
        process3=multiprocessing.Process(target=output)
        checker = Thread(target=check)
        gas_main()
        process3.daemon=True
        process3.start()
        checker.start()
        detection.config(state=DISABLED)
        
#pauses gas sensor reading, cna be resumed with gas detection button
def stop_all():
        try:
            process3.terminate()
            process3.join()
            detection.config(state=NORMAL)
        except:
                print("USER HAS NOT STARTED THE GAS SENSOR")

#converts file string to boolean value
def convert_bool(a_string):
        str(a_string)
        if ("F" in a_string):
                return False
        if ("T" in a_string):
                return True
        
#changes safety/danger status
def changeDN(bool_value):
    if bool_value == True:
        gas_output.config(text="STATUS: DANGEROUS", bg="red")
        off_all(green_lights)
        danger_lights(red_lights)
        off_all(red_lights)
    if bool_value == False:
        off_all(red_lights)
        normal_lights(green_lights)
        gas_output.configure(text="STATUS: NORMAL", bg="blue")

#function to alter visual danger/safety status
def check():
    f=open('DS.txt', 'r')
    danger_string=f.read()
    f.close
    danger_status=convert_bool(danger_string)
    changeDN(danger_status)
    #if stop_thread == True:
        #chcker.pause()
    sleep(1)
    check()
                        
#puts the title label on main menu
def start_label(name, color):
	title = StringVar()
	global title_label
	

def message_menu():
	#message FAQs frame
	global MFAQ, maker_label_msg
	MFAQ = Frame(root2, bg="grey5", height=420)

	title_label = Label(MFAQ, anchor = CENTER, width=750, height=2,\
		text="Messaging System Info", relief=RAISED, bg="cyan", fg="black",\
                font=("Gill Sans", 12), bd=4)
	#text widget to display our documentation of our messaging system
	T = Text(MFAQ, height=7, bg="grey6", fg="white", wrap=WORD, spacing2=3,\
                 font=14, bd=10, relief=RAISED)
	T.insert(INSERT, "For our project we incorperated Twilio Messaging service. Twilio\
	is a programable messaging service that allows you to pruchase phone numbers. From\
	there you can incorporate the phone numbers within you code to accomplish all your messaging needs.\
	To message a non-Twilio phone number you must first register your phone with your twilio account on\
	their website. We have provided a link to Twilios HomePage below.")

	#label for our names on the GUI
	maker_label_msg=Label(root2, bg="grey5", fg="red", text="a DND product")
	#link to twilio for the user to go too
	link = Label(MFAQ, text="Twilio HomePage", bg="grey5", fg="purple", cursor="hand2")
	link.bind("<Button-1>", lambda e: callback("https://www.twilio.com/what-is-cloud-communications?\
		msclkid=ebaf789cccd416ca76a219166dc54502&utm_source=bing&utm_medium=\
		cpc&utm_campaign=B_S_NAMER_Brand_Twilio&utm_term=twilio&utm_content=Twilio%20-%20Phrase") )

	MFAQ.pack(fill="both")
	title_label.pack(side=TOP, anchor=N)
	T.pack(side=TOP, anchor=N)
	maker_label_msg.pack(side=RIGHT, anchor=SE)
	#back_button.pack(side=LEFT, anchor=NW)
	link.pack(side=BOTTOM, anchor=S)

#creates the Frames of our main menu
def main_menu():
	#smoke Frame
	global smoke_frame, utilities_frame, gas_output
	global gas_output2, detection, msgInfo
	smoke_frame_title = StringVar()
	smoke_frame = Frame(root, width=390, bg="grey5")
	smoke_frame_title.set("Gas Readouts")
	smoke_frame_label=Label(smoke_frame, anchor=CENTER, bd=10, bg="green yellow",\
	fg="grey5", relief="raised", textvariable=smoke_frame_title)
	smoke_frame.pack_propagate(0)
	title_label = Label(root, anchor = CENTER, width=750, height=2,\
		text="Smart Smoke Detector", relief=RAISED, bg="seashell4", fg="black",\
                font=("Gill Sans", 12), bd=4)
	title_label.pack_propagate(0)
	title_label.pack(side=TOP, anchor=N)

	#label for our gas output readings
	gas_output=Label(smoke_frame, height=4, width=50, font=12, bd=5, relief=GROOVE,\
                        bg="blue", fg="black", text="STATUS: NORMAL")
	gas_output2=Label(smoke_frame, height=4, width=50, font=12, bd=5, relief=GROOVE,\
                          bg="red", fg="black", text="STATUS: DANGEROUS")
	#packing smoke_frame and its attributes
	smoke_frame.pack(side=LEFT, fill="y", expand=False)
	smoke_frame_label.pack()
	gas_output.pack()

	#utilities Frame
	utilities_title = StringVar()
	utilities_frame = Frame(root, width=375, bg="dark slate gray")

	#label for our names on the GUI
	maker_label=Label(utilities_frame, bg="dark slate gray", fg="red", text="a DND product")

	#utilities frame title
	utilities_frame_label = Label(utilities_frame, bd=5, anchor=CENTER,\
		textvariable=utilities_title, bg="black", fg="tomato",\
		relief="raised")
	utilities_title.set("Utilities Menu")
	utilities_frame.pack(side=RIGHT, fill="y")
	utilities_frame_label.pack()

	#Buttons for utility frame
	msg = Button(utilities_frame, relief=RAISED, height=1, width=50, bg="mint cream",\
		text="Messages On/Off",activebackground="black", bd=10, cursor="hand2")
	detection = Button(utilities_frame, relief=RAISED, height=1, width=50, bg="mint cream",\
	 	text="Activate Gas Sensor", activebackground="black", bd=10, cursor="hand2",\
                          command=lambda : display_gas_output())
	msgInfo = Button(utilities_frame, relief=RAISED, height=1, width=50,bg="mint cream",\
		command=lambda : messageFAQs(), text="More Info on Messages",\
		activebackground="black", bd=10, cursor="hand2")
	power = Button(utilities_frame, relief=RAISED, height=1, width=50,\
	 	text="Emergency Stop", bg="tomato", command=lambda : stop_all(), activebackground="black",\
	 	bd=10, cursor="hand2")

	buttons = [msg, detection, msgInfo, power]
	for i in buttons:
		i.pack(pady=10)
	maker_label.pack(side=RIGHT, anchor=SE)


#MISCELANOUS FUNCTIONS
#loops the root
def loop():
    root.mainloop()
def loop2():
    root2.mainloop()
#used to open a url for our message documentation
def callback(url):
	webbrowser.open_new(url)

