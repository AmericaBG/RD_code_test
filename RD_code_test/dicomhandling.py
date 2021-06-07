# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:23:05 2021

@author: usuario
"""
import sys
import numpy as np 
import os, inspect
import glob
import nibabel as nib
import cv2
from PIL import Image
import scipy
from scipy import ndimage
from pydicom import dcmread
from pathlib import Path
import matplotlib.pyplot as plt

#Clase con métodos comunes

class compartido(object):
    def __init__(self, path):
        self.path=path
        
    def original(self):
        img=dcmread(self.path)
        self. original=img.pixel_array
        return(self.original)
    
    def ipp(self):
        img=dcmread(self.path)
        ipp_list=img.ImagePositionPatient[:]
        return(ipp_list)
        
    
    
    
class DcmFilter(compartido):
    
    def __init__(self, path,sigma=3):
        self.path=path
        self.sigma=sigma
    
    
    def filtered(self):
        filtered_img=ndimage.gaussian_filter(self.original,self.sigma)
        return(filtered_img)
    
    
class DcmRotate(compartido):
    
    def __init__(self, path,angle=180):
        self.path=path
        self.angle=angle
        
    def rotated(self):
        if self.angle%90==0 :
            rotated_image=ndimage.rotate(self.original,self.angle)
        else:
            rotated_image=self.original 
            print("El ángulo debe de ser múltiplo de 90º")
            
        return(rotated_image)
    
def check_ipp(obj1,obj2):
    ipp1=obj1.ipp()
    ipp2=obj2.ipp()
    
    return(ipp1==ipp2)
        
    
    
if __name__ == "__main__":
    
    class IncorrectNumberOfImages(Exception):
        def __init__(self, msg='Incorrect number of images. Aborting'):
            super().__init__(msg)
            
    class SameImagePositionPatient(Exception):
        def __init__(self, msg='The DICOM files appear to be the same. Aborting.'):
            super().__init__(msg)
            
            
    #Lectura del argumento de la línea de comandos
    path_folder=sys.argv[1]
    
    #Examinación de carpeta
    images=os.listdir(path_folder)
    n_imgs=len(images)
    
   #Control de númerode imágenes         
    if n_imgs!=2:
        raise IncorrectNumberOfImages
        
    
    path1=(path_folder+'\\'+images[0])
    path2=(path_folder+'\\'+images[1])
        
    im1_obj=DcmFilter(path1,3)
    im2_obj=DcmFilter(path2,3)
      
    # Control de IPP
    if check_ipp(im1_obj,im2_obj):
        raise SameImagePositionPatient
    
    # Cálculo de los residuos
    unfiltered_res=im1_obj.original()-im2_obj.original()
    filtered_res=im1_obj.filtered()-im2_obj.filtered()
    
    #Creamos la carpeta para almacenar los residuos
    path_residues=(path_folder+'\\residues')
    
    if not os.path.exists(path_residues):
        os.makedirs(path_residues)       
    
    #Guardamos
    plt.imsave((path_residues+'\\unfiltered_residue.jpg'),unfiltered_res)
    plt.imsave((path_residues+'\\filtered_residue.jpg'),filtered_res)
    plt.figure,plt.imshow(filtered_res,cmap="gray")

    
    

    
    
    
    
    

