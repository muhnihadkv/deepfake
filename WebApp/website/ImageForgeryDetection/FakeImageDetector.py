import numpy as np
import os
import cv2 as cv
from PIL import Image,ImageChops,ImageEnhance,ImageFilter,ImageDraw
from keras.models import load_model

resaved_filename = os.getcwd()+'/media/tempresaved.jpg'


class FID:

    def prepare_image(self,fname):
        image_size = (128, 128)
        return np.array(self.convert_to_ela_image(fname,90).resize(image_size)).flatten() / 255.0
    
    def convert_to_ela_image(self,path,quality):

      print('-----------path--------------',path)
      original_image = Image.open(path).convert('RGB')

      resaved_file_name = resaved_filename  
      original_image.save(resaved_file_name,'JPEG',quality=quality)
      resaved_image = Image.open(resaved_file_name)

      ela_image = ImageChops.difference(original_image,resaved_image)
      
      extrema = ela_image.getextrema()
      max_difference = max([pix[1] for pix in extrema])
      if max_difference ==0:
         max_difference = 1
      scale = 255.0 / max_difference
      
      ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
      return ela_image
    
    def predict_result(self,fname):
       model=load_model('C:/Users/LENOVO/OneDrive/Desktop/FAKEYE/AI/proposed_ela_50_casia_fidac.h5')
       class_names = ['Forged', 'Authentic']
       test_image = self.prepare_image(fname)
       test_image = test_image.reshape(-1, 128, 128, 3)
       y_pred = model.predict(test_image)
       print('y_pred====',y_pred)
       y_pred_class = int(round(y_pred[0][0]))
      
       prediction= class_names[y_pred_class]
       if y_pred <= 0.5:
          confidence = f'{(1-(y_pred[0][0])) * 100:0.2f}'
       else:
          confidence = f'{(y_pred[0][0]) * 100:0.2f}'
       return (prediction, confidence)
    
    def show_ela(self, file_path,sl=50):
      
      intensity=sl
      ela_im=self.convert_to_ela_image(file_path, 90)
      ela_im.save(resaved_filename, 'JPEG')

      return ela_im
    
    def detect_edges(self, path):
      image = Image.open(path)   
      image = image.convert("L") #Converting to greyscale
      image = image.filter(ImageFilter.FIND_EDGES)
      image = np.array(image.resize((256,256)))
      image = np.reshape(image, (256, 256))
      edge_im = Image.fromarray(image)
      edge_im.save(resaved_filename, 'JPEG')
      return edge_im
    
    def noise_analysis(self, path, quality, intensity):
      filename = path
      resaved_filename = 'tempresaved.jpg'
      
      im = Image.open(filename).convert('L')
      im.save(resaved_filename, 'JPEG', quality = quality)
      resaved_im = Image.open(resaved_filename)
      
      na_im = ImageChops.difference(im, resaved_im)
      
      extrema = na_im.getextrema()
      max_diff = max([ex for ex in extrema])
      if max_diff == 0:
         max_diff = 1      
      na_im = ImageEnhance.Brightness(na_im).enhance(intensity)
      return na_im

    def apply_na(self, file_path, sl=50):
      intensity=sl
      na=self.noise_analysis(file_path, 90, intensity)
      na.save(resaved_filename, 'JPEG')
      return na
    

