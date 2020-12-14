
"""
provide the synthetic data with the label
todo list
1. distortion
2. RGB Last then 50
3. Next Thurday presenttaion
4. try the different dataset generation
"""
import os
import random
import string
import scipy.ndimage
import numpy as np
import argparse # future control
from PIL import Image, ImageDraw, ImageFont,ImageColor ,ImageFilter,ImageEnhance
import numpy as np
from skimage import io 
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.restoration import inpaint
# Random english words (upper/lower)
# the length range 1~15 
black=(0,0,0)
white=(255,255,255)
def transformtoGCP(source,gcpfp):
    
    fontlist=source+'labels.csv'#source+fontlist.txt
    GCP=source+'gcplables.csv'#source+fontlist.txt
    fpname=gcpfp

    with open(fontlist,'r') as file:
        exist=[]
        for line in file.readlines():
            exist.append(line)

    with open(GCP,'w') as nfile:
        nfile.write("[set,]image_path[,label]\n")
        for i, ele in enumerate(exist[1:]):
            name,text,gt,x,y=ele.split(',')
            
            if i%8==0:
                T="TEST"
            else:
                T="TRAIN"
            nfile.write(T+','+fpname+name+','+gt.lower()+'\n')
    
            
def updatefontlist(source,update):
    #folders=os.listdir(source)#folders a b c d
    fontlist=source+'/fontlist.txt'#source+fontlist.txt
    #print(os.listdir(source+'/'+update))
    print(fontlist)
    with open(fontlist,'w') as file:
#        file.write("uehor")
        for name in os.listdir(source+'/'+update):
            file.write(str(update+'/'+name)+'\n')
    file.close
                
#    with open(fontlist,'r') as file:
#        exist=[]
#        for line in file.readlines():
#            exist.append(line.split('/')[0])
#    file.close()
#    with open(fontlist,'a') as file:
#        for folder in folders: 
#            if folder=='fontlist.txt':
#                continue
#            if folder in exist:
#                continue
#            else:
#                for name in os.listdir(source+'/'+folder):
#                    file.write(str(folder+'/'+name)+'\n')
            
            
#update the font list in the folder
    
def get_random_string(length):
    letters = string.ascii_lowercase+string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
# need to seperate the combiner!

class Text_render(object):
    def __init__(self, 
                 texts,
                 radius=2,
                 fontsize=random.choice(range(30,50)),
                 fontfp="data/fonts/"):
        #color in the PIL colormap
        self.color=list(ImageColor.colormap.keys())

        #print(self.color)
        #the random texts
        self.texts=texts
        #the fontstate:
        self.fontsize=fontsize
        tmp=open(fontfp+'fontlist.txt', "r").read().split("\n")[:-1]
        self.fontfp=[fontfp+ele for ele in tmp]
        #the output image 
        
        self.r=radius
    def word_only(self):
        res=[]# List of PIL image and the text and the font name
        for text in self.texts:
            
            fontname=random.choice(self.fontfp)
            try:
                font=ImageFont.truetype(fontname,self.fontsize)
            except OSError:
                continue

            #textpos=font.getsize(text)[0],font.getsize(text)[1]
            image=Image.new("RGB",(font.getsize(text)[0],font.getsize(text)[1]),white)
            draw=ImageDraw.Draw(image)
            draw.text((0,0),text,black,font=font)
            #image=image.filter(ImageFilter.GaussianBlur(radius=self.r))
            #image.show(image)
            lablefont=fontname.split('/')[3].split('.')[0]
            res.append([image,text,lablefont])
            
        return res
    
    def forward(self):
        res=[]# List of PIL image and the text and the font name
        for text in self.texts:
            image=Image.new("RGB",(self.outsize),(0,0,0))
            fontname=random.choice(self.fontfp)
            try:
                font=ImageFont.truetype(fontname,self.fontsize)
            except OSError:
                continue
            draw=ImageDraw.Draw(image)
            try:
                textpos=(random.choice(range(1,image.width-font.getsize(text)[0])),
                         random.choice(range(1,image.height-font.getsize(text)[1])))
            except IndexError:
                continue
            
            draw.text(textpos,text,random.choice(self.color),font=font)
            #image=image.filter(ImageFilter.GaussianBlur(radius=self.r))
            lablefont=fontname.split('/')[3].split('.')[0]
            res.append([image,text,lablefont,textpos])
        return res
class Textcombiner(object):
    # task combine the render text and the background
    def __init__(self, 
                 input,#with image, text, fontfp name, textpos
                 outsize=(640,480),
                 bgsource="data/background_render",
                 outdir="dataset/ArialFamilyTest"):
        #color in the PIL colormap
        self.outsize=outsize
        self.input=input
        #the background image 
        self.imdir=bgsource
        #the output dir
        self.output=outdir
        

    def combine(self):
        # return the label and the image
        label=[]
        images=[]
        for row in self.input:
            try:
#                background = io.imread(self.imdir+"/"+random.choice(os.listdir(self.imdir))
                name=self.imdir+"/"+random.choice(os.listdir(self.imdir))
                background=Image.open(name)
