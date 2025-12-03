""" 
recquired moduless 
pip install pytube
pip install pytubefix
"""

import os
import time
import youtube_function as yt


print("="*7+ " Start App " +"="*7)

def MainApp(folder_path, playlist_link, list_of_extension) :
  
  # change current working directory
  os.chdir(folder_path)
  
  # get a filtered copy of files in folder
  t = round(time.time())
  directory_files = yt.getFilesList(folder_path, list_of_extension)
  print(f"getFilesList runtime {round(time.time()) - t} second")
  
  # store each data of file as dictionary in this list
  list_video_metadata = []
  t = round(time.time())
  
  i = 0
  while(i < len(directory_files)):
    file_object = yt.getFileMetadata(folder_path, directory_files[i])
    list_video_metadata.append(file_object)
    i += 1
  
  print(f"getFileMetadata runtime {round(time.time()) - t} second")
  
  
  # store a list of all video in playlist as dictionary
  t = round(time.time())
  ytList_video_metadata = yt.getPlaylistContent(playlist_link)
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
        new_title = yt.generateVideoName(local_video['name'], yt_video['index'], local_video['extension'])
        
        
        # get all the sentence before first character ']'  
        file_name_prefix = local_video['name'][0: local_video['name'].find(']') + 1]
        # if file already renamed there we skip to avoid extra renaming 
        # print(file_name_prefix)
        if(file_name_prefix == new_title[0:new_title.find(']') + 1]):
          print(f"the file : {local_video} already exist")
          break
        
        # get full file path
        local_video_path = os.path.join(folder_path, local_video['name'])
        # replace name of local video by new_title
        yt.renameFile(local_video_path, new_title)
        # ignor this local video in future
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

