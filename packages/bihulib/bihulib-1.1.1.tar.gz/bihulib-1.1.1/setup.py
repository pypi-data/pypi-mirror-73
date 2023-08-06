from setuptools import setup, find_packages
setup(
    name='bihulib',  # 包名称
    version='v1.1.1',  # 包版本
    description='bihu.com lib',  # 包详细描述
    long_description='Bihu Lib | by QQQQQ',   # 长描述，通常是readme，打包到PiPy需要
    author='QQQQQ',  # 作者名称
    author_email='15166054530@163.com',  # 作者邮箱
    url='https://bihu.com/people/1052858039',   # 项目官网
    packages=['bihulib'],    # 项目需要的包
    data_files=[],   # 打包时需要打包的数据文件，如图片，配置文件等
    include_package_data=True,  # 是否需要导入静态数据文件
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=['requests>=2.23.0'],  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[    # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)