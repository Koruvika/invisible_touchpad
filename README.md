# Invisible Touchpad

![GitHub repo size](https://img.shields.io/github/repo-size/cleardusk/3DDFA_V2.svg)
[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1OKciI0ETCpWdRjP-VOGpBulDJojYfgWv)


**\[Updates\]**
 - `2023.4.25`: Add GUI to desktop app
 - `2023.4.10`: Add UDP module
 - `2023.3.20`: Change Model & Library in Arduino
 - `2023.2.6`: Init 


## Introduction

Dự án xây dựng thiết bị cho phép điều khiển con trỏ chuột từ xa thông qua cảm biến quán tính và giao thức UDP.

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
