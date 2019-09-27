import numpy as np
import argparse
import imutils
import matplotlib.pyplot as plt
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    output = frame.copy()
    # Operations
	# Convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)

	# Find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=65, minRadius=5, maxRadius=50)

	# loop over the contours
    for c in cnts:
	    # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

	    # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
		    # compute the bounding box of the approximated contour and
		    # use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
 
		    # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)
 
		    # compute whether or not the width and height, solidity, and
		    # aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
 
		    # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
			    # draw an outline around the target and update the status
			    # text
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                status = "Target(s) Acquired"
 
			    # compute the center of the contour region and draw the
			    # crosshairs
                M = cv2.moments(approx)
                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
                cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)



    # ensure at least some circles were found
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle in the image
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)               
            M = cv2.moments(approx)
            (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
            (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))
            (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))
            cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
            cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)
            #time.sleep(0.5)


    # Show taken images
	# show the frame and record if a key is pressed
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame 2", output)
    key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
