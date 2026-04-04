# Mini Embodied Agent - A Learning Project

&gt; 一个用于学习具身智能基础的最小化实践项目。通过7天的动手实验，探索从视觉感知到动作执行的完整pipeline。

## 项目概述

这个项目源于对具身智能（Embodied AI）的好奇心。我希望通过从零搭建一个简单的**Vision-Action Pipeline**，理解机器人如何从"看见"到"行动"的基本流程。

项目实现了最简化的四步闭环：
1. **感知**：使用YOLOv8进行物体检测，DeepSORT完成多目标跟踪
2. **决策**：基于规则的简单决策器（如检测到bottle则触发pick动作）
3. **执行**：在PyBullet仿真环境中控制KUKA iiwa机械臂完成基础动作
4. **验证**：通过仿真观察动作执行效果

## 项目结构
mini-embodied-agent/
├── detect.py          # Day 1-2: YOLOv8 detection
├── track.py           # Day 2: DeepSORT tracking  
├── agent.py           # Day 3: Rule-based decision
├── sim.py             # Day 4-5: PyBullet simulation
├── main.py            # Day 6: Integrated pipeline
├── pointcloud_demo.py # Day 2: Open3D basics (optional but recommended)
├── assets/
│   └── demo.mp4       # Day 7: Screen recording
└── README.md

## 技术实现

### Day 1-2: 视觉感知模块
- 使用YOLOv8n（轻量级模型）实现实时物体检测
- 集成DeepSORT实现跨帧目标关联，为每个目标分配唯一ID
- 针对CPU环境优化，使用半精度推理和分辨率调整

### Day 3: 决策逻辑
```python
# 最简单的Agent决策逻辑，理解VLA架构的基础形式
def decide_action(objects):
    if "bottle" in objects:
        return "pick_bottle"
    elif "cup" in objects:
        return "move_cup"
    return "idle"

### Day 4-5: 仿真执行

- 使用PyBullet搭建仿真环境
- 加载KUKA iiwa 7自由度机械臂模型
- 实现基础的关节位置控制，完成简单抓取动作

## Day 6: 系统集成

将上述模块串联，实现：
视频流 → YOLO检测 → DeepSORT跟踪 → 规则决策 → PyBullet执行


## Day 7: Open3D基础（延伸学习）

- 点云数据的读取与可视化
- 基础下采样和去噪处理
- 理解3D感知在机器人操作中的作用

## 实验环境

- **硬件**：Intel 18核CPU, 32GB内存（无GPU）
- **软件**：Python 3.9, PyTorch (CPU), OpenCV, PyBullet, Open3D

## 运行方式

```bash
# 安装依赖
pip install ultralytics opencv-python torch torchvision
pip install deep-sort-realtime pybullet open3d

# 运行完整pipeline
python main.py --input video.mp4

# 单独运行各模块
python detect.py --source test.jpg    # 检测
python track.py --source test.mp4     # 跟踪
python sim.py --action pick_bottle    # 仿真

关键学习收获
工程实践：理解了如何将深度学习模型（YOLO）与传统跟踪算法（DeepSORT）结合
系统思维：体验了感知-决策-执行闭环的延迟和耦合问题
仿真基础：掌握了PyBullet的基本使用，理解物理仿真在机器人开发中的重要性
性能优化：在无GPU环境下，通过降低分辨率和批处理优化推理速度
局限性与未来探索
当前局限：
决策模块使用简单规则，未引入LLM/VLM
仅支持仿真环境，未接入真实机械臂
3D感知部分仅完成基础点云处理，未实现完整的三维重建
下一步想探索的：
尝试将决策模块升级为轻量级VLM（如LLaVA）接入
深入学习3D视觉，尝试用Open3D实现简单的物体位姿估计
了解Sim-to-Real的基本方法，为后续接触真实机器人做准备
参考资料
YOLOv8官方文档
PyBullet Quickstart Guide
DeepSORT原始论文与实现
Open3D官方Tutorial
---
声明：这是一个本科阶段的学习练习项目，旨在通过动手实践理解具身智能的基础流程。代码以可读性和教学性为主，未进行生产级优化。
