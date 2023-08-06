# [GreenLab] - Libraries 

## 1. Description

This library is built for specific tasks

* **Face Recognition Project**
  * Face Detection
  * Extract Face Embedding
  * Search Face in database
* **License Plate Recognition Project**

**Documentation**: 

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
* Keras

### 3.2 Installation

Make sure `conda` is installed.

**Note that**: If you are using GPU, you need to change the version of cuda in `requirements.txt` file.

*`mxnet-cu101`* means the package is built with CUDA/cuDNN and the CUDA version is 10.1.

```
# create environment 
conda create --name face_recog_test python=3.6
conda activate face_recog_test

# install dependencies for cpu 
pip install -r requirements-cpu.txt
# or install dependencies for gpu 
pip install -r requirements-gpu.txt

# install face recognition library
pip install --upgrade green-face-recognition
```

## 4. Usage

Prepare the config file as `yaml` type. Take a look [this example](https://github.com/leviethung2103/face-recognition-baseline/blob/master/configs/server_api.yaml).

**Show the list of models**

```python
from face_recognition import models
models.show_avai_models()
```

**Load the models**

```python
retina_model = models.build_model('retina-r50',config_path)
arcface = models.build_model('arc-face',config_path)
```

**Make the prediction**

```python
# get faces and landmarks
retina_model.detect_fast(img,img.shape,0.8,[1],do_flip=False)
```

## 5. Examples

[Face Recognition - Getting Started](https://github.com/leviethung2103/face-recognition-baseline)

## 6. APIs

## 7. References

[1. RetinaFaceModel](https://github.com/deepinsight/insightface/tree/master/RetinaFace)

## Maintainers

**Author:** Hung Le Viet

**Last Update:** July 14, 2020

## Updates

* `[Jul 9]` Initial version
* `[Jul 13]` Make the models can run on GPU/CPU. Integrated `rcnn` library. 