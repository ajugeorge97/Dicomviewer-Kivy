import pydicom as dm
import numpy as np
import os
import time
import matplotlib.pyplot as plt




def dicom_stack(path):
    slice=[dm.dcmread(path+'/'+s) for s in os.listdir(path)]
    slice.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    image = np.stack([s.pixel_array for s in slice])
    # Covert to 16 bit
    image = image.astype(np.int16)

    return image


def calcpixel(pixelarray,wmin,wmax):
    value=((pixelarray-wmin)/(wmax-wmin))*255
    return value


def Dicom_to_image(img,WL,WW):
    
    if (img.get(0x00281052) is None):
        Rescaleintercept=0
    else:
        Rescaleintercept = int(img.get(0x00281052).value)
    if (img.get(0x00281053) is None):
        Rescaleslope=1
    else:
        Rescaleslope=int(img.get(0x00281053).value)

    Window_Center=WW
    Window_Width=WL
    Window_Max = int(Window_Center + Window_Width / 2)
    Window_Min = int(Window_Center - Window_Width / 2)

    pixel_array=img.pixel_array
    
    pixel_array=pixel_array*Rescaleslope + Rescaleintercept

    #WW & WL conditions for outside scope
    pixel_array=np.where(pixel_array>Window_Max,255,pixel_array)
    pixel_array=np.where(pixel_array<Window_Min,0,pixel_array)

    pixel_array = np.where(((pixel_array > Window_Min) & (pixel_array < Window_Max)), calcpixel(pixel_array,Window_Min,Window_Max),pixel_array)

    return pixel_array
