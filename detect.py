from ultralytics import YOLO
import cv2
import os

# 1. 加载模型
model = YOLO("yolov8n.pt")

# 2. 路径
img_path = "data/test.jpg"
video_path = "data/test.mp4"
output_video_path = "data/output_detect.mp4"
output_image_path = "data/output_detect.jpg"

# 3. 先做图片检测
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"图片读取失败: {img_path}")

results = model(img)

for r in results:
    annotated = r.plot()
    cv2.imwrite(output_image_path, annotated)
    cv2.imshow("image_result", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 4. 再做视频检测
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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for r in results:
        frame = r.plot()

    writer.write(frame)
    cv2.imshow("video_result", frame)

    # 按 ESC 退出
    if cv2.waitKey(1) == 27:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()

print("图片检测结果已保存到:", output_image_path)
print("视频检测结果已保存到:", output_video_path)