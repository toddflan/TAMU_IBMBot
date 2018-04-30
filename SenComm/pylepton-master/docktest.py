import sys
import serial
import subprocess    # to call scripts
import time
import cmd
import numpy as np
import cv2
from pylepton import Lepton

# open serial port
ser = serial.Serial("/dev/ttyS0")		# ttyS0 is Todd's pi's UART
ser.baudrate = 115200


# define capture function 
def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  #np.right_shift(a, 8, a)
  return np.uint16(a)

# define moving average function
def movingaverage(ema, current_val):
  average = (ema*0.7 + current_val*0.3)
  average = round(average, 0)
  return(int(average))

############################################ Main ##########################################
if __name__ == '__main__':
  from optparse import OptionParser

  usage = "usage: %prog [options] output_file[.format]"
  parser = OptionParser(usage=usage)

  parser.add_option("-f", "--flip-vertical",
                    action="store_true", dest="flip_v", default=False,
                    help="flip the output image vertically")

  parser.add_option("-d", "--device",
                    dest="device", default="/dev/spidev0.0",
                    help="specify the spi device node (might be /dev/spidev0.1 on a newer device)")

  (options, args) = parser.parse_args()

  # instantiate variables
  kernel = np.ones((5,5), np.uint8)
  iteration = 0
  old1 = 0
  old2 = 0
  turns = 0


  while True:
    dock_x = 40  # x value of lights
    # Capture the raw image
    rawIm = capture(flip_v = options.flip_v, device = options.device)
    count = 0
    for i in range(len(rawIm)):
      for j in range(len(rawIm[i])):
        if rawIm[i][j] > 8200:
	  print(j)
          dock_x = j
#          count += 1
#    if count < 175:
#      if turns < 30:
#        print("There aint nobody home")
#        turns = turns + 1
#        if ser.isOpen():
#          val = 81
#          ser.write(str(unichr(val)))
#      else:  # alert user we lost them
#        subprocess.call("./lost_user.sh", shell=True)
#        turns = 0
    else:
      turns = 0 
      cv2.normalize(rawIm, rawIm, 0, 65535, cv2.NORM_MINMAX)
      rawImage = cv2.convertScaleAbs(rawIm, alpha = 255.0/65535.0)
      
      # Level the historgam
      leveled = cv2.equalizeHist(rawImage)

      # Image processing (blur, threshold, dilate & erode)
      blurred = cv2.GaussianBlur(leveled,(9,9),0)
      ret3, thresholded = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)
      thresholded = cv2.dilate(thresholded, None, iterations=4)
      thresholded = cv2.erode(thresholded, None, iterations=2)

      _, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
      
      areaArray = sorted(contours, key=cv2.contourArea, reverse=True) # Create a sorted array of contour areas from largest to smallest
      largestContour = areaArray[0] # Find the largest contour and its bounding rectangle
      x, y, w, h = cv2.boundingRect(largestContour)

      # Find the center of the largest contour
      M = cv2.moments(largestContour)
      cX = int(M["m10"] / M["m00"]) #THIS IS THE IMPORTANT COORDINATE
      cY = int(M["m01"] / M["m00"])

      ################################
      if iteration == 0:
        old1 = cX
        old2 = cX
        ema = cX
        iteration = 1
      else:
        ema = movingaverage(ema, cX)
        print("cX = ", cX, ", EMA = ", ema)
        old2 = old1
        old1 = cX
      ################################


      # Send coordinates to other Pi
        if ser.isOpen():
          #print("SENDING DATA! :-)")
          ser.write(str(unichr(dock_x)))	# was ema not cX

      minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(rawImage)

      #if maxVal > 210:
        # Draw the center and bounding rectangle if pixel intensity is high enough
      cv2.circle(rawImage, (cX, cY), 3, (255,0,0), -1)
      cv2.rectangle(rawImage, (x,y), (x+w, y+h), (255,0,0), 2)

#      cv2.imshow('image', rawImage)
      cv2.imwrite("yunowork.jpeg", rawImage)

      # Wait key
      key = cv2.waitKey(1) & 0xFF      
      if key == ord('q'):
        break

  cv2.destroyAllWindows()
