"""

"""

import time
import functools
import logging
import sys
import random
import traceback
import json
import gc

# 导入常用的固定路径(多平台通用)
from kw618._file_path import *

# AES加密使用
import base64
#注：python3 安装 Crypto 是 pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome<br><br>
from Crypto.Cipher import AES
import hashlib

# 个人用于记录报错内容的log装饰器
def log_error(log_directory=f"{FILE_PATH_FOR_ZIRU_CODE}/Log/ttt_log", throw_error=False):
    # 作为装饰器时, 一定要加上(); 否则就不会返回内部的decorate函数了
    # 如果没有传入log的存放目录, 默认使用上述目录
    def decorate(func):
        def record_error(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                module_name = get_this_module_name()
                func_name = func.__name__ # 暂时没利用, 可删
                kprint(module_name=module_name, func_name=func_name)
                tb_txt = traceback.format_exc(limit=5) # limit参数: 表示traceback最多到第几层
                log_file_path = f"{log_directory}/{module_name}_error.log"
                with open(log_file_path, "a", encoding="utf-8") as f:
                    print(f"\n【捕获到异常】\n{tb_txt}\n【异常存储路径】: {log_file_path}\n")
                    log_msg = tb_txt
                    this_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    f.write(f"{this_time}\n{log_msg}\n\n\n")
                # 有时候需要把错误内容抛出, 在更外层捕获 (通过'消费者多线程池'来捕获,让其url进入到error_queue)
                if throw_error:
                    raise Exception(tb_txt)
        return record_error
    return decorate



# python官网的例子
def logged(level, name=None, message=None):
    """
    这是python cookbook 中官方写写的log案例
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.

    可以看到, 如果你想要给装饰器传参, 就需要在decorate外面再嵌套一层函数: 总共3层
    """
    def decorate(func): # 此处一定只有一个func形参
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @functools.wraps(func) # 这里的装饰器可以修改__name__的问题(其实没啥用, 反正写上更好就对了, 管他呢)
        def wrapper(*args, **kwargs):  # 此处的形参一定是(*args, **kwargs), 并且与下面return中传入的参数一致!!
            log.log(level, logmsg)
            return func(*args, **kwargs) # 一定要记得return
        return wrapper  # 返回的函数名称一定和上面定义(warpper)的一致!!
    return decorate

# Example use
# @logged(logging.DEBUG)
# def add(x, y):
#     return x + y
#
# @logged(logging.CRITICAL, 'example')
# def spam():
#     print('Spam!')




def timer(func):
    """装饰器：记录并打印函数耗时"""
    def decorated(*args, **kwargs):
        st = time.time()
        ret = func(*args, **kwargs)
        print('执行时长: {} 秒'.format(time.time() - st))
        return ret
    return decorated



def get_this_module_name():
    "获取本函数所在脚本的模块名称"
    argv_str = sys.argv[-1]
    return argv_str.split("/")[-1][:-3]



def kprint(**kwargs):
    "方便打印出某些变量的值(测试使用); 需要使用关键字传参"
    json_ = json.dumps(kwargs, indent=4, ensure_ascii=False)
    print(json_)



def k_update(dic, key, value):
    "添加一个'k-v'对的同时, 返回这个添加后的dict对象!! (python默认是没有返回值的, 有些时候不方便) [下同]"
    dic[str(key)] = value
    return dic

def k_append(lst, element):
    lst.append(element)
    return lst

def k_extend(lst, lst2):
    lst.extend(lst2)
    return lst


def k_memory(obj, accuracy=False):
    """
        getsizeof函数默认返回bytes(字节/大B)
        return:
            memory_usage, unit

        tips:
            比 df["<col>"].memory_usage(deep=True) 要稍大一丢丢 (但可以认为是相同的)
    """
    # 1. 需要精准计算
    if accuracy:
        # 1. 列表对象
        if type(obj) == list:
            memory_usage_lst = [ sys.getsizeof(e) for e in obj]
            memory_usage = sum(memory_usage_lst)

        # 2. 字典对象
        elif type(obj) == dict:
            memory_usage_lst = [ sys.getsizeof(k)+sys.getsizeof(v) for k, v in d.items()]
            memory_usage = sum(memory_usage_lst)

        # 3. 其他
        else:
            memory_usage = sys.getsizeof(obj)

    # 2. 粗略计算即可
    else:
        memory_usage = sys.getsizeof(obj)

    # 以一种更"human"的方式呈现 '内存大小'
    if memory_usage < 1024:
        return round(memory_usage, 2), "Bytes"
    elif memory_usage < 1024*1024:
        return round(memory_usage/1024, 2), "KB"
    elif memory_usage < 1024*1024*1024:
        return round(memory_usage/1024/1024, 2), "MB"
    elif memory_usage < 1024*1024*1024*1024:
        return round(memory_usage/1024/1024/1024, 2), "GB"

def get_deep_memory(df):
    show_dict = {}
    columns = list(df.columns)
    for col in columns:
        # df[col].memory_usage(deep=True)
        memory_usage_tuple = k_memory(df[col])
        show_dict.update({col:memory_usage_tuple})
    kprint(show_dict=show_dict)
    return show_dict



def get_top(df, field_1, field_2, top_num=5, ascending=True):
    """
        function: 计算"某"个分类的"某"个字段的"前5名"
        params:
            df: 所需df
            field_1: 按它分类
            field_2: 按它排名
            top_num: 取前几名
    """
    # 先对df的 "field_2" 进行排序
    df = df.sort_values(field_2, ascending=ascending)

    # 用于计数的dict
    d = {}
    def foo(row):
        # nonlocal d
        """
            row: 是df中的一行
        """
        _key = row.get(field_1)
        if d.get(_key, 0) == 0:
            d.update({_key : 1})
            return row
        elif d.get(_key) < top_num:
            d.update({_key : d.get(_key) + 1})
            return row

    # 使用apply, 应用上面的函数
    df2 = df.apply(foo, axis=1)
    _ = df2.columns[0]
    df3 = df2.query(f"{_} == {_}")

    output_data(df3, f"top5_{field_2}")

    return df3


def base64_encrypt(data):
    """
    in:
        data: str类型 / bytes类型
    out:
        encrypted_b: bytes类型
    """
    # base64编码
    if type(data) == str:
        encrypted_b = base64.b64encode(data.encode('utf-8'))
    elif type(data) == bytes:
        encrypted_b = base64.b64encode(data)
    print(f"base64加密后的字节码: {encrypted_b}\n")
    return encrypted_b


def base64_decrypt(b):
    """
    in:
        b: bytes类型
    out:
        origin_s: str类型
    """
    # base64解码
    origin_s = base64.b64decode(b).decode("utf-8")
    print(f"base64解密后的'原始字符串': {origin_s}\n")
    return origin_s





class kwEncryption():
    "支持中文的AES加密!!(mode:CBC模式)"

    def __init__(self, key):
        """
        params:
            key: 必须是ascii字符 (不能是中文) (可以不要求16个字符, 因为后续会自动填充)

        function:
            1. 初始化 key值 和 iv值

        notes:
            1. key,iv使用同一个值
            2. key值和iv值必须要16个字节才行, 所以当key小于16位的时候, 使用"!"自动填充
        """
        # key 和 iv 使用同一个值
        key = key.ljust(16,'!')
        self.key = key
        self.iv = key
        self.key_bytes = bytes(key, encoding='utf-8')
        self.iv_bytes = bytes(key, encoding='utf-8')



    # 用于填充16位字节的辅助函数
    # (不太重要, 但必须要有. 其实可以直接写在底层,不需要自己造轮子啊....!!!贼烦)
    def pkcs7padding(self, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文)
        :return:
        """
        bs = AES.block_size  # 16
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        # tips：utf-8编码时，英文占1个byte，而中文占3个byte
        padding_size = length if(bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding) * padding
        return text + padding_text
    def pkcs7unpadding(self, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        try:
            length = len(text)
            unpadding = ord(text[length-1])
            return text[0:length-unpadding]
        except Exception as e:
            pass


    def aes_encode(self, content):
        """
        function: AES加密
        参数:
            content: 待加密的内容(原内容)
        模式: cbc
        填充: pkcs7
        return:
            加密后的内容

        """
        cipher = AES.new(self.key_bytes, AES.MODE_CBC, self.iv_bytes)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        aes_encode_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
        # 重新编码
        result = str(base64.b64encode(aes_encode_bytes), encoding='utf-8')
        return result


    def aes_decode(self, content):
        """
        function: AES解密
        参数:
            content: 加密后的内容
        模式: cbc
        去填充: pkcs7
        return:
            加密前的内容(原内容)
        """
        try:
            cipher = AES.new(self.key_bytes, AES.MODE_CBC, self.iv_bytes)
            # base64解码
            aes_encode_bytes = base64.b64decode(content)
            # 解密
            aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
            # 重新编码
            result = str(aes_decode_bytes, encoding='utf-8')
            # 去除填充内容
            result = self.pkcs7unpadding(result)
        except Exception as e:
            pass
        if result == None:
            return ""
        else:
            return result



# 对中文加密
x = kwEncryption("kw618").aes_encode("萧山")
# 对中文解密
s = kwEncryption("kw618").aes_decode(x)


if __name__ == "__main__":
    m = 33
    n = 99
    kprint(m=m, n=n)








#
