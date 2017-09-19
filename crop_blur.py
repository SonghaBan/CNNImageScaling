from PIL import Image, ImageFilter
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

input_dir = 'resized/'
count = 0

def crop_blur():
    for filename in os.listdir(input_dir):
    	im = Image.open(input_dir+filename)
    	img = im.filter(ImageFilter.GaussianBlur(radius=1))
    	on = filename[:-4]
    	for i in range(64):
    		count = count+1
    		h = i // 8
    		w = (i+1) % 8
    		area = ((w-1)*32, h*32, w*32, (h+1)*32)
    		cropped = im.crop(area)
    		cropped.save('cropped/'+str(count)+'.jpg')
    		bc = img.crop(area)
    		bc.save('blurred/'+str(count)+'.jpg')
    		if count % 1000 == 0 :
    			print(filename, 'cropped and blurred..')



def check_blurred():
    filenamelist = []
    for i in range(1,65):
        filenamelist.append(str(i)+'.jpg')
    original = combine_images('cropped', filenamelist)
    blurred = combine_images('blurred',filenamelist)
    original.show()
    blurred.show()
    

def combine_images(path,filenamelist):
    result = Image.new("RGB", (256, 256))
    for i in range(len(filenamelist)):
        filename = filenamelist[i]
        img = Image.open(path+os.sep+filename)
        img.thumbnail((32,32), Image.ANTIALIAS)
        h = i // 8
        w = (i+1) % 8
        area = ((w-1)*32, h*32, w*32, (h+1)*32)
        result.paste(img, area)
    return result

check_blurred()

