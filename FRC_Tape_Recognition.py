import cv2
import numpy as np
from networktables import NetworkTables

def printValues(event, x, y, flags, param):
	global mouseX, mouseY;
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print(f"x: {x} y: {y}");
		vals = hsv[y,x]; #Prints bgr values, regardless of the image shown
		#vals = hsv[y,x];  #Prints hsv values, regardless of the image shown
		print(f"vals:{vals}");



print ("here1")
#inputStream = cv2.VideoCapture("http://roborio-7411-frc.local:1181/?action=stream")
inputStream = cv2.VideoCapture("http://10.74.11.2:1181/?action=stream")

print ("here2")
screen_res = 1920, 1080;

NetworkTables.initialize(server='10.74.11.2');
smartDashboard = NetworkTables.getTable('SmartDashboard');


#inputStream = cv2.VideoCapture(0);
if not inputStream.isOpened():
	print ("File not opened")

ret, inputImage = inputStream.read();
inputImage = cv2.rotate(inputImage, cv2.ROTATE_90_CLOCKWISE)


width = screen_res[0] / inputImage.shape[1];
height = screen_res[1] / inputImage.shape[0];
scale = min(width, height);
newWidth = int(inputImage.shape[1] * scale);
newHeight = int(inputImage.shape[0] * scale);

cv2.namedWindow('Display', cv2.WINDOW_NORMAL);

cv2.resizeWindow('Display', newWidth, newHeight);

print ("here3")

#lowerBoundRGB = np.array([0, 180, 75]);
#upperBoundRGB = np.array([15, 255, 115]);

lowerBoundRGB = np.array([0, 15, 0]);
upperBoundRGB = np.array([210, 256, 140]);

windowLowerRGB = np.array([240, 240, 240]);
windowUpperRGB = np.array([256, 256, 256]);

lowerBoundHSV = np.array([80, 0, 50]);
upperBoundHSV = np.array([170, 110, 255]);

lowerBoundHSVWhite = np.array([235, 235, 210]);
upperBoundHSVWhite = np.array([255, 255, 255]);

lowerBoundTargetHSV = np.array([60, 220, 50]);
upperBoundTargetHSV = np.array([90, 256, 150]);

cv2.setMouseCallback('Display', printValues);
openingKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2));
dilationKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 9));
secondDilationKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13,13));

while(True):
	ret, frame = inputStream.read();
	if ret:
		frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		#cv2.imshow("Output", frame);

		maskedVersion = cv2.inRange(frame, lowerBoundRGB, upperBoundRGB)
		maskedWhite = cv2.bitwise_not(cv2.inRange(hsv, lowerBoundHSVWhite, upperBoundHSVWhite));
		maskedVersion = cv2.bitwise_and(maskedVersion, maskedWhite)
		maskedHSV = cv2.bitwise_not(cv2.inRange(hsv, lowerBoundHSV, upperBoundHSV));
		maskedHSVTarget = cv2.inRange(hsv, lowerBoundTargetHSV, upperBoundTargetHSV);
		maskedHSV = cv2.bitwise_and(maskedHSV, maskedHSVTarget);

		maskedVersion = cv2.bitwise_and(maskedVersion, maskedHSV);

		#dilatedVersion = cv2.dilate(maskedVersion, dilationKernel);
		#openedVersion = cv2.morphologyEx(maskedVersion, cv2.MORPH_OPEN, openingKernel);
		dilatedMask = cv2.dilate(maskedVersion, dilationKernel);
		#cv2.imshow('Display', dilatedMask);

		edged = cv2.Canny(dilatedMask, 100, 200);

		dilatedEdges = cv2.dilate(edged, secondDilationKernel);

		contours, hierarchy = cv2.findContours(dilatedEdges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);


		#M = cv2.moments(dilatedEdges);
		#if M["m00"] != 0:
		#	cX = int(M["m10"] / M["m00"]);
		#	cY = int(M["m01"] / M["m00"]);
		#else:
		#	cX = -1;
		#	cY = 0;

		#if cX != -1:
		#	deltaX = (inputImage.shape[1]/2) - cX;
		#	cv2.circle(frame, (cX, cY), 5, (255,255,255), -1);
		#	smartDashboard.putNumber('deltaX', deltaX);
		#else:
		#	smartDashboard.putNumber('deltaX', 0);

		largestArea = 0;
		largestIndex = -1;
		currIndex = 0;

		for c in contours:
			contourArea = cv2.contourArea(c)
			if (contourArea > largestArea and contourArea > 150):
				largestArea = contourArea;
				largestIndex = currIndex;
			currIndex = currIndex + 1;


		if largestIndex >= 0:
			cv2.drawContours(frame, contours[largestIndex], -1, (255,255,255), 2);
			#print(cv2.contourArea(contours[largestIndex]))
			x,y,w,h = cv2.boundingRect(contours[largestIndex]);
			posX = int(x + (w/2));
			posY = int(y + (h/2));
			polyApprox = cv2.approxPolyDP(contours[largestIndex], 0.04* cv2.arcLength(contours[largestIndex], True), True)
			if(len(polyApprox) >= 5 and len(polyApprox) <= 8):
				#print(len(polyApprox));
				cv2.circle(frame, (posX, posY), 5, (255,255,255), -1);
				deltaX = (inputImage.shape[1]/2) - posX
				smartDashboard.putNumber('deltaX', deltaX)
		else:
			smartDashboard.putNumber('deltaX', 0)

		cv2.imshow("Display", frame);

		#cv2.imwrite("testFrameHSV.jpg", hsvVersion);
		#cv2.imwrite("testFrameRGB.jpg", frame);



		cv2.waitKey(1);

	else:
		smartDashboard.putNumber('deltaX', 0);

inputStream.release();
cv2.destroyAllWindows();