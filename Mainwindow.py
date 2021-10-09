
from kivy.uix.image import Image, Loader 
import cv2
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix import scatter
from functions import Dicom_to_image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.transformation import Matrix
from kivy.uix.scatter import Scatter
from kivy.properties import ObservableDict

import os 
import pydicom as dm
import numpy as np



#global data loaded

stack=[]
WW=0
WL=0
current_location=1






 
class Mywidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        
        
        #self.image_update(current_location, WW,WL)


        #update slider
        slidermax=np.shape(stack)
        self.ids.slider1.max=slidermax[0]-1
        


        
    
    
       
        
    def slider_update(self):
        global WW, WL, current_location
        #get Slider values
        Windowwidth=int(self.ids.windowwidthslider.value)
        Windowlevel=int(self.ids.windowlevelslider.value) 
        current_location_global=int(self.ids.slider1.value)
      


        self.ids.windowlevellabel.text=str(WL)
        self.ids.windowwidthlabel.text=str(WW)

        image=Dicom_to_image(stack[current_location],WL,WW)
        cv2.imwrite('temp.png',image)
        
        self.app.root.ids.imageclass.ids.new_img.source='temp.png'
        self.app.root.ids.imageclass.ids.new_img.reload()        
        
        #print(type(self.ids))
        WW=Windowwidth
        WL=Windowlevel
        current_location=current_location_global
 
        
    





 #main class 





class MyImage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        image=Dicom_to_image(stack[current_location],WL,WW)
        cv2.imwrite('temp.png',image)
        
                
        
    
        


    def image_update(self,current_location, WW,WL):
        
        


        image=Dicom_to_image(stack[current_location],WL,WW)
        cv2.imwrite('temp.png',image)
        self.ids.new_img.source ='temp.png'
        self.ids.new_img.reload()
    


    def on_touch_move(self, touch):  
       
           

        global current_location,WW,WL
        if self.collide_point(*touch.pos):
            x,y=touch.pos

            x2,y2=touch.ppos
            dy=y2-y            
            slidermax=np.shape(stack)

            if dy>=1:
                
                if current_location!=slidermax[0]-1:
                    current_location+=1
                    self.image_update(current_location, WW,WL)
            elif dy<0:
                if current_location!=0:
                    current_location-=1
                    self.image_update(current_location, WW,WL)



      

                
                




class Mainwindow(App): 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            


    

    
    
    def load_data(self):
        global stack
        path=r'path to the dicom folder'
        slice=[dm.dcmread(path+'/'+s) for s in os.listdir(path)]
        slice.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        stack=slice
        
    def build(self):
        self.load_data() 
        
           
        return Mywidget()

#subclass


       
        


   
    

            
            
            
            
            
  
        







    
        

if __name__=="__main__":
    Mainwindow().run()

