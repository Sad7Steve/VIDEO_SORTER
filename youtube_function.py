import os
import sys
# import time
from pytubefix import Playlist
from pytubefix import YouTube
from subprocess import run, PIPE

sys.stdout.reconfigure(encoding='utf-8')

# =============== getFilesList ===============


""" 
input: 
  path      : of folder that contain all video we want to rename it => "D://course/"
  extension : all format posible in your video => ["mp4","mkv","mp3",]
output:
  list contain video filtred => ["learn c in 30 min", "learn python in 10 min", "learn git and github"]
The gloal of this function:
  In folder that contain all video maybe found unneccessary element => {
    original list : ["test/", "learn c in 30 min", "learn python in 10 min", "learn git and github", "ttt.txt"]
  }
  This element are represent by : non video file type(py, txt, zip) and all folders
  We want to create a list clean by remove all element unneccessary => {
    element want to remove : ["test/", "ttt.txt"]
  }
"""
# filter file list and remove all element that dosen't match extension list and any directiory 
def getFilesList(path = "", extension = ["mp4"]):
  if(not os.path.isdir(path)): return f"{path} are not an existed folder!"

  os.chdir(path)
  filesList = os.listdir()
  finalList = []
  
  i = 0
  while(i < len(filesList)):
    if(os.path.isdir(filesList[i])):
      i += 1
      continue
    
    currentFile = filesList[i]
    currentFileExtension = currentFile[len(currentFile) - 4: len(currentFile)]
    
    for ext in extension:
      if(currentFileExtension == f".{ext}"):
        finalList.append(currentFile)
        break
    
    i += 1
  
  return finalList


# =============== generateVideoName ===============

# (old_name = "test" , order = 5) => "[05] test .mp4"
def generateVideoName(old_name, order, extension = "mp4"):
  if(order < 10):
    return f"[0{order}] {old_name}.{extension}"
  else:
    return f"[{order}] {old_name}.{extension}"


# print( generateVideoName("test", 5) )
# print( generateVideoName("learn python in less than 10 min", 9) )
# print( generateVideoName("create simple api with fastAPI", 10) )

# ============================================================


# =============== getPlaylistContent (need internet connexion) ===============

# in future we use yt-dlp liberary
def getPlaylistContent(link):
  url_list = list(Playlist(link))
  final_list = []
  
  i = 0
  # while(i < 20):
  while(i < len(url_list)):
    video = YouTube(url_list[i])
    
    video_obj = {}
    video_obj['name'] = video.title
    video_obj['time'] = video.length
    video_obj['url'] = url_list[i]
    video_obj['index'] = i + 1
    
    
    final_list.append(video_obj)
    
    i += 1
  
  return final_list


# test_link = "https://www.youtube.com/playlist?list=PL0LHNc-7k_LAYjlXkmKRYRk0lgh7r4oT3"
# print( getPlaylistContent(test_link) ) # playlist contain 55 video

# ============================================================


# =============== getFileMetadata ===============

def getFileMetadata(path, file):
  # refuse any wrong parameter passed (path can't contain wrong folder path)
  if(not os.path.isdir(path)): return f"{path} are not a valid folder reference"
  # refuse any wrong parameter passed (file can't contain folder path)
  if(os.path.isdir(file)):     return f"{file} are path folder reference"
  
  # get full path + file name (ex: path = D:\\course, file = c in 30 min.mp4) => D:\\course\c in 30 min.mp4
  p = os.path.join(path, file)
  
  # calculate time of video file using get_duration function
  def get_duration(video_file):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_file], stdout=PIPE).stdout)
  
  file_obj = {}
  file_obj['name'] = file
  file_obj['time'] = round(get_duration(p))
  file_obj['extension'] = file[len(file) - 4: len(file)]
  
  return file_obj


# print( getFileMetadata('./video') )
# print( getFileMetadata('./video/test') )

# test_path = os.path.join(os.getcwd(), './video')
# video_01  = os.listdir(test_path)[0] 
# print( getFileMetadata(test_path, video_01) )

# ============================================================


# =============== renameFile ===============

def renameFile(file_path, new_name):
  if(not os.path.isfile(file_path)): return f"{file_path} not a correct path of an exist file"
  os.rename(file_path, new_name)
  return f"{file_path} done"

# print ( renameFile('./ttt.txt', 'test.json') )
# print ( renameFile('./test.txt', 'test.json') )
# time.sleep(3)
# print ( renameFile('./test.json', 'ttt.txt') )