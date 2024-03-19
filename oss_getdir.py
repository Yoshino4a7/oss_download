import subprocess
import sys
import oss2
import os
import re
import copy
#登录信息
endpoint = ''
accesskey_id = ""
accesskey_secret = ""
bucket_name = ""
DNA_list = []
RNA_list= []
# 本地文件保存路径前缀
download_local_save_prefix = ""
root_dir_list = []
'''
列举prefix全部文件
'''


def prefix_all_list(bucket):
    # print("开始列举" + prefix + "全部文件")
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket):


        # print(' key : ' + obj.key)
        if str(obj.key).endswith('/'):
            print("D " +obj.key)

        else:
            # print("F: "+obj.key)
            download_to_local(bucket, obj.key)

def prefix_all_list_md5(bucket):
    # print("开始列举" + prefix + "全部文件")
    oss_file_size = 0


    for obj in oss2.ObjectIterator(bucket):
        key = obj.key
        # print(key)


        if key.count("00.mergeRawFq/D")>=1:
            prefix = key[:key.index("00.merge")]
            if (prefix in DNA_list) == False:
                DNA_list.append(prefix)
            continue
        elif key.count("00.mergeRawFq/R")>=1:
            prefix = key[:key.index("00.merge")]
            if (prefix in RNA_list) ==False:
                RNA_list.append(prefix)
            continue

    all_list_md5_dna(bucket)

    all_list_md5_rna(bucket)







    # print(prefix + " file size " + str(oss_file_size))

# def all_list_md5_rna(bucket):
#     iter_complete = False
#     for obj in oss2.ObjectIterator(bucket):
#         key = obj.key
#
#         if key.count("/") >= 2:
#             try:
#                 if key.endswith("MD5.txt"):
#                     prefix = key[:key.index("MD5.txt")]
#                     if prefix in RNA_list:
#                         # print("F: " + obj.key)
#                         download_to_local(bucket, obj.key, 1)
#                         continue
#                 prefix = key[:key.index("00.merge")]
#             except ValueError:
#                 continue
#         else:
#             continue
#         if key.endswith('/') and prefix in RNA_list:
#
#             str1 = os.path.join(download_local_save_prefix, "RNA")
#             str2 = str1.replace("\\", "/")
#             dir = os.path.join(str2, key)
#             dir = dir.replace("\\", "/")
#             # print(dir)
#             if not os.path.exists(dir):
#                 os.makedirs(dir)
#                 continue
#         if iter_complete == False:
#             for rna_dir in RNA_list:
#                 list = [download_local_save_prefix, "RNA", rna_dir]
#                 root_dir = "/".join(list)
#                 subprocess.Popen(["D:\\Git\\git-bash.exe", "-c", f"python file_check.py -d {root_dir} ; bash"])
#             iter_complete = True
#         else:
#             continue
#     # print(RNA_list)
#         if  prefix in RNA_list:
#             download_to_local(bucket, obj.key, 1)

def all_list_md5_dna(bucket):
    iter_complete = False
    for dna_dir in DNA_list:
        prefix = dna_dir
        list = [download_local_save_prefix,"DNA",prefix]
        dir = "/".join(list)
        if not os.path.exists(dir):
            os.makedirs(dir)
        key = os.path.join(prefix, "MD5.txt")
        key = key.replace("\\","/")
        download_to_local(bucket, key, 0)
        root_dir = "/".join(list)
        #print(root_dir)
        subprocess.Popen(["D:\\Git\\git-bash.exe", "-c", f"python file_check.py -d {root_dir} ; bash"])
    for obj in oss2.ObjectIterator(bucket):
        key = obj.key
        # print(key)
        if key.count("/") >= 2:
            try:
                # if key.endswith("MD5.txt"):
                #     prefix = key[:key.index("MD5.txt")]
                #     if prefix in DNA_list:
                #         # print("F: " + obj.key)
                #         download_to_local(bucket, obj.key, 0)
                #         continue
                prefix = key[:key.index("00.merge")]

            except ValueError:
                continue

        else:
            continue
        if key.endswith("/") and prefix in DNA_list:


                str1 = os.path.join(download_local_save_prefix,"DNA")
                str2 = str1.replace("\\", "/")
                dir = os.path.join(str2,key)
                dir = dir.replace("\\","/")
                #print(dir)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                    continue


        if (prefix in DNA_list) and key.endswith("/")==False:
            download_to_local(bucket, obj.key, 0)
def all_list_md5_rna(bucket):
    iter_complete = False
    for rna_dir in RNA_list:
        prefix = rna_dir
        list = [download_local_save_prefix, "RNA", prefix]
        dir = "/".join(list)
        if not os.path.exists(dir):
            os.makedirs(dir)
        key = os.path.join(prefix, "MD5.txt")
        key = key.replace("\\","/")
        download_to_local(bucket, key, 1)
        root_dir = "/".join(list)
        subprocess.Popen(["D:\\Git\\git-bash.exe", "-c", f"python file_check.py -d {root_dir} ; bash"])
    for obj in oss2.ObjectIterator(bucket):
        key = obj.key
        # print(key)
        if key.count("/") >= 2:
            try:
                # if key.endswith("MD5.txt"):
                #     prefix = key[:key.index("MD5.txt")]
                #     if (prefix in RNA_list):
                #         # print("F: " + obj.key)
                #         download_to_local(bucket, obj.key, 1)
                #         continue
                prefix = key[:key.index("00.merge")]

            except ValueError:
                continue

        else:
            continue
        if key.endswith("/") and prefix in RNA_list:
                str1 = os.path.join(download_local_save_prefix,"RNA")
                str2 = str1.replace("\\", "/")
                dir = os.path.join(str2,key)
                dir = dir.replace("\\","/")
                #print(dir)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                    continue



        if (prefix in RNA_list) and key.endswith("/")==False:
            download_to_local(bucket, obj.key, 1)



