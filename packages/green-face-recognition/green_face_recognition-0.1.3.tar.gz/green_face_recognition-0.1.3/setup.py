from setuptools import setup
import setuptools

with open('README.md') as f:
    long_description = f.read()

setup(
name='green_face_recognition',
version='0.1.3',
description='HungLV package',
url='https://github.com/leviethung2103/greenlab_ai_utils',
author='Hung LV',
long_description= long_description,
long_description_content_type="text/markdown",
author_email='leviethung1280@gmail.com',
license='MIT',
packages=setuptools.find_packages(),
package_data={'cutils':['Aller_Bd.ttf']},
# packages=['personDect','headPose','personPose','videos','custom_configs','unitest','mtcnn','cutils'],
classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
 ],
 python_requires='>=3.6',
zip_safe=False)
