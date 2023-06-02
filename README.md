# Invisible Touchpad

![GitHub repo size](https://img.shields.io/github/repo-size/cleardusk/3DDFA_V2.svg)
[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OKciI0ETCpWdRjP-VOGpBulDJojYfgWv)

By [Jianzhu Guo](https://guojianzhu.com), [Xiangyu Zhu](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/), [Yang Yang](http://www.cbsr.ia.ac.cn/users/yyang/main.htm), Fan Yang, [Zhen Lei](http://www.cbsr.ia.ac.cn/users/zlei/) and [Stan Z. Li](https://scholar.google.com/citations?user=Y-nyLGIAAAAJ).
The code repo is owned and maintained by **[Jianzhu Guo](https://guojianzhu.com)**.


<p align="center">
  <img src="docs/images/webcam.gif" alt="demo" width="512px">
</p>


**\[Updates\]**
 - `2021.7.10`: Run 3DDFA_V2 online on [Gradio](https://gradio.app/hub/AK391/3DDFA_V2).
 - `2021.1.15`: Borrow the implementation of [Dense-Head-Pose-Estimation](https://github.com/1996scarlet/Dense-Head-Pose-Estimation) for the faster mesh rendering (speedup about 3x, 15ms -> 4ms), see [utils/render_ctypes.py](./utils/render_ctypes.py) for details.
 - `2020.10.7`: Add the latency evaluation of the full pipeline in [latency.py](./latency.py), just run by `python3 latency.py --onnx`, see [Latency](#Latency) evaluation for details.
 - `2020.10.6`: Add onnxruntime support for FaceBoxes to reduce the face detection latency, just append the `--onnx` action to activate it, see [FaceBoxes_ONNX.py](FaceBoxes/FaceBoxes_ONNX.py) for details.
 - `2020.10.2`: **Add onnxruntime support to greatly reduce the 3dmm parameters inference latency**, just append the `--onnx` action when running `demo.py`, see [TDDFA_ONNX.py](./TDDFA_ONNX.py) for details.
 - `2020.9.20`: Add features including pose estimation and serializations to .ply and .obj, see `pose`, `ply`, `obj` options in [demo.py](./demo.py).
 - `2020.9.19`: Add PNCC (Projected Normalized Coordinate Code), uv texture mapping features, see `pncc`, `uv_tex` options in [demo.py](./demo.py).


## Introduction

This work extends [3DDFA](https://github.com/cleardusk/3DDFA), named **3DDFA_V2**, titled [Towards Fast, Accurate and Stable 3D Dense Face Alignment](https://guojianzhu.com/assets/pdfs/3162.pdf), accepted by [ECCV 2020](https://eccv2020.eu/). The supplementary material is [here](https://guojianzhu.com/assets/pdfs/3162-supp.pdf). The [gif](./docs/images/webcam.gif) above shows a webcam demo of the tracking result, in the scenario of my lab. This repo is the official implementation of 3DDFA_V2.

Compared to [3DDFA](https://github.com/cleardusk/3DDFA), 3DDFA_V2 achieves better performance and stability. Besides, 3DDFA_V2 incorporates the fast face detector [FaceBoxes](https://github.com/zisianw/FaceBoxes.PyTorch) instead of Dlib. A simple 3D render written by c++ and cython is also included. This repo supports the onnxruntime, and the latency of regressing 3DMM parameters using the default backbone is about **1.35ms/image on CPU** with a single image as input. If you are interested in this repo, just try it on this **[google colab](https://colab.research.google.com/drive/1OKciI0ETCpWdRjP-VOGpBulDJojYfgWv)**! Welcome for valuable issues, PRs and discussions 😄

<!-- Currently, the pre-trained model, inference code and some utilities are released.  -->

## Getting started

### Requirements
See [requirements.txt](./requirements.txt), tested on macOS and Linux platforms. The Windows users may refer to [FQA](#FQA) for building issues. Note that this repo uses Python3. The major dependencies are PyTorch, numpy, opencv-python and onnxruntime, etc. If you run the demos with `--onnx` flag to do acceleration, you may need to install `libomp` first, i.e., `brew install libomp` on macOS.

### Usage

1. Clone this repo
   
```shell script
git clone https://github.com/cleardusk/3DDFA_V2.git
cd 3DDFA_V2
```

2. Build the cython version of NMS, Sim3DR, and the faster mesh render
<!-- ```shell script
cd FaceBoxes
sh ./build_cpu_nms.sh
cd ..

cd Sim3DR
sh ./build_sim3dr.sh
cd ..

# the faster mesh render
cd utils/asset
gcc -shared -Wall -O3 render.c -o render.so -fPIC
cd ../..
```

or simply build them by -->
```shell script
sh ./build.sh
```

3. Run demos

```shell script
# 1. running on still image, the options include: 2d_sparse, 2d_dense, 3d, depth, pncc, pose, uv_tex, ply, obj
python3 demo.py -f examples/inputs/emma.jpg --onnx # -o [2d_sparse, 2d_dense, 3d, depth, pncc, pose, uv_tex, ply, obj]

# 2. running on videos
python3 demo_video.py -f examples/inputs/videos/214.avi 