'''
列举全部的根目录文件夹、文件
'''


def root_directory_list(bucket):
    # 设置Delimiter参数为正斜线（/）。
    num = 0
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        # 通过is_prefix方法判断obj是否为文件夹。
        if obj.is_prefix():  # 文件夹
            global root_dir
            root_dir= f"{download_local_save_prefix}/{obj.key}"
            # print(root_dir)
            # print(root_dir)
            # print('directory: ' + obj.key)
            # print(str(obj.key).strip("/"))
            prefix_all_list(bucket, str(obj.key).strip("/")) # 去除/
        else:  # 文件
            # print('file: ' + obj.key)
            # 下载根目录的单个文件
            download_to_local(bucket, str(obj.key))
            num += 1
            print(num)
def root_directory_list_md5(bucket):
    # 设置Delimiter参数为正斜线（/）。
    num = 0
    try:
        for obj in oss2.ObjectIterator(bucket, delimiter='/'):
            # 通过is_prefix方法判断obj是否为文件夹。
            if obj.is_prefix():  # 文件夹
                global root_dir_DNA
                global root_dir_RNA
                #root_dir = f"{download_local_save_prefix}/{obj.key}"
                prefix_all_list_md5(bucket)
            # else:  # 文件
            #     # print('file: ' + obj.key)
            #     # 下载根目录的单个文件
            #     download_to_local(bucket,obj.key)
            #     num += 1
            #     # print(num)
    except:
        return 0
    return 1


'''
下载文件到本地
'''



def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        # rate表示下载进度。
        print('\r{0}% '.format(rate), end='')

        sys.stdout.flush()
def download_to_local(bucket, object_name,option):
    url = download_local_save_prefix
    # print(object_name)
    # 文件名称
    # file_name = url[url.rindex("/") + 1:]

    # file_path_prefix = url.replace(file_name, "")
    # if False == os.path.exists(object_name):
    #     os.makedirs(file_path_prefix)
    #     print("directory don't not makedirs " + file_path_prefix)

    # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
    if option == 1:
        list = [download_local_save_prefix,"RNA", object_name]
        down_dir = "/".join(list)
        dir = down_dir.replace("\\", "/")
        

        if not os.path.exists(dir):
            print(dir)
            oss2.resumable_download(bucket,object_name, dir, progress_callback=percentage)
            print("")
    else:
        list = [download_local_save_prefix,"DNA", object_name]
        down_dir = "/".join(list)
        dir = down_dir.replace("\\", "/")

        if not os.path.exists(dir):
            print(dir)
            oss2.resumable_download(bucket,object_name, dir, progress_callback=percentage)
            print("")





if __name__ == '__main__':
    command_list = ["-d", "-ak", "-as", "-ep", "-b"]



    # 本地文件保存路径前缀
    # download_local_save_prefix = "D:/EXAMPLEEEEEEE"
    if "-d" in sys.argv:
        try:
            j = sys.argv.index("-d")
            download_local_save_prefix = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-b" in sys.argv:
        try:
            j = sys.argv.index("-b")
            bucket_name = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-ak" in sys.argv:
        try:
            j = sys.argv.index("-ak")
            accesskey_id = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-as" in sys.argv:
        try:
            j = sys.argv.index("-as")
            accesskey_secret = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass

    if "-ep" in sys.argv:
        try:
            j = sys.argv.index("-ep")
            endpoint = sys.argv[j + 1]
        except IndexError:
            pass
    else:
        pass







    print("start \n")
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(accesskey_id, accesskey_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # 单个文件夹下载
    #prefix_all_list(bucket, "20201223")
    try:
        os.mkdir(download_local_save_prefix)
    except FileExistsError:
        pass
    try:
        os.mkdir(download_local_save_prefix+"/DNA/")
    except FileExistsError:
        pass
    try:
        os.mkdir(download_local_save_prefix+"/DNA/rawdata")
    except FileExistsError:
        pass
    try:
        os.mkdir(download_local_save_prefix+"/RNA/")
    except FileExistsError:
        pass
    try:
        os.mkdir(download_local_save_prefix+"/RNA/rawdata")
    except FileExistsError:
        pass
    result = 0
    while result == 0:
        try:
            result = root_directory_list_md5(bucket)
        except Exception as e:
            print(e)
            continue
    # dna_data_dir_list = os.listdir(root_dir_DNA)
    # rna_data_dir_list = os.listdir(root_dir_RNA)
    # print(data_dir_list)
    # for dir in data_dir_list:
    #     print(f"python file_check.py -d {root_dir}{dir}")

    #root_directory_list(bucket)

    # print(root_dir)


    print("end \n")