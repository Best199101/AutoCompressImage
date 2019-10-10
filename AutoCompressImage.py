#!/usr/local/bin/python3
# -*- coding: utf-8 -*-



import os.path
import tinify, os
import shutil
import time

__author__ = 'fei'
__date__ = '2019/9/24'

# 请替换为自己申请的Key
tinify.key = 'WWrP9sdH2qSk1LWTRL5ZRN38PTtNJllx'

class CompressImg ():
    def __init__ (self, finder):
        self.png_path = []
        self.finder = finder
    
    def get_img_path(self, finder):
        for p in os.listdir(finder):
            temp_path = os.path.join(finder, p)

            if temp_path.endswith('Assets.xcassets'):

                print('过滤输出路径')

            else :
                if os.path.isdir(temp_path):

                    self.get_img_path(temp_path)
                else:
                    if os.path.splitext(p)[1] == '.png' or os.path.splitext(p)[1] == '.jpg' or os.path.splitext(p)[1] == '.jpeg' or os.path.splitext(p)[1] == '.bmp' or os.path.splitext(p)[1] == '.json':
                        self.png_path.append(os.path.join(finder, p))

            
    
    def handle_compress (self):
        for file in self.png_path:
            self.compress_file(os.path.abspath(file))
    
    def compress_file (self, inputFile):
        print('-----------------compress start-----------------')
        if not os.path.isfile(inputFile):
        
            return
        else:
            dirname  = os.path.dirname(inputFile)
            basename = os.path.basename(inputFile)
            fileName, fileSuffix = os.path.splitext(basename)
            print('dirname=%s, basename=%s, fileName=%s, fileSuffix=%s' % (dirname, basename, fileName, fileSuffix))

            outFile = self.finder + '/Assets.xcassets' + dirname[len(self.finder):]

            print('outFile=%s' % outFile)

            self.mkdir(outFile)

            if fileSuffix == '.png' or fileSuffix == '.jpg' or fileSuffix == '.jpeg' or fileSuffix == '.bmp':

                png_path = outFile + '/' + basename

                print('png_path=%s' % png_path)

                # time.sleep(100)

                self.compress(inputFile, png_path)
            elif fileSuffix == '.json':

                json_path = outFile

                print('json_path=%s' % json_path)

                # time.sleep(100)

                shutil.copy2(inputFile,json_path)
            else:
                print(f'{fileName}不支持该文件类型压缩!')
        print('-----------------compress end-----------------')
    
    def compress (self, inputFile, outputFile):
        source = tinify.from_file(inputFile)
        source.to_file(outputFile)

        # with open(outputFile, 'rb') as source:
        #     source_data = source.read()
        #     result_data = tinify.from_buffer(source_data).to_buffer()

        print(f'{inputFile}压缩成功!')
    
    def mkdir (self, path):
        exist = os.path.exists(path)
        if not exist:
            print(f'建了一个名字叫做{path}的文件夹！')
            os.makedirs(path)
            return True
        else:
            print(f'名字叫做{path}的文件夹已经存在了！')
            return False
def cStart ():
    
    finder = os.getcwd()
    try:
        tinify.validate()
        if tinify.compression_count < 500:
            print(f'本月已压缩图片次数{tinify.compression_count}')
            ci = CompressImg(finder)
            ci.get_img_path(finder)
            ci.handle_compress()
            # ci.handle_copy()

        else:
            print(f'本月压缩图片次数不足')
    except tinify.Error as e:
        print(f'{e}error')

if __name__ == '__main__':
    cStart()