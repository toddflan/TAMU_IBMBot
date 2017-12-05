import sys
import numpy as np
import cv2
from pylepton import Lepton

def capture(flip_v = False, device = "/dev/spidev0.0"):
  with Lepton(device) as l:
    a,_ = l.capture()
  if flip_v:
    cv2.flip(a,0,a)
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
      # CApture the raw image
      rawImage = capture(flip_v = options.flip_v, device = options.device)
      # Level the historgam
      leveled = cv2.equalizeHist(rawImage)
      # Blur the image
      blurred = cv2.GaussianBlur(leveled,(9,9),0)
     #ret3, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Threshold image

      ret3, thresholded = cv2.threshold(blurred, 190, 255, cv2.THRESH_BINARY)
      thresholded = cv2.erode(thresholded, None, iterations=2)
      thresholded = cv2.dilate(thresholded, None, iterations=4)
    
      ##Remove small connected objects
##      nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(I3, 8, cv2.CV_32S)
##      sizes = stats[1:,-1]; nb_components = nb_components - 1
##
##      min_size = 150
##
##      I3 = np.zeros((output.shape))
##
##      for i in range(0, nb_components):
##        if sizes[i] >= min_size:
##          I3[output == i+1] = 255

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

      if maxVal > 240:
        # Draw the center and bounding rectangle if pixel intensity is high enough
        cv2.circle(rawImage, (cX, cY), 3, (255,0,0), -1)
        cv2.rectangle(rawImage, (x,y), (x+w, y+h), (255,0,0), 2)

      # Show image
      cv2.imshow('image', rawImage)
      
      key = cv2.waitKey(1) & 0xFF
      if key == ord('q'):
        break

  cv2.imwrite("output.jpeg", rawImage)
  cv2.destroyAllWindows()
    
    

##canny edge detector, blur every frame before using this
##threshold then contour
## imread --> imagesc -->
