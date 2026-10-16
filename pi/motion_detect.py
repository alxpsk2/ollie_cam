import time
from datetime import datetime
from pathlib import Path

import cv2
from picamera2 import Picamera2

# --- Tunable settings ---
MIN_AREA = 5000  # Minimum area size for motion detection
PIXEL_THRESHOLD = 25  # Pixel intensity difference threshold for motion detection
COOLDOWN_TIME = 10  # Cooldown time in seconds between motion detections
LOOP_DELAY = 0.1  # Delay between each frame capture in seconds

# Your project folder: /home/<user>/picamera/motion-captures
SAVE_DIR = Path.home() / "picamera" / "motion-captures"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(2)  # Allow camera to warm up

prev_gray = None
last_event_time = 0

print(f"Saving captures to: {SAVE_DIR}")
print("Watching for motion... Ctrl+C to stop")

try:
    while True:
        # Picamera2's "RGB888" arrays are BGR-ordered, which is what OpenCV expects
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_gray is None:
            prev_gray = gray
            continue

        delta = cv2.absdiff(prev_gray, gray)
        thresh = cv2.threshold(delta, PIXEL_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest = max((cv2.contourArea(c) for c in contours), default=0)

        now = time.time()
        if largest > MIN_AREA and (now - last_event_time) > COOLDOWN_TIME:
            ts = datetime.now()
            filename = SAVE_DIR / f"motion_{ts.strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(str(filename), frame)
            print(f"[{ts.isoformat()}] Motion! area={largest:.0f} saved={filename}")
            last_event_time = now

        prev_gray = gray
        time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
    print("Stopping.")
finally:
    picam2.stop()
