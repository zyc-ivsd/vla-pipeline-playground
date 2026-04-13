# Embodied AI Demo: A Minimal Vision-to-Action Pipeline

> 一个面向具身智能入门实践的微型项目：从视频中的目标检测与跟踪出发，生成简单动作指令，并在 PyBullet 中完成机械臂仿真执行。

## 项目简介

这个项目的目标是搭建一条简单的具身智能闭环：

**视频输入 → 目标检测 → 目标跟踪 → 动作决策 → 仿真执行**

项目目前已经完成以下部分：

1. **视觉感知**：使用 YOLOv8 对视频帧中的目标进行检测。
2. **时序关联**：使用 DeepSORT 对目标进行跨帧跟踪，并分配稳定 ID。
3. **动作决策**：根据当前检测到的目标类别，用简单规则生成动作指令。
4. **仿真执行**：在 PyBullet 中加载 KUKA iiwa 机械臂，并执行对应动作。

目前的重点在于验证一条简单的从“看见”到“执行”的基础 pipeline 是否能够顺利跑通，做一个虚拟的小玩具，为后续我自己能够扩展到更复杂的具身智能任务打下工程基础。

---

## 当前系统流程

```text
Input Video
   ↓
YOLOv8 Detection
   ↓
DeepSORT Tracking
   ↓
Rule-Based Decision Module
   ↓
PyBullet Robot Execution
```

---

## 项目结构

```text
embodied-ai-demo/
├── data/
│   ├── test——bottle.mp4
│   └── output_machine.mp4
├── assets/
│   ├── tracking_result.png
│   └── pybullet_gui.png
├── detect.py
├── track.py
├── agent.py
├── sim.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

说明：
- `detect.py`：目标检测相关逻辑
- `track.py`：多目标跟踪相关逻辑
- `agent.py`：规则决策模块
- `sim.py`：PyBullet 仿真与机械臂动作执行
- `main.py`：整合后的完整 pipeline

---

## 核心功能

### 1. 目标检测
- 使用 YOLOv8n 进行视频帧级目标检测
- 输出目标类别、边界框与置信度

### 2. 多目标跟踪
- 使用 DeepSORT 对目标进行跨帧关联
- 为检测结果分配 ID，并在输出视频中进行可视化

### 3. 动作决策
当前版本使用最简单的基于类别的规则决策：

```python
# agent.py

def decide_action(objects):
    if "bottle" in objects:
        return "pick_bottle"
    elif "person" in objects:
        return "follow_person"
    else:
        return "idle"
```

这个代码比较简单，没有涉及深度学习，目的不是追求复杂策略，而是先验证感知结果能否被顺利转化为动作指令。

### 4. 仿真执行
- 使用 PyBullet 构建基础场景
- 加载 KUKA iiwa 机械臂模型
- 根据动作指令执行预定义的机械臂动作

目前实现的动作包括：
- `pick_bottle`
- `idle`

---

## 运行环境

- Python 3.9
- PyTorch
- OpenCV
- YOLOv8 / Ultralytics
- DeepSORT Realtime
- PyBullet
- NumPy

---

## 安装方式

### 1. 创建环境

```bash
conda create -n agent_env python=3.9
conda activate agent_env
```

### 2. 安装依赖

```bash
pip install ultralytics opencv-python torch torchvision
pip install deep-sort-realtime
conda install -c conda-forge pybullet -y
pip install numpy
```

### 3. Windows 兼容说明

在部分 Windows 环境下，可能出现 OpenMP 运行库冲突。调试阶段可在 `main.py` 最顶部加入：

```python
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
```

这只是临时兼容方案，后续可以通过整理环境进一步解决。
---

## 运行方法

### 1. 准备输入视频

将测试视频放在：

```text
data/test.mp4
```

模型简单,当前 demo 更适合使用包含明显 `bottle` 或 `person` 的短视频。

### 2. 运行主程序

```bash
python main.py
```

### 3. 输出结果

程序运行后会：
- 打开 PyBullet GUI 窗口
- 执行对应机械臂动作
- 保存结果视频到：

```text
data/output_machine.mp4
```
---

## 当前成果
这个项目目前已经实现：
- 视频目标检测
- 多目标跟踪与 ID 标注
- 基于规则的动作生成
- PyBullet 机械臂动作执行
- 从视觉输入到动作执行的最小闭环验证

---

## 局限性

当前版本仍然比较基础，主要局限包括：

- 只使用 RGB 视频输入，没有引入深度信息
- 决策模块是规则驱动的，不具备学习能力
- 机械臂动作是预定义脚本，不是真正的抓取规划
- 没有接入真实机器人硬件
- 还没有加入三维场景建模、点云处理或世界模型模块

这些限制也是这个项目后续继续扩展的空间所在。

---

## 项目价值

这个项目的价值不在于复杂度，而在于它把几个原本分散的部分进行了串联：

- 视觉模型输出
- 时序目标关联
- 动作选择
- 仿真执行
仅是为了让我自己了解简单具身智能的一条完整链路,为入坑做准备。

---

## 备注

一个普通大学生以学习和工程实践为主的项目，重点是把小系统跑通、理清模块之间的关系。
