#coding: utf-8
from PIL import Image
import os
import sys
import json
from datetime import datetime
from ImageProcess import Graphics

# 定義壓縮比，數值越大，壓縮越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0


def make_directory(directory):
    """創建目錄"""
    os.makedirs(directory)

def directory_exists(directory):
    """判斷目錄是否存在"""
    if os.path.exists(directory):
        return True
    else:
        return False

def list_img_file(directory):
    """列出目錄下所有檔，並篩選出圖片檔清單返回"""
    old_list = os.listdir(directory)
    # print old_list
    new_list = []
    for filename in old_list:
        name, fileformat = filename.split(".")
        if fileformat.lower() == "jpg" or fileformat.lower() == "png" or fileformat.lower() == "gif":
            new_list.append(filename)
    # print new_list
    return new_list


def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)

def compress(choose, des_dir, src_dir, file_list):
    """壓縮演算法，img.thumbnail對圖片進行壓縮，
    
    參數
    -----------
    choose: str
            選擇壓縮的比例，有4個選項，越大壓縮後的圖片越小
    """
    if choose == '1':
        scale = SIZE_normal
    if choose == '2':
        scale = SIZE_small
    if choose == '3':
        scale = SIZE_more_small
    if choose == '4':
        scale = SIZE_more_small_small
    for infile in file_list:
        img = Image.open(src_dir+infile)
        # size_of_file = os.path.getsize(infile)
        w, h = img.size
        img.thumbnail((int(w/scale), int(h/scale)))
        img.save(des_dir + infile)
def compress_photo():
    '''調用壓縮圖片的函數
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list_src = list_img_file(src_dir)
    if directory_exists(des_dir):
        if not directory_exists(des_dir):
            make_directory(des_dir)
        file_list_des = list_img_file(des_dir)
        # print file_list
    '''如果已經壓縮了，就不再壓縮'''
    for i in range(len(file_list_des)):
        if file_list_des[i] in file_list_src:
            file_list_src.remove(file_list_des[i])
    if len(file_list_src) == 0:
        print("=====沒有新檔需要壓縮=======")
    compress('4', des_dir, src_dir, file_list_src)

def handle_photo():
    '''根據圖片的檔案名處理成需要的json格式的資料
    
    -----------
    最後將data.json文件存到博客的source/photos資料夾下
    '''
    src_dir, des_dir = "photos/", "min_photos/"
    file_list = list_img_file(src_dir)
    list_info = []
    file_list.sort(key=lambda x: x.split('_')[0])   # 按照日期排序
    for i in range(len(file_list)):
        filename = file_list[i]
        date_str, info = filename.split("_")
        info, _ = info.split(".")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]            
        if i == 0:  # 處理第一個文件
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                                   'month': date.month,
                                                                   'link': [filename],
                                                                   'text': [info],
                                                                   'type': ['image']
                                                                   }
                                        } 
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # 不是最後的一個日期，就新建一個dict
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                   'month': date.month,
                                                   'link': [filename],
                                                   'text': [info],
                                                   'type': ['image']
                                                   }
                        }
            list_info.append(new_dict)
        else:  # 同一個日期
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')
    list_info.reverse()  # 翻轉
    final_dict = {"list": list_info}
    with open("E:\htdocs\www\git\hexo\blog\source\photos\data.json","w") as fp:
        json.dump(final_dict, fp)

def cut_photo():
    """裁剪演算法
    
    ----------
    調用Graphics類中的裁剪演算法，將src_dir目錄下的檔進行裁剪（裁剪成正方形）
    """
    src_dir = "photos/"
    if directory_exists(src_dir):
        if not directory_exists(src_dir):
            make_directory(src_dir)
        # business logic
        file_list = list_img_file(src_dir)
        # print file_list
        if file_list:
            print_help()
            for infile in file_list:
                img = Image.open(src_dir+infile)
                Graphics(infile=src_dir+infile, outfile=src_dir + infile).cut_by_ratio()            
        else:
            pass
    else:
        print("source directory not exist!")     



def git_operation():
    '''
    git 命令列函數，將倉庫提交
    
    ----------
    需要安裝git命令列工具，並且添加到環境變數中
    '''
    os.system('git add --all')
    os.system('git commit -m "add photos"')
    os.system('git push origin master')

if __name__ == "__main__":
    cut_photo()        # 裁剪圖片，裁剪成正方形，去中間部分
    compress_photo()   # 壓縮圖片，並保存到mini_photos資料夾下
    git_operation()    # 提交到github倉庫
    handle_photo()     # 將檔處理成json格式，存到博客倉庫中
    
    
    
    