#                background =row[0]
            except OSError:
                continue
            
            
            mask=row[0] # mask of text
            text=row[1]
            font=row[2]
            #position=row[3]
            
            image=mask.copy()
            width=image.size[0]
            height=image.size[1]
            pixels = image.load() 
            bpixels = background.load() 
            bwidth=abs(background.size[0]-width)+1
            bheight=background.size[1]-height
            rc0=random.choice(range(0,bwidth))
            rc1=random.choice(range(height,bheight))
            for i in range(width):
                for j in range(height):
                    try:
                        if pixels[i,j]==white:
                            pixels[i,j]=bpixels[rc0+i,rc1+j]
                    except IndexError:
                        print(background.size)
                        print(name)
            #image=self.mask_blur(10,mask,image,background)
            images.append(image)
            label.append([text,font]) #position
            
        return images, label
    def mask_blur(self,blur,mask,image,background):
        image=image.filter(ImageFilter.GaussianBlur(radius=blur))
        width=image.size[0]
        height=image.size[1]
        pixels = image.load() 
        bpixels = mask.load() 
        bbpixels= background.load()
        for i in range(width):
            for j in range(height):
                if bpixels[i,j]==white:
                    pixels[i,j]=bbpixels[i,j]
        return image
    def colorenhace(self, image):
        converter = ImageEnhance.Color(image)
        img2 = converter.enhance(0.5)
        return img2

    def save_file(self,images,labels):
        try:
            with open(self.output+'/'+'labels.csv','r') as f:
                cur=len(f.readlines())
            with open(self.output+'/'+'labels.csv','a') as f:
                for i , im in enumerate(images) :
                    name=str(cur+i)+".png"
                    im.save(name)
                    os.replace(name,self.output+'/'+name)
                    f.write("%s,%s,%s\n"%(name,labels[i][0],labels[i][1].split('.')[0].lower()))
        except FileNotFoundError:
            cur=0
            os.mkdir(self.output)
            with open(self.output+'/'+'labels.csv','w') as f:
                f.write("name,text,font,x,y\n")
                for i , im in enumerate(images) :
                    name=str(cur+i)+".png"
                    im.save(name)
                    os.replace(name,self.output+'/'+name)
                    f.write("%s,%s,%s\n"%(name,labels[i][0],labels[i][1].split('.')[0].lower()))

    def forward(self):
        images,labels=self.combine()
        self.save_file(images,labels)
#todo mask blur
#setup the environment of producet the dataset
#
        
    

# paint the background
        
"""
label: contain the position(box) of the text, and the font of the text pair<imagename: [font,position]>
text: size, color , font
"""
def background_render(input,output):
    import cv2
    
    image = cv2.imread(input) #Image of cat with text watermark
    #image=cv2.resize(image,(640,480))
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    # Morph open to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    erosion = cv2.erode(thresh,kernel,iterations = 0)
    dilate = cv2.dilate(erosion, kernel, iterations=4)
    
    result=cv2.inpaint(image,dilate,3,cv2.INPAINT_NS)
    fig, axes = plt.subplots(ncols=2, nrows=2)
    ax = axes.ravel()

    ax[0].set_title('thresh')
    ax[0].imshow(thresh, cmap=plt.cm.gray)
#
#    ax[1].set_title('opening')
#    ax[1].imshow(opening, cmap=plt.cm.gray)
#
    ax[2].set_title('image')
    ax[2].imshow(image)
#
    ax[3].set_title('result')
    ax[3].imshow(result)
    #cv2.imshow('thresh', dilate)
    #cv2.imshow('dilate', dilate)
    #cv2.imshow('result', result)
    number=str(len(os.listdir(output)))
    cv2.imwrite(output+'/'+number+".jpg",result)
    #cv2.waitKey()
if __name__=='__main__':
    # use parser to check out the using parameters
#    output='./data/background_render'
#    imdir='./data/background'
#    for filename in os.listdir(imdir):
#        curf=imdir+'/'+filename# the image file in dir
    background_render('bc.jpg','./')
        
        
#    updatefontlist('data/fonts','win-fonts')
#    transform=False
#    if (transform):
#        transformtoGCP("dataset/","gs://synfont/")
#    else:
#        #updatefontlist("data/fonts/")
#        texts=[]
#        for i in range(100):
#            texts.append(get_random_string(random.choice(range(8,23))))
#        T=Text_render(texts)
#        output=T.word_only()
#        T1=Textcombiner(output,outdir="dataset/Test")
#        T1.forward()
    
"""
reference
"""
#print(os.listdir("data/background"))
#print(random.choice(os.listdir("data/background")))
#https://www.geeksforgeeks.org/python-pil-gaussianblur-method/
#https://www.tutorialspoint.com/python/python_tuples.htm
#https://stackoverflow.com/questions/41528576/how-can-i-write-text-on-an-image-and-not-go-outside-of-the-border
#https://www.w3schools.com/python/python_try_except.asp
#https://pynative.com/python-generate-random-string/
#https://www.w3schools.com/python/python_file_open.asp
#https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ImageColor.html
#https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names
#https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
#https://stackoverflow.com/questions/8858008/how-to-move-a-file
#https://www.geeksforgeeks.org/python-pil-imagedraw-draw-text/
#https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
#https://github.com/ankush-me/SynthText/blob/master/synthgen.py
#https://predictivehacks.com/iterate-over-image-pixels/
