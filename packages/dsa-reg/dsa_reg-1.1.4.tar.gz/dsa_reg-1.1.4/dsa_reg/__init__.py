import json
import girder_client
from PIL import Image, ImageFile
import sys
from io import BytesIO 
import numpy as np
import requests

import cv2
import base64

from skimage import measure
import getpass

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

def alignImages(im1, im2, im1colored,  enhanceFlag):
  """
  This follows OpenCV example...https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/ 
  """
  """
  :param im1: ref image
  :param im2: target image
  :param enhanceFlag: boolen (0,1)  
  :return: homography metrix and registered imaage
  """ 

  # Convert images to grayscale
  if (enhanceFlag==0):
   im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)   # image to align
   im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)   # Ref image
   
  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(MAX_FEATURES)
  if (enhanceFlag==0):
   keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
   keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
  else:
   keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
   keypoints2, descriptors2 = orb.detectAndCompute(im2, None) 
   
  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)
   
  # Sort matches by score
  matches.sort(key=lambda x: x.distance, reverse=False)
 
  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]
 
  
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
 
  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
   
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

  if(enhanceFlag==0):
   height, width, channels = im2.shape
   im1Reg = cv2.warpPerspective(im1, h, (width, height)) 
  else:
   height, width = im2.shape
   im1Reg = cv2.warpPerspective(im1colored, h, (width, height)) 
 
   
  return im1Reg,  np.round(h, 3), height, width
 




def itemRegistration(refURL, targetURL, xBaseUrl, xAuthentication, xEnhancement):
  """
  This follows OpenCV example...https://www.learnopencv.com/image-alignment-feature-based-using-opencv-c-python/ 
  """
  """
  :param refURL (string): ref image URL 
  :param targetURL (string): target image URL
  :param xBaseUrl (string): DSA Server URL e.g. https://styx.neurology.emory.edu/girder/api/v1
  :param xAuthentication: boolen (0,1)  
  :param xEnhancement: boolen (0,1)  
  :return (Dict): homography metrix, psnr, thumb width and height
  """ 
  if(xAuthentication):
    xDSA_User = raw_input("Login name :")
    xPassword = getpass.getpass("Enter password :")
    gc = girder_client.GirderClient(apiUrl=xBaseUrl)
    gc.authenticate(username=xDSA_User, password=xPassword)
    refResponse = gc.get(refURL, jsonResp=False)
    targetResponse = gc.get(targetURL, jsonResp=False)    
  else:
    refResponse = requests.get(xBaseUrl + refURL)
    targetResponse = requests.get(xBaseUrl + targetURL)     
  imReference = np.array(Image.open(BytesIO(refResponse.content)))
  im = np.array(Image.open(BytesIO(targetResponse.content)))
    
  if(xEnhancement==0): 
    imReg, h, height, width = alignImages(im, imReference, im,  xEnhancement)
  else:
    imReferenceGray = cv2.cvtColor(imReference, cv2.COLOR_BGR2GRAY)
    blurRef = cv2.GaussianBlur(imReferenceGray,(5,5),0)
    retRef,imReference_OTSU = cv2.threshold(blurRef,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    imGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurIm = cv2.GaussianBlur(imGray,(5,5),0)
    retIm,im_OTSU = cv2.threshold(blurIm,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    imReg, h, height, width  = alignImages(im_OTSU, imReference_OTSU, im,  xEnhancement)


  resutls = {'Hemography':'','thumbWidth':'','thumbHeight':'','psnr':'', 'x':'', 'y':'','scaleX':'','scaleY':''} ;
  resutls['Hemography'] = h
  resutls['thumbWidth'] = width
  resutls['thumbHeight']= height
  resutls['psnr'] = measure.compare_psnr( np.array(imReference),imReg)
  resutls['x'] = h[0][2]
  resutls['y'] = h[1][2]
  resutls['scaleX'] = h[0][0]
  resutls['scaleY'] = h[1][1]
  return resutls



def rigidRegByThumb(refItemId, targetItemId, xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1",xAuthentication = 0, xEnhancement = 0):
  refURL = "/item/" + str(refItemId) + "/tiles/thumbnail?encoding=JPEG"
  targetURL = "/item/" + str(targetItemId) + "/tiles/thumbnail?encoding=JPEG"
  return   itemRegistration(refURL, targetURL, xBaseUrl, xAuthentication , xEnhancement)




def rigidRegByMagnification(refItemId, targetItemId, xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1", magnification= 1,  xAuthentication = 0, xEnhancement = 0):
  refURL = "/item/" + str(refItemId) + "/tiles/region?units=base_pixels&magnification=" + str(magnification) + "&exact=false&encoding=JPEG&jpegQuality=95&jpegSubsampling=0"
  targetURL = "/item/" + str(targetItemId) + "/tiles/region?units=base_pixels&magnification=" + str(magnification) + "&exact=false&encoding=JPEG&jpegQuality=95&jpegSubsampling=0"
  return   itemRegistration(refURL, targetURL, xBaseUrl, xAuthentication , xEnhancement)


