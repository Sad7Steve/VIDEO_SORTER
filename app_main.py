""" 
recquired moduless 
pip install pytube
pip install pytubefix
"""

import os
import time
# import youtube_function as yt
from youtube_function import *


print("="*7+ " Start App " +"="*7)

def MainApp(folder_path, playlist_link, list_of_extension) :
  
  # change current working directory
  os.chdir(folder_path)
  
  # get a filtered copy of files in folder
  t = round(time.time())
  directory_files = getFilesList(folder_path, list_of_extension)
  print(f"getFilesList runtime {round(time.time()) - t} second")
  
  # store each data of file as dictionary in this list
  list_video_metadata = []
  t = round(time.time())
  
  i = 0
  while(i < len(directory_files)):
    file_object = getFileMetadata(folder_path, directory_files[i])
    list_video_metadata.append(file_object)
    i += 1
  
  print(f"getFileMetadata runtime {round(time.time()) - t} second")
  
  
  # store a list of all video in playlist as dictionary
  t = round(time.time())
  ytList_video_metadata = getPlaylistContent(playlist_link)
  print(f"getPlaylistContent runtime {round(time.time()) - t} second")
  
  # print(ytList_video_metadata)
  
  # rename each video in local machine with [order + name + extension] ex: [05] learn c#
  j = 0
  while(j < len( ytList_video_metadata )):
    yt_video = ytList_video_metadata[j]
    
    k = 0
    while(k < len( list_video_metadata )):
      local_video = list_video_metadata[k]
      # print( f"yt_video : {yt_video} => local_video : {local_video}" )
      
      if(yt_video['time'] == local_video['time']):
        # print(f"find file name {yt_video['name']}")
        # generate new name that contain a name and extension from local video and index from youtube
        video_name = generateVideoName(yt_video['name'], yt_video['index'], local_video['extension'])
        
        # get number of file [01] or [27] in the start of file name
        file_name_prefix = local_video['name'][0: local_video['name'].find(']') + 1]
        # print(file_name_prefix) # for testing
        # if file already renamed will skip rest of code to gain proccess time 
        if(file_name_prefix == video_name['affix']): # get [num] in new title
          print(f"the file : {local_video} already exist") # information test msg
        #   break
        
        local_video_path = os.path.join(folder_path, local_video['name']) # get full file path
        renameFile(local_video_path, video_name['name'])
        # ignor this local video in next cycle
        # list_video_metadata.remove(local_video)
        # exit from loop
        break
        
      k += 1
    
    
    j += 1


# user input example test:
# directory_path = os.path.join(os.getcwd(), "./video")
# URL_playlist   = "https://www.youtube.com/playlist?list=PL0LHNc-7k_LAYjlXkmKRYRk0lgh7r4oT3"
extension_list = ["mp4", "mkv"]

directory_path = input("Enter folder path that contain all video : ")
URL_playlist   = input("Enter URL of playlist : ")
# extension_list = input("Enter all extension ex: mp4,mkv: ").split(",")


# calculate code excution time
t0 = round(time.time()) 
MainApp(directory_path, URL_playlist, extension_list)
print(f"the programme runtime {round(time.time()) - t0} second")


# print(directory_path)
# print(URL_playlist)
# print(extension_list)

print("="*7+ " End App " +"="*7)

