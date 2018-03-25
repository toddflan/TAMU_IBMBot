import sys, time, cmd
import numpy as np
import cv2
from pylepton import Lepton
sys.path.insert(0, '../Dexter/GoPiGo3/Software/Python')
import easygopigo3 as easy



def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
  #cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
  #np.right_shift(a, 8, a)
  return np.uint16(a)

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

  # Create an instance of the GoPiGo3 class.
  # GPG will be the GoPiGo3 object.
  gpg = easy.EasyGoPiGo3()

  while True:
      # Capture the raw image
      rawIm = capture(flip_v = options.flip_v, device = options.device)
      count = 0
      for i in range(len(rawIm)):
        for j in range(len(rawIm[i])):
          if rawIm[i][j] > 8050:
            count += 1
      print("Count: ", count)
      if count < 1200:
        print("There aint nobody home")
      else:
        cv2.normalize(rawIm, rawIm, 0, 65535, cv2.NORM_MINMAX)
        #np.right_shift(rawImage, 8, rawImage)
        rawImage = cv2.convertScaleAbs(rawIm, alpha = 255.0/65535.0)
        #np.uint8(rawImage)
        #max_raw = np.amax(rawImage)
        

        # Level the historgam
        leveled = cv2.equalizeHist(rawImage)
        #max_leveled = np.amax(leveled)
        #print(max_raw, max_leveled)
        # Blur the image
        blurred = cv2.GaussianBlur(leveled,(9,9),0)
        # ret3, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Threshold image


        #res = np.hstack((rawImage, leveled)) 


        ret3, thresholded = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)
        thresholded = cv2.dilate(thresholded, None, iterations=4)
        thresholded = cv2.erode(thresholded, None, iterations=2)


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

        if maxVal > 210:
          # Draw the center and bounding rectangle if pixel intensity is high enough
          cv2.circle(rawImage, (cX, cY), 3, (255,0,0), -1)
          cv2.rectangle(rawImage, (x,y), (x+w, y+h), (255,0,0), 2)
        print(cX)
        if (cX < 50 or cX > 30):
          gpg.stop()
          print("Chill")
        elif(cX > 50):
          gpg.right()
        elif(cX < 30):
          gpg.left()
        else:
          gpg.stop()
          print("error?")
        
        # Show image
        cv2.imshow('image', rawImage)
      
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
          break

  #cv2.imwrite("output.jpeg", rawImage)
  cv2.destroyAllWindows()
    
    

## imread --> imagesc -->
