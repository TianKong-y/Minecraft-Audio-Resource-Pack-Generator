"""
音频资源包生成器v1.0.0 powered by bilibili@TianKong_y
使用方法
1.将需要生成资源包的音频放入audios文件夹
2.运行main.py
	2.1输入资源包名称、最低支持的版本
3.在resource_pack文件夹中输出资源包文件
"""

import os
import shutil

def process(file_path, file_name):
	global last
	shutil.copy(file_path, target)
	tmp = file_name[:-4] #去掉".ogg"
	last = '"' + tmp + '"' + ':{"sounds":[{"name":"' + namespace + '/' + tmp + '"}]}'

def print_version():
	print("""音频资源包生成器v1.0.0 powered by bilibili@TianKong_y
使用方法
1.将需要生成资源包的音频放入audios文件夹
2.按照此界面的提示输入资源包基础信息
3.在resource_pack文件夹中找到生成的资源包文件夹，自行压缩为zip文件""")
	print("注意事项:")
	print("1.audios文件夹中的音频文件名只能为英文/下划线")
	print("2.音频的后缀名必须为.ogg")
	print("3.调用方法为: /playsound minecraft:{音频名称(无后缀名)}")

def input_information():
	global name, namespace, version, description
	name = input("请输入资源包的名称:")
	namespace = input("请输入命名空间名称(只能为英文/下划线，否则会调用失败):")
	print("1.6.1(13w24a)–1.8.9                 => 1")
	print("1.9(15w31a)–1.10.2                  => 2")
	print("1.11(16w32a)–1.12.2(17w47b)         => 3")
	print("1.13(17w48a)–1.14.4(19w46b)         => 4")
	print("1.15(1.15-pre1)–1.16.1(1.16.2-pre3) => 5")
	print("1.16.2(1.16.2-rc1)–1.16.5           => 6")
	print("1.17(20w45a)–1.17.1(21w38a)         => 7")
	print("1.18(21w39a)–1.18.2(1.18.2-rc1)     => 8")
	print("1.19(22w11a)                        => 9")
	version = input("请输入资源包的版本:")
	while(int(version) < 1 | int(version) > 9):
		version = input("请输入正确的资源包的版本:")
	description = input("请输入资源包描述:")

def init():
	global main_path, fileList, tmp_folder, target, mcmeta, sounds_json
	main_path = os.path.abspath('')
	fileList = os.listdir(main_path + "\\audios")


	tmp_folder = main_path + "\\resource_pack\\" + name
	if os.path.exists(tmp_folder):
		shutil.rmtree(tmp_folder, ignore_errors=True)
	os.makedirs(tmp_folder)
	if not os.path.exists(tmp_folder + "\\assets"):
		os.makedirs(tmp_folder + "\\assets")
	if not os.path.exists(tmp_folder + "\\assets\\minecraft"):
		os.makedirs(tmp_folder + "\\assets\\minecraft")
	if not os.path.exists(tmp_folder + "\\assets\\minecraft\\sounds"):
		os.makedirs(tmp_folder + "\\assets\\minecraft\\sounds")
	if not os.path.exists(tmp_folder + "\\assets\\minecraft\\sounds\\" + namespace):
		os.makedirs(tmp_folder + "\\assets\\minecraft\\sounds\\" + namespace)
	target = tmp_folder + "\\assets\\minecraft\\sounds\\" + namespace + "\\"

	mcmeta = open(tmp_folder + "\\pack.mcmeta", "w")
	mcmeta.write('{\n')
	mcmeta.write('  "pack": {\n')
	mcmeta.write('    "pack_format": ' + version + ',\n')
	mcmeta.write('    "description": "'+ description + '"\n')
	mcmeta.write('  }\n')
	mcmeta.write('}\n')

	sounds_json = open(tmp_folder + "\\assets\\minecraft\\sounds.json", "w")
	sounds_json.write("{\n")

print_version()
input_information()
init()

flag = 1
last = ""

for tmp in fileList:
	if(flag == 0):
		sounds_json.write(last + ",\n")
	flag = 0
	process(main_path + "\\audios\\" + tmp, tmp)

sounds_json.write(last + "\n")
sounds_json.write("}")

print("资源包生成完毕，请在resource_pack文件夹下找到输出资源包文件夹，自行压缩")