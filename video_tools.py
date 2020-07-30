import sys
import os
import cv2
import pandas as pd
import numpy as np
import glob

def decode_fourcc(v):
    v = int(v)
    fourcc = ("".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])).upper()
    
    return fourcc

def divideVideo(src_path, dst_dir, start_frame=0, end_frame=None):
    vcap = cv2.VideoCapture(path)

    if(vcap.isOpened()):

        vcap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        if(not os.path.exists(dst_dir)):
            os.makedirs(dst_dir)
            print("Create dir:",dst_dir)
 
        origin_fourcc = decode_fourcc(vcap.get(cv2.CAP_PROP_FOURCC))
        origin_fps = vcap.get(cv2.CAP_PROP_FPS)
        origin_width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        origin_height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("FOURCC:",origin_fourcc)
        print("FPS :",origin_fps)
        print("WIDTH :",origin_width)
        print("HIGHT :",origin_height)
        prop_df = pd.DataFrame({"Fourcc":origin_fourcc,
                                "Fps":origin_fps,
                                "Width":origin_width,
                                "Height":origin_height},index=['i',])
        prop_df.to_csv(dst_dir+"/OriginalProps.csv",index=False)
            
        while True:
            frame_count = int(vcap.get(cv2.CAP_PROP_POS_FRAMES))
            #print(frame_count)
            
            if(end_frame is not None):
                if(frame_count > end_frame):
                    break


            ret, frame = vcap.read()

            if ret:
                cv2.imwrite(dst_dir+"/img_{:06d}.png".format(frame_count),frame)
            else:
                break
        #cv2.imshow("debug",frame)

        #cv2.waitKey(0)
    vcap.release()
        
def combineImages(src_dir, dst_path):
    filenames = glob.glob(src_dir+"/*.png")
    #print(filenames)
    
    prop_df = pd.read_csv(src_dir+"/OriginalProps.csv")
    
    origin_fourcc = np.array(prop_df["Fourcc"])[0]
    print(origin_fourcc)
    origin_fps = np.array(prop_df["Fps"])[0]
    print(origin_fps)
    origin_width = np.array(prop_df["Width"])[0]
    print(origin_width)
    origin_height = np.array(prop_df["Height"])[0]
    
    fourcc = cv2.VideoWriter_fourcc(*origin_fourcc)  #fourccを定義
    writer = cv2.VideoWriter(dst_path,fourcc, origin_fps, (origin_height,origin_width))  #動画書込準備

    for filename in filenames:
        frame = cv2.imread(filename)
        
        print(frame.shape)
        
        writer.write(frame)
    
    writer.release()

    