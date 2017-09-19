#preprocessing for image scaling

from PIL import Image
import os
import csv
import numpy as np



def main():
	#resize....
	#crop
	input_dir = 'photos32/'
	output_dir = 'cropped16/'
	input_dir2 = 'photos100/'
	output_dir2 = 'cropped50/'
	#crop_m(input_dir, output_dir, 32, 4)
	#crop_m(input_dir2, output_dir2, 100, 4)
	#to csv
	pixeldata_to_csv('cropped16','data/',filename = 'cropped16.csv')
	pixeldata_to_csv('cropped50','data/',filename = 'cropped50.csv')

def resize_all(input_dir, output_dir, img_size, output_dir2=' ', img_size2=0, errors_file='resize_errors.txt'):
    try:
        input_dir  = str(input_dir.rstrip('/'))  #path to img source folder
        output_dir  = str(output_dir.rstrip('/')) #output directory
        print ("Collecting data from %s " % input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print ("Resizing images...")

        for d in os.listdir(input_dir):
            fname, extension = os.path.splitext(d)
            if extension == ".jpg":
                try:
                    img = Image.open(os.path.join(input_dir,d))
                    img = img.resize((img_size,img_size),Image.ANTIALIAS)
                    img.save(os.path.join(output_dir,fname+'.jpg'),"JPEG",quality=90)
                    if img_size2 != 0:
                        img = img.resize((img_size2,img_size2),Image.ANTIALIAS)
                        img.save(os.path.join(output_dir2,fname+'.jpg'),"JPEG",quality=90)
                    print ("Resizing file : %s " % (d))
                except Exception as e:
                    print ("Error resize file : {!s}, will remove from posts.csv and from down dir".format(d))
                    with open(errors_file, 'a') as f:
                        f.write(d+'\n')
                    # sys.exit(1) 
    except Exception as e:
        print ("Error, check Input directory etc : ", e)
        sys.exit(1)

def crop_m(input_dir, output_dir,size,n):
	m = n**(1/2)
	newsize = size/m
	count = 0
	for filename in os.listdir(input_dir):
		img = Image.open(input_dir+filename)
		on = filename[:-4]
		for i in range(n):
			count += 1
			h = i // m
			w = i % m
			area = (w*newsize, h*newsize, (w+1)*newsize, (h+1)*newsize)
			cropped = img.crop(area)
			cropped.save(output_dir+str(count)+'.jpg')
		print(filename,'cropped..')

def pixels(image):
    with Image.open(image) as im:
        pixels = np.array(im.getdata(), dtype=int)
    return pixels

def pixeldata_to_csv(resized_dir, csv_dir, filename):
	#channel first
    pixeldata = np.array([], dtype=int)
    with open(os.path.join(csv_dir,filename), "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for file_name in os.listdir(resized_dir):
            try:
                if file_name.endswith('.jpg'):
                    pixeldata = pixels(resized_dir + os.sep + file_name).reshape(-1,3).T.tolist()
                    writer.writerows(pixeldata)
            except ValueError as e:
                print(e)
                pixeldata = np.repeat(pixels(resized_dir + os.sep + file_name).reshape(-1,1).T, 3, axis=0).tolist()
                writer.writerows(pixeldata)

            except Exception as e:
                print('Exception while saving RGB with file {}'.format(file_name), e)


main()

    
