from tkinter import *
from tkinter import filedialog,ttk,simpledialog
import cv2 as cv
from PIL import Image, ImageTk
import time
import numpy as np

# http://50.231.121.221/axis-cgi/mjpg/video.cgi
#video file
video_capture = None
isPaused = True
fps = None
speed = 1
def get_photo_from_frame(frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Resize frame to fit in video player
        resized_frame = cv.resize(rgb_frame, (1200, 600))
        # Convert the resized frame to a PhotoImage from numPy array
        # representing openCV frame to PhotoImage
        photo = ImageTk.PhotoImage(Image.fromarray(resized_frame))
        return photo
        # lblVideoFrame.config(image=photo)
        # Keeping reference of image to avoid garbage collection
        # lblVideoFrame.image = photo

def set_first_frame(capVideo):
    if(capVideo.isOpened()):
        global video_capture
        global fps
        video_capture = capVideo
        fps = video_capture.get(cv.CAP_PROP_FPS) 
        ret,frame = capVideo.read()
        photo =  get_photo_from_frame(frame)
        lblVideoFrame.config(image=photo)
        # Keeping reference of image to avoid garbage collection
        lblVideoFrame.image = photo
        print(capVideo.get(cv.CAP_PROP_FRAME_HEIGHT))
        return True
    else:
        return False

def on_Browse_Clicked():
    selected_video_path = filedialog.askopenfilename(title="Select a video", filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")])
    capVideo =  cv.VideoCapture(selected_video_path)
    # capVideo =  cv.VideoCapture("http://50.231.121.221/axis-cgi/mjpg/video.cgi")
    if(set_first_frame(capVideo)):
        lblVideoName.config(text=selected_video_path)
        print("video opended")
    else:
        print("video not opened")

def open_modal():
    def open_primary_camera():
        capVideo =  cv.VideoCapture(0)
        if(set_first_frame(capVideo)):
            lblVideoName.config(text="Primary Camera")
            print("video opended")
            destroy_modal()
        else:
            print("video not opened")

    def open_secondary_camera():
        capVideo =  cv.VideoCapture(1)
        if(set_first_frame(capVideo)):
            lblVideoName.config(text="Secondary Camera")
            print("video opended")
            destroy_modal()

        else:
            print("video not opened")

    def destroy_modal():
        modal_window.destroy()
    
    # Create a new Toplevel window (modal dialog)
    modal_window = Toplevel(rootWindow)
    modal_window.title("Select Camera")

    # Add widgets to the modal window
    btnPrimaryCam = Button(modal_window,text="Primary Camera",command=open_primary_camera)
    btnPrimaryCam.pack(pady=5)

    btnSecondaryCam = Button(modal_window,text="Secondary Camera",command=open_secondary_camera)
    btnSecondaryCam.pack(pady=5)

    # Add a close button to close the modal window
    close_button = Button(modal_window, text="Close", command=modal_window.destroy)
    close_button.pack(pady=10)
    
    modal_window.geometry("+{}+{}".format(
    rootWindow.winfo_screenwidth() // 2 -modal_window.winfo_reqwidth() // 2,
    rootWindow.winfo_screenheight() // 2 -modal_window.winfo_reqheight() // 2
    ))

    modal_window.transient(rootWindow)
    modal_window.grab_set()
    rootWindow.wait_window(modal_window)
    # rootWindow.grab_release()


def get_screen_resolution():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def set_frame_color(frame):
    if(cbxColorVar.get() == "Color"):
        return frame
    elif (cbxColorVar.get() == "GrayScale"):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        return frame
    elif (cbxColorVar.get() == "B/W"):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frame = cv.adaptiveThreshold(
        frame, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 4
    )
        return frame
    elif cbxColorVar.get() == "RedChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,0] = z
        frame[:,:,1] = z
        return frame
    elif cbxColorVar.get() == "BlueChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,1] = z
        frame[:,:,2] = z
        return frame
    elif cbxColorVar.get() == "GreenChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,0] = z
        frame[:,:,2] = z
        return frame
        
    

def play_pause_video():
    global isPaused
    if isPaused == True:
        isPaused = False
        global video_capture

        while(not isPaused):
            start_time = time.time()
            ret,frame = video_capture.read()

            if(not ret):
                video_capture.set(cv.CAP_PROP_POS_FRAMES, 0)
                break

            frame =  set_frame_color(frame)
            photo = get_photo_from_frame(frame)
            lblVideoFrame.config(image=photo)
            lblVideoFrame.image = photo
            rootWindow.update()

            # Calculate the time taken to process a frame
            elapsed_time = time.time() - start_time
            delay = max(0,1/(speed*fps) - elapsed_time) # Here i use max to avoid negative values
            time.sleep(delay)
    else:
        isPaused = True
        rootWindow.update()

def on_speed_change(event):
    global speed
    speed = int(cbxSpeedVar.get())

def on_Color_Change(event):
    global color
    if(cbxColorVar.get() == "GrayScale"):
        color = cv.COLOR_BGR2GRAY

# Function to resize image
def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)



#Initializing root window
rootWindow = Tk()
screen_width, screen_height = get_screen_resolution()
rootWindow.geometry(f"{screen_width}x{screen_height}")
rootWindow.columnconfigure(0, weight=1)  # col 0 use any available space
# Set a theme for ttk
style = ttk.Style()
style.theme_use('clam')  # or ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# Container for video name and browse Button
frameHeader = ttk.Frame(rootWindow, padding="5 5 5 5")
frameHeader.grid(row=0, column=0, pady=10, padx=40, sticky="ew")  # Increased padding for outer margin
frameHeader.columnconfigure(0, weight=1)

# Camera Icon Button
iconCamera = PhotoImage(file='camIcon.png')  # Ensure this path is correct
iconCamera = resize_image('camIcon.png', 75, 75)
btnCamera = ttk.Button(frameHeader, image=iconCamera, command=open_modal)
btnCamera.grid(row=0, column=0, padx=20, pady=10, sticky="w")

# Label That display video name
lblVideoName = ttk.Label(frameHeader, text="Video Address", width=200)
lblVideoName.grid(row=0, column=1, padx=5)

# Define a custom style for the button
style.configure('Custom.TButton', foreground='white', background='#4682B4')

# Map background and foreground colors for different button states
style.map('Custom.TButton',
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '!disabled', 'blue'), ('active', 'blue')])

