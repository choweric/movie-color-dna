# -*- coding: utf-8 -*-

import cv2
import colorsys
import sys
import pandas as pd
import numpy as np


def getFrame(second):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,second*1000)
    hasFrames,image = vidcap.read()  
    return hasFrames,image
    


###################################################
# 1. Variables definition and init
###################################################

video_name = "madmax"
#video_name = "blade_runner_2049"
#video_name = "blade_runner"

frameRate = 5      # frameRate = N; one frame per N second
out_height = 500
write_file = True

v = video_name+".mp4"


count = 1
second = 0

df_hsl=pd.DataFrame(columns=['h', 's', 'l'])
#df_rgb=pd.DataFrame(columns=['r', 'g', 'b'])


###################################################
# 2. Capture video frames and build HSL dataframe
###################################################

vidcap = cv2.VideoCapture(v)

total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vidcap.get(cv2. CAP_PROP_FPS))
total_time_sec = total_frame / fps


success = getFrame(second)

while success:
    
    count = count + 1
    second = second + frameRate
    second = round(second, 2)
    success,image = getFrame(second) #image in BGR (not RGB)
    
    if success:
        
        # Save frame to JPG file
        if write_file:
            cv2.imwrite(video_name+"/image"+str(second)+".jpg", image)  
        
        #Compute average color (RGB) value of frame
        average = image.mean(axis=0).mean(axis=0)   
        b = average[0]
        g = average[1]
        r = average[2]
        #df_rgb.loc[len(df_rgb.index)] = [r, g, b] 
        
        #Converts RGB value to HLS, and store result in a DataFrame
        hls = colorsys.rgb_to_hls(r/255, g/255, b/255) #RGB value are fractional values, need to be converted to 255
        df_hsl.loc[len(df_hsl.index)] = [hls[0], hls[2], hls[1]] 
        
     
    complete = round(second / total_time_sec * 100,2)
    #sys.stdout.write("  [%-20s] %d%%\n" % ('='*int(complete), int(complete/5)))
    
    sys.stdout.write(str(complete)+"% ")
    sys.stdout.flush()
    





###################################################
# 3. Create color sequence (w.r.t time)
###################################################
df = df_hsl
dim = df.shape[0]

out_rect = np.zeros((out_height, dim, 3), dtype=np.uint8)    
start = 0

for index, row in df.iterrows():            
    c = colorsys.hls_to_rgb(row[0],row[2],row[1])
    cv2.rectangle(out_rect, (index, 0), (index+1, out_height), [c[2]*255,c[1]*255,c[0]*255], -1)  #draw by bgr

cv2.imwrite(video_name+"_color_seq.jpg", out_rect)




###################################################
# 4. Sort HSL dataframe and create color map (DNA)
###################################################
df = df_hsl
df = df.sort_values(by=['h','s','l'],ignore_index=True)                  
dim = df.shape[0]

out_rect = np.zeros((out_height, dim, 3), dtype=np.uint8)    
start = 0

for index, row in df.iterrows():            
    c = colorsys.hls_to_rgb(row[0],row[2],row[1])
    cv2.rectangle(out_rect, (index, 0), (index+1, out_height), [c[2]*255,c[1]*255,c[0]*255], -1)  #draw by bgr

cv2.imwrite(video_name+"_dna.jpg", out_rect)

