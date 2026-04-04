import cv2
import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")

from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30, n_init=1)

video_path = "data/test_agent.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: video cannot be opened.")
    raise SystemExit

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 25

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output_demo.mp4", fourcc, fps, (width, height))

def decide_action(objects):
    if "bottle" in objects:
        return "pick_bottle"
    else:
        return "idle"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    detections = []
    objects = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        name = model.names[cls_id]
        objects.append(name)
        detections.append(([x1, y1, x2 - x1, y2 - y1], conf, name))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue
        l, t, r, b = track.to_ltrb()
        track_id = track.track_id
        cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id}", (int(l), int(t) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    action = decide_action(objects)
    cv2.putText(frame, f"Action: {action}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    out.write(frame)
    cv2.imshow("Agent Demo", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print("Program finished.")