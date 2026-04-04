# sim.py

import time
import pybullet as p
import pybullet_data


class ArmSimulator:
    def __init__(self, gui=True):
        self.client = p.connect(p.GUI if gui else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)

        # 场景
        self.plane = p.loadURDF("plane.urdf")
        self.table = p.loadURDF("table/table.urdf", [0.7, 0.0, -0.65], useFixedBase=True)

        # 放一个目标物体，模拟 bottle
        self.object_id = p.loadURDF("cube_small.urdf", [0.75, 0.0, 0.02])

        # 机械臂
        self.robot = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)

        # 获取可控关节
        self.arm_joints = []
        for j in range(p.getNumJoints(self.robot)):
            info = p.getJointInfo(self.robot, j)
            joint_type = info[2]
            if joint_type in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                self.arm_joints.append(j)

        # 预定义姿态
        self.home_pose = [0.0, 0.4, 0.0, -1.2, 0.0, 1.0, 0.0]
        self.pick_pose = [0.2, 0.8, 0.0, -1.6, 0.0, 1.2, 0.3]
        self.left_pose = [0.8, 0.5, 0.0, -1.2, 0.0, 1.0, 0.0]
        self.right_pose = [-0.8, 0.5, 0.0, -1.2, 0.0, 1.0, 0.0]

        self.reset_to_home()
        self.step(120)

    def reset_to_home(self):
        for i, joint_id in enumerate(self.arm_joints[:len(self.home_pose)]):
            p.resetJointState(self.robot, joint_id, self.home_pose[i])

    def move_joints(self, target_positions, steps=240, sleep=1.0 / 240.0):
        for _ in range(steps):
            for i, joint_id in enumerate(self.arm_joints[:len(target_positions)]):
                p.setJointMotorControl2(
                    bodyUniqueId=self.robot,
                    jointIndex=joint_id,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=target_positions[i],
                    force=500
                )
            p.stepSimulation()
            time.sleep(sleep)

    def step(self, steps=120, sleep=1.0 / 240.0):
        for _ in range(steps):
            p.stepSimulation()
            time.sleep(sleep)

    def execute_action(self, action):
        print(f"[PyBullet] Execute action: {action}")

        if action == "idle":
            self.move_joints(self.home_pose, steps=180)

        elif action == "pick_bottle":
            # 先伸过去，再回来
            self.move_joints(self.pick_pose, steps=240)
            self.step(60)
            self.move_joints(self.home_pose, steps=240)

        elif action == "follow_person":
            # 左右摆动，模拟“朝向人”
            self.move_joints(self.left_pose, steps=180)
            self.move_joints(self.right_pose, steps=180)
            self.move_joints(self.home_pose, steps=180)

        else:
            self.move_joints(self.home_pose, steps=180)

    def close(self):
        p.disconnect()