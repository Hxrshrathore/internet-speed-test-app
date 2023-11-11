import tkinter as tk
from tkinter import Canvas
import speedtest
import threading
import time

class InternetSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")

        self.canvas = Canvas(root, width=400, height=200)
        self.canvas.pack()

        self.download_label = tk.Label(root, text="Download Speed: ")
        self.download_label.pack()

        self.upload_label = tk.Label(root, text="Upload Speed: ")
        self.upload_label.pack()

        self.download_rpm_meter = RPMeter(self.canvas, 100, 100, 60, "blue")
        self.upload_rpm_meter = RPMeter(self.canvas, 300, 100, 60, "green")

        self.run_button = tk.Button(root, text="Run Speed Test", command=self.run_speed_test)
        self.run_button.pack()

    def update_speedometer(self, download_speed, upload_speed):
        self.download_label.config(text=f"Download Speed: {download_speed:.2f} MB/s")
        self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} MB/s")

        self.download_rpm_meter.update_speed(download_speed)
        self.upload_rpm_meter.update_speed(upload_speed)

    def run_speed_test(self):
        st = speedtest.Speedtest()

        def speed_test():
            while True:
                download_speed = st.download() / 1024 / 1024  # Convert to MB/s
                upload_speed = st.upload() / 1024 / 1024  # Convert to MB/s

                self.update_speedometer(download_speed, upload_speed)

                time.sleep(1)  # Update every 1 second

        threading.Thread(target=speed_test, daemon=True).start()

class RPMeter:
    def __init__(self, canvas, x, y, radius, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.speed = 0
        self.rpm_text = canvas.create_text(x, y, text="0 RPM", font=("Helvetica", 12), fill=color)

    def update_speed(self, speed):
        self.speed = speed
        rpm = int(speed * 10)  # Scale for better visualization
        self.canvas.itemconfig(self.rpm_text, text=f"{rpm} RPM")

        self.draw_speedometer()

    def draw_speedometer(self):
        self.canvas.delete(f"{self.rpm_text}_arc")

        start_angle = 90
        extent_angle = min(self.speed * 3.6, 360)  # Scale to 0-360 degrees
        self.canvas.create_arc(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            start=start_angle, extent=extent_angle,
            outline=self.color, width=2, tags=f"{self.rpm_text}_arc"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetSpeedTestApp(root)
    root.mainloop()
