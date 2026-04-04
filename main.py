import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

from agent import decide_action
from sim import ArmSimulator


def extract_objects_and_detections(results, model):
    """
    从 YOLO 结果中提取:
    1. objects: 类别名列表
    2. detections: DeepSORT 需要的检测框格式
    """
    objects = []
    detections = []

    if len(results) == 0:
        return objects, detections

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        name = model.names[cls_id]

        objects.append(name)
        detections.append((
            [x1, y1, x2 - x1, y2 - y1],
            conf,
            name
        ))

    return objects, detections


def draw_tracks(frame, tracks):
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()

        l, t, r, b = int(l), int(t), int(r), int(b)
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"ID {track_id}",
            (l, max(0, t - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    return frame


def draw_action(frame, action):
    cv2.putText(
        frame,
        f"Action: {action}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 255),
        2
    )
    return frame


def main():
    video_path = "data/test_bottle.mp4"
    output_path = "data/output_machine.mp4"

    model = YOLO("yolov8n.pt")
    tracker = DeepSort(max_age=30)
    sim = ArmSimulator(gui=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        sim.close()
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    prev_raw_action = None
    stable_action = "idle"
    same_action_count = 0

    frame_idx = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1

            # 1. 检测
            results = model(frame, verbose=False)

            # 2. 提取类别和检测框
            objects, detections = extract_objects_and_detections(results, model)

            # 3. 跟踪
            tracks = tracker.update_tracks(detections, frame=frame)

            # 4. 决策
            raw_action = decide_action(objects)

            # 做一个“稳定器”，避免每一帧都触发机械臂
            if raw_action == prev_raw_action:
                same_action_count += 1
            else:
                same_action_count = 1
                prev_raw_action = raw_action

            # 连续 10 帧同一动作，才真正执行一次
            if same_action_count >= 10 and raw_action != stable_action:
                stable_action = raw_action
                sim.execute_action(stable_action)

            # 5. 绘制结果
            annotated = results[0].plot()
            annotated = draw_tracks(annotated, tracks)
            annotated = draw_action(annotated, stable_action)

            cv2.imshow("Day6 Pipeline", annotated)
            writer.write(annotated)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

    finally:
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        sim.close()

    print(f"Saved video to: {output_path}")


if __name__ == "__main__":
    main()