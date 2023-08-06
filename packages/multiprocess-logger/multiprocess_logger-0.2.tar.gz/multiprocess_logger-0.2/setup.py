from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='multiprocess_logger',
      version='0.2',
      description='一个安全可靠高效的进程间日志处理器  A safe, reliable and efficient inter process log processor',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitee.com',
      author='liuyancong',
      author_email='lyc456789@163.com',
      license='MIT',
      packages=find_packages(),
      )


setup(
    name="multiprocess_logger", # Replace with your own username
    version="0.2",
    author="liuyancong",
    author_email="lyc456789@163.com",
    description="一个安全可靠高效的进程间日志处理器  A safe, reliable and efficient inter process log processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
