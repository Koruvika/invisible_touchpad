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
