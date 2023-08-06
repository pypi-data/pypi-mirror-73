# coding=UTF-8
"""
import matplotlib.pyplot as plt
from skimage import io as skio
from skimage import transform
import pandas as pd
import shutil
import keras
from keras import layers
import time
import warnings
warnings.filterwarnings("ignore")
"""
import os, zipfile
import re
import cv2
import json
import math
import random
import requests
import time, datetime
import subprocess
import hashlib
import numpy as np
import pandas as pd
from PIL import Image
from skimage import io as skio
from requests_toolbelt.multipart import encoder

class video2image():

    def __init__(self, name='', image_resize=(30,30)):
        """
        video2image构造函数，传入名称name和目标图片尺寸image_resize
        """
        if name == '':
            self.name = str(int(time.time()))
        else:
            self.name = name
        self._path = self.name + "_imgs"
        self.image_resize = image_resize
        self.video_index = -1
        self.has_converted = False
        
        if os.path.exists(self._path):
            
            if os.path.exists(self._path + "/config.json"):
                with open(self._path + "/config.json", 'r') as f:
                    try:
                        config = json.load(f)
                        if "image_resize" in config.keys() and config["image_resize"] == list(image_resize) and config["video_index"] >= 0:
                            self.video_index = config["video_index"]
                            self.has_converted = True
                            return
                    except:
                        pass
                   
            os.remove( self._path + "/config.json" )
            if os.path.exists(self._path + "/images"):
                for f in os.listdir( self._path + "/images" ):
                    fp = os.path.join( self._path, "images", f)
                    if os.path.isfile(fp):  os.remove( fp )
            else:
                os.mkdir( self._path + "/images" )
        else:
            os.mkdir( self._path )
            os.mkdir( self._path + "/images" )

        config = {}
        config["image_resize"] = self.image_resize

        with open(self._path + "/config.json", 'w') as f:
            json.dump(config, f)


    def set_video_label(self, source, label):
        """
        在当前目录下生成一个以 video2image.name 命名的文件夹,如./sig,文件夹结构如下：
        ./
            sig/
                config.json     # config文件中存储一些配置信息，如当前的image_resize值，label文本（按set_video_label执行顺序确定0、1、2....）
                images/
                    null_2020-5-12-10-10-10-0.png   # 考虑同一个标签多个视频文件，因此最终图片的命名规则为:  label_时间日期戳_序号.png
                    null_2020-5-12-10-10-10-1.png
                    .............................
        """
        if not os.path.exists(source):
            print("[video2image.set_video_label] file does not exist")
            return

        config = {}
        has_label = False
        if os.path.exists(self._path + "/config.json"):
            with open(self._path + "/config.json", 'r') as f:
               config = json.load(f)
            for index in range(self.video_index, -1, -1):
                key = "label_" + str(index)
                if key in config:
                    if label == config[key]:
                        has_label = True
                        break
        else:
            config["image_resize"] = self.image_resize
        
        if not has_label:
            self.video_index += 1
            config["label_" + str(self.video_index)] = label

        config["video_index"] = self.video_index

        with open(self._path + "/config.json", 'w') as f:
            json.dump(config, f)

        cap = cv2.VideoCapture( source )
        frame_count = int(cap.get(7))

        now = datetime.datetime.now()
        timestamp = now.strftime("_%Y-%m-%d-%H-%M-%S_")
        temp_path = self.path() + "/images/" + label + timestamp
        for c in range(frame_count):
            ret,frame = cap.read()
            save_path = temp_path + str(c) + ".jpg"
            cv2.imencode('.jpg', frame)[1].tofile(save_path)
            img = Image.open(save_path)

            ratio = (img.size[0] * self.image_resize[1]) / (img.size[1] * self.image_resize[0])
            if ratio > 1:
                # 裁切x轴
                crop_len = int( (img.size[0] - (self.image_resize[0] * img.size[1] / self.image_resize[1]) ) / 2 )
                img = img.crop((crop_len, 0, img.size[0] - crop_len, img.size[1]))
            elif ratio < 1:
                # 裁切y轴
                crop_len = int( (img.size[1] - (self.image_resize[1] * img.size[0] / self.image_resize[0]) ) / 2 )
                img = img.crop((0, crop_len, img.size[0], img.size[1] - crop_len))
           
            img = img.resize( self.image_resize, Image.ANTIALIAS)
            img.save(save_path)
            print( "\r"+"progress label:[{}] {}/{}".format(label, c+1, frame_count), end="" ,flush=True)
        print("")

        
    def labels(self):
        """
        通过config获取标签文本列表
        """
        if os.path.exists(self._path + "/config.json"):
            with open(self._path + "/config.json", 'r') as f:
                config = json.load(f)
                _labels = []
                for index in range(self.video_index + 1):
                    key = "label_" + str(index)
                    if key in config: _labels.append(config[key])
                return _labels
        else:
            return []
        
    def path(self):
        """
        获取之前生成的文件夹绝对路径
        """
        return os.path.abspath(self._path)
        
    def data(self, shuffle=True):
        """
        将images文件夹下的图片读取为ndarray格式，最终返回一个元组(x,y),x、y都是ndarray
        shuffle参数默认为True，即需要打乱顺序
        """
        config = None
        with open(self._path + "/config.json", 'r') as f:
            config = json.load(f)
        
        if config is None: return None, None

        _dict = {}
        for index in range(self.video_index + 1):
            key = "label_" + str(index)
            if key in config: _dict[config[key]] = index

        imglist = []
        labellist = []
        for imgpath in os.listdir(self._path + "/images"):
            img = skio.imread(os.path.join(self._path, "images", imgpath))
            imglist.append(img)
            _label = imgpath.split("_")[0]
            if _label in _dict: labellist.append(_dict[_label])

        x_data = np.array(imglist)
        y_data = np.array(pd.get_dummies(np.array(labellist)))
        x_data = x_data/255

        if shuffle:
            indices = np.arange(x_data.shape[0])
            np.random.shuffle(indices)
            x_data = x_data[indices]
            y_data = y_data[indices]

        return x_data, y_data


