import os
import ffmpeg


filename = 'test.mp4'
des_filename = 'out.mp4'
data = ffmpeg.probe(filename)
print(data)
ffmpeg.compile
# cmd_commond = "ffmpeg -i "+filename+" -c:f libx264 -q:v 22 "+des_filename
# print(cmd_commond)
# # 这里的filename 表示输入的语音文件路径，des_filename 表示输出的语音文件路径
# os.system(cmd_commond)