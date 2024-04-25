import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob

classes = ['hand1', 'hand2', 'hand3', 'hand4']
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
    
def convert_annotation(image_name,prePath = './train/'):
    in_file_path = prePath + 'ann/'
    out_file_path = prePath + 'labels/'
    if not os.path.exists(out_file_path):
        os.mkdir(out_file_path)

    in_file = open(in_file_path + image_name[:-3] + 'xml')
    out_file = open(out_file_path + image_name[:-3] + 'txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + ' ' +  ' '.join([str(a) for a in bb]) + '\n')
        
wd = getcwd()

if __name__ == '__main__':

    trainPrepath = './train/'
    for image_path in glob.glob(trainPrepath + 'images/*.jpg'):
        image_name = image_path.split('\\')[-1]
        # print(image_path)
        convert_annotation(image_name,trainPrepath)

    validPrepath = './valid/'
    for image_path in glob.glob(validPrepath + 'images/*.jpg'):
        image_name = image_path.split('\\')[-1]
        # print(image_path)
        convert_annotation(image_name,validPrepath)