class npu_predict():

    def unzip_single(self, src_file, dest_dir, password):
        """
        解压单个文件到目标文件夹。
        """
        if password:
            password = password.encode()
        zf = zipfile.ZipFile(src_file)
        try:
            zf.extractall(path=dest_dir, pwd=password)
        except RuntimeError as e:
            print(e)
        zf.close()

    def unzip_all(self, source_dir, dest_dir, password):
        if not os.path.isdir(source_dir):    # 如果是单一文件
            self.unzip_single(source_dir, dest_dir, password)
        else:
            it = os.scandir(source_dir)
            for entry in it:
                if entry.is_file() and os.path.splitext(entry.name)[1]=='.zip' :
                    self.unzip_single(entry.path, dest_dir, password)

    def my_callback(self, monitor):
        # print(monitor)
        if self.finished_uploading: return
        progress = (monitor.bytes_read * 100) / self.zip_size
        print("\r上传进度：{:.2f} %".format(progress), end="")
        if progress >= 100:
            self.finished_uploading = True
            print("")
            print("等待远程服务器转换模型 ...")

    def get_file_md5(self, fname):
        m = hashlib.md5()   #创建md5对象
        with open(fname, 'rb') as fobj:
            while True:
                data = fobj.read(4096)
                if not data:
                    break
                m.update(data)  #更新md5对象
        return m.hexdigest()    #返回md5对象

    def __init__(self, h5_path, image_path=None):
        """
        传入h5文件和一张图片，完成模型转换
        模型转换完成后，在当前目录下生成一个文件夹：npu_[modelname],把二进制文件保存到该文件夹下，具体结构如下：
        ./
            modelname_npu/  #其中modelname通过传入h5_path的文件名确定
                test_image.jpg
                config.json #保存模型输入尺寸信息
                xxxxxx      #转换好的模型以及可执行程序文件等
        """
        self.h5_path = h5_path
        self.image_path = image_path

        modelname,_ = os.path.splitext(os.path.basename(h5_path))
        self.model_name = modelname
        npu_path = modelname + "_npu"
        self.npu_path = npu_path
        self.npu_abspath = os.path.abspath(npu_path)

        h5_md5 = self.get_file_md5(h5_path)

        if os.path.exists(npu_path):
            if os.path.exists(npu_path + "/config.json"):
                with open(npu_path + "/config.json", 'r') as f:
                    try:
                        config = json.load(f)
                        if "h5_md5" in config.keys() and config["h5_md5"] == h5_md5:
                            self.image_size = config["image_size"]
                            self.date_time = config["date_time"]
                            if os.path.exists(npu_path + "/model_{}".format(self.date_time)) and os.path.exists(npu_path + "/model_{}.nb".format(self.date_time)):
                                print('此H5文件已被转换过，现在调用前一次的转换结果 ...')
                                return
                    except:
                        pass
        else:
            os.mkdir( npu_path )
               
        if not os.path.exists(image_path):
            return

        img = Image.open(image_path)
        
        dateTime = int(time.time())
        self.date_time = dateTime

        config = {}
        config["image_size"] = img.size
        config["h5_md5"] = h5_md5
        config["date_time"] = str(dateTime)
        self.image_size = img.size
        # print(self.image_size)

        with open( npu_path + "/config.json", 'w') as f:
            json.dump(config, f)

        os.system('cp {} {}'.format(image_path, npu_path + "/test_image.jpg"))

        url = 'http://cfz.labplus.cn:8089/api/uploadConvertModel'

        z = zipfile.ZipFile('model.zip', 'w', zipfile.ZIP_DEFLATED)
        z.write(h5_path, arcname='model.h5')
        z.write(image_path, arcname='0_0.jpg')
        z.close()

        self.zip_size = os.path.getsize('model.zip')


        e = encoder.MultipartEncoder(
            fields={
                "model_name": 'model',
                "dateTime": str(dateTime),
                "file": ("model.zip", open( "model.zip", "rb"))
            }
        )

        self.finished_uploading = False
        m = encoder.MultipartEncoderMonitor(e, self.my_callback)

        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"]
        headers['Content-Type'] = m.content_type
        headers['User-Agent'] = random.choice(user_agent_list)
        # response = requests.post(url, data, files=files, timeout=50, headers=headers)
        response = requests.post(url, data=m, headers=headers)

        length = int(response.headers['content-length'])
        print("已接收 {} 字节".format(length))
        
        # response.encoding = "utf-8"
        with open(npu_path + '/{}.zip'.format(modelname), "wb") as f:
            for bl in response.iter_content(chunk_size=1024):
                if bl:
                    f.write(bl)
        #print(response.text)

        # 判断源路径是否合法
        if not os.path.exists(npu_path):
            print("压缩文件或压缩文件所在路径不存在！")
            exit()
        if not os.path.isdir(npu_path) and not zipfile.is_zipfile(npu_path):
            print("指定的源文件不是一个合法的.zip文件！")
            exit()
    
        # 如果解压到的路径不存在，则创建     
        if not os.path.exists(npu_path):
            os.mkdir(npu_path)

        self.unzip_all(npu_path, npu_path, '')
        
        os.system('chmod +x {}/model_{}'.format(self.npu_abspath, self.date_time))
        # time.sleep(1)
        print('转换成功!')
        # print("__init__ npu_predict")

    def predict(self, frame):
        """
        执行二进制文件进行前向预测。传入的是frame，即ndarray格式
        ->[0.534,0.323,0.143}]
        对于传入的frame，需要先根据模型输出尺寸进行resize，然后进行前向预测，最后输出向量即可
        """
        # print("Basic_CNN.predict")
        img = Image.fromarray(np.uint8(frame*255))
        img = img.resize( self.image_size, Image.ANTIALIAS)
        img.save( '/ramdisk/ndarray.jpg' )

        command = '{}/./model_{} "{}/model_{}.nb" /ramdisk/ndarray.jpg'.format(self.npu_abspath, self.date_time, self.npu_abspath, self.date_time)
        # print(command)
        
        res = subprocess.getoutput(command)
        # print(res)
        
        res = re.findall(r"Result: \[([\d\.\s]+) \]", res)
        if len(res) > 0:
            res = res[0].split(' ')
            for i in range(len(res)):
                res[i] = float(res[i])
        return res