# Browse Button
btnBrowse = ttk.Button(frameHeader, text="Browse", command=on_Browse_Clicked, style='Custom.TButton')
btnBrowse.grid(row=0, column=2, padx=10)

#Video Player
frameVideoPlayer = ttk.Frame(rootWindow, padding="5 5 5 5", relief=SOLID)
frameVideoPlayer = Frame(rootWindow,height=600,width=1200, padx=5, pady=5, bd=2, relief=SOLID)
frameVideoPlayer.grid(row=1,column=0)

# Set grid_propagate to False to maintain the specified size
frameVideoPlayer.pack_propagate(False)
lblVideoFrame = Label(frameVideoPlayer)
lblVideoFrame.pack()

# Video Options Panel
frameVideoOption = ttk.Frame(rootWindow, padding="5 5 5 5")
frameVideoOption.grid(row=2, column=0, padx=550, pady=10, sticky="ew")

# Play and Pause Button with Icon
iconPause = PhotoImage(file='playPauseIcon.png')  # Ensure this path is correct
iconPause = resize_image('playPauseIcon.png', 30, 30)
btnPause = ttk.Button(frameVideoOption, image=iconPause, command=play_pause_video)
btnPause.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Speed Combobox
cbxSpeedVar = StringVar()
cbxSpeed = ttk.Combobox(frameVideoOption, textvariable=cbxSpeedVar, values=["1", "2", "3"], state="readonly")
cbxSpeed.set("1")  # Default value
cbxSpeed.grid(row=0, column=2, padx=10, pady=10, sticky="w")

# Color Combobox
cbxColorVar = StringVar()
cbxColor = ttk.Combobox(frameVideoOption, textvariable=cbxColorVar, values=["Color", "GrayScale", "B/W", "RedChannel", "GreenChannel", "BlueChannel"], state="readonly")
cbxColor.set("Color")  # Default value
cbxColor.grid(row=0, column=3, padx=10, pady=10, sticky="w")

rootWindow.mainloop()