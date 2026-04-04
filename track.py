from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

# 1. 加载模型和跟踪器
model = YOLO("yolov8n.pt")
tracker = DeepSort()

# 2. 路径
video_path = "data/test.mp4"
output_video_path = "data/output_track.mp4"

# 3. 打开视频
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"视频打开失败: {video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# 4. 逐帧处理
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 检测
    results = model(frame)

    # 先画出 YOLO 原始检测框
    annotated_frame = frame.copy()
    for r in results:
        annotated_frame = r.plot()

    # 构造 DeepSORT 输入
    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])

        # YOLO类别名
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]

        # DeepSORT 需要的是 [left, top, width, height]
        detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls_name))

    # 更新跟踪器
    tracks = tracker.update_tracks(detections, frame=annotated_frame)

    # 画 ID
    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()

        l, t, r, b = int(l), int(t), int(r), int(b)

        # 画跟踪框
        cv2.rectangle(annotated_frame, (l, t), (r, b), (0, 255, 0), 2)

        # 画ID
        cv2.putText(
            annotated_frame,
            f"ID {track_id}",
            (l, max(t - 10, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # 保存并显示
    writer.write(annotated_frame)
    cv2.imshow("tracking_result", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()

print("跟踪视频已保存到:", output_video_path)