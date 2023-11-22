import threading
import numpy
import pyautogui
import time
import cv2


class ScreenRecordModule():
    DURATION = 5
    SCREEN_SIZE = (1920, 1080)  # these variables set the ground rules and shouldn't be changed
    FPS = 25.0                  # anything higher then this breaks the program, I am trying to find a new method
    frame_buffer = []           # This is where all the frames get stored


    # captures a screenshot and writes it to the framebuffer
    def captureScreenshot(self, frame_number):
                time.sleep((1/self.FPS)*frame_number) 
                img = pyautogui.screenshot()
                frame = numpy.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_buffer.append(frame)


    # this function does the actual process of recording the screen
    def recordScreen(self, duration):
        self.DURATION = duration # sets the duration

        # create the video object 
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output = cv2.VideoWriter("output.avi", fourcc, self.FPS, self.SCREEN_SIZE)
        thread_buffer = [] # serves a similar purpose to the frame buffer

        # create a thread for each screenshot
        for frame in range(self.DURATION*int(self.FPS)):
            t = threading.Thread(target=self.captureScreenshot, args=(frame,))
            thread_buffer.append(t)


        # actually capture each screenshot
        for thread in thread_buffer:
            thread.start()

        # wait a few seconds added to the duration just in case
        time.sleep(3+self.DURATION)
        
        # write the frames
        for frame in self.frame_buffer:
            output.write(frame)

        # release the output
        cv2.destroyAllWindows()
        output.release()
