#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_speech',
      version='1.0.0',
      description='Speech operation api.',
      long_description='Speech Recognition,voice2text,text2voice',
      author='Charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['pip3', 'speech', 'python3', 'python', 'Speech Recognition'],
      url='https://www.shinelab.cn',
      packages=['qbc_speech'],
      package_data={'qbc_speech': ['*.wav', '__init__.py', 'qbc_speech.py', 'qbc_speech_unitest.py']},
      license='MIT',
      install_requires=['pyaudio', 'wave', 'requests', 'ybc_config', 'ybc_exception']
     )