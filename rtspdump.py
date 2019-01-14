#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import datetime, os, fnmatch, shutil, subprocess, time
storage_dir='/media/hdd/'
storage_size=1800 #storage in GB
target_folder_list=[]
if storage_dir.endswith('/')==False:
	storage_dir+='/'

def folder_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size/1000000000 #return size in GB




while True:
	destdate = datetime.datetime.now().strftime("%Y_%m_%d")
	desttime = datetime.datetime.now().strftime("%H-%M-%S")
	if folder_size(storage_dir)>storage_size-1:
		for file in os.listdir(storage_dir):
			if fnmatch.fnmatch(file, '????_??_??'):
				target_folder_list.append(file)
		target_folder_list.sort()
		print(str(folder_size(storage_dir)) +' more than '+	str(storage_size-1)+' deleting...')
		shutil.rmtree(storage_dir+target_folder_list[0],ignore_errors=True)
	if os.path.exists(storage_dir+destdate+'/')==False:
		os.mkdir(storage_dir+destdate+'/')
	cam1cmd=["ffmpeg","-i", "rtsp://192.168.1.1:554/user=user_password=password_channel=1_stream=0.sdp?real_stream", "-t", "00:10:00","-vcodec", "copy", storage_dir+destdate+"/cam1_"+desttime+".mp4"]
	cam2cmd=["ffmpeg","-i", "rtsp://192.168.1.2:554/user=user_password=password_channel=1_stream=0.sdp?real_stream", "-t", "00:10:00","-vcodec", "copy","-an",storage_dir+destdate+"/cam2_"+desttime+".mp4"]
	subprocess.Popen(cam1cmd)
	subprocess.Popen(cam2cmd)
	time.sleep(589)
