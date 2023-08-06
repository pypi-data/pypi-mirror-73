# [GreenLab] - Libraries 

## 1. Description

This library is built for specific tasks

* **Face Recognition Project**
  * Face Detection
  * Extract Face Embedding
  * Search Face in database
* **License Plate Recognition Project**

**Documentation**: https://leviethung2103.github.io/

**Pypi Project**: https://pypi.org/project/greenlab-library/

## 2. Table of Contents

* Setup guide
* Usage
* Examples
* APIs
* References

## 3. Setup guide

### 3.1 System requirements

* Python>=3.6
* CUDA==10.0
* MXNet
* Tensorflow
* Keras==2.2.0

### 3.2 Installation

Create a new virtual environment, you can choose `virtualenv` or `anaconda`. 

**Virtualenv** 

```
python3 -m venv venv
source venv/bin/activate
```

**Anaconda**

```
# create environment 
conda create --name face_recog_test python=3.6
conda activate face_recog_test
```

**Install packages and dependencies**

```
# install dependencies for cpu 
pip install -r requirements-cpu.txt
# or install dependencies for gpu 
pip install -r requirements-gpu.txt

# install face recognition library
pip install --upgrade greenlab-library
```

## 4. Usage

### 4.1 Face Recognition Library

**Documentation**: https://leviethung2103.github.io/pkg/face_recognition.html

**Getting started code:** https://github.com/leviethung2103/face-recognition-baseline

```
git clone https://github.com/leviethung2103/face-recognition-baseline
python main.py
```

### 4.2 License Plate Library

**Documentation**: https://leviethung2103.github.io/pkg/license_recog.html

**Getting started code:** https://github.com/leviethung2103/license-plate-baseline


## 5. APIs

## 6. References

[1. RetinaFaceModel](https://github.com/deepinsight/insightface/tree/master/RetinaFace)

## 7. Maintainers

**Author:** Hung Le Viet

**Last Update:** July 14, 2020

## Updates

* `[Jul 9]` Initial version
* `[Jul 13]` Make the models can run on GPU/CPU. Integrated `rcnn` library. 