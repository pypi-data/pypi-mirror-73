from distutils.core import setup

setup(
    name='baizhannimeimath',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author='huliang',  # 作者
    author_email='huliang@163.com',
    py_modules=['baizhannimeimath.demo01', 'baizhannimeimath.demo02']  # 要发布的模块
)