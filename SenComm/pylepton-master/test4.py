import sys
import numpy as np
import cv2
from pylepton import Lepton

def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l: 
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  print np.max(a)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  return np.uint8(a)

def capture2(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l: 
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  print np.max(a)
  cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(a, 8, a)
  return np.uint8(a)

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

  kernel = np.ones((5,5), np.uint8)

  while True:
      # Capture the raw image
      rawImage = capture(flip_v = options.flip_v, device = options.device)
      max_raw = np.amax(rawImage)
      rawImage2 = capture2(flip_v = options.flip_v, device = options.device)
      max_raw2= np.amax(rawImage2)

      # Level the historgam
      leveled = cv2.equalizeHist(rawImage)
      leveled2 = cv2.equalizeHist(rawImage2)
      max_leveled = np.amax(leveled)
      max_leveled2 = np.amax(leveled2)
      #print max_raw, max_leveled
      # Blur the image
      blurred = cv2.GaussianBlur(leveled,(9,9),0)
      blurred = cv2.GaussianBlur(leveled2,(9,9),0)
     #ret3, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Threshold image


      #res = np.hstack((rawImage, leveled)) 


      ret3, thresholded = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)

      cv2.imshow('image1', thresholded)
      thresholded = cv2.dilate(thresholded, None, iterations=4)
      cv2.imshow('image2', thresholded)
      thresholded = cv2.erode(thresholded, None, iterations=2)
      cv2.imshow('image3', thresholded)


      _, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      
      # Create a sorted array of contour areas from largest to smallest
      areaArray = sorted(contours, key=cv2.contourArea, reverse=True)
      # Find the largest contour and its bounding rectangle
      largestContour = areaArray[0]
      x, y, w, h = cv2.boundingRect(largestContour)
  
      #Find the center of the largest contour
      M = cv2.moments(largestContour)
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])

      minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(rawImage)
      minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(rawImage2)

      if maxVal > 250:
	print "maxVal: %d" % maxVal
        # Draw the center and bounding rectangle if pixel intensity is high enough
        cv2.circle(rawImage, (cX, cY), 3, (255,0,0), -1)
        cv2.rectangle(rawImage, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.circle(rawImage2, (cX, cY), 3, (255,0,0), -1)
        cv2.rectangle(rawImage2, (x,y), (x+w, y+h), (255,0,0), 2)

      # Show image
      cv2.imshow('image', rawImage)
      cv2.imshow('image', rawImage2)
      
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        break

  cv2.imwrite("output.jpeg", rawImage)
  cv2.imwrite("output2.jpeg", rawImage2)
  cv2.destroyAllWindows()
    
    

## imread --> imagesc -->
