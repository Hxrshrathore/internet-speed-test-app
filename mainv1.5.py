import tkinter as tk
from tkinter import Canvas, Button, font
import speedtest
import threading
import time

class InternetSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")
        self.root.geometry("500x250")

        # Set custom font
        custom_font = font.Font(family="Helvetica", size=12)

        self.canvas = Canvas(root, width=500, height=200, bg="#f0f0f0")
        self.canvas.pack()

        self.download_label = tk.Label(root, text="Download Speed: ", font=custom_font)
        self.download_label.pack()

        self.upload_label = tk.Label(root, text="Upload Speed: ", font=custom_font)
        self.upload_label.pack()

        self.download_rpm_meter = RPMeter(self.canvas, 120, 100, 60, "#3498db", "Download")
        self.upload_rpm_meter = RPMeter(self.canvas, 380, 100, 60, "#2ecc71", "Upload")

        self.run_button = RoundedButton(root, text="Run Speed Test", font=custom_font, command=self.run_speed_test)
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
    def __init__(self, canvas, x, y, radius, color, label):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.label = label

        self.speed = 0
        self.rpm_text = canvas.create_text(x, y, text=f"{label}: 0 MB/s", font=("Helvetica", 12), fill=color)

    def update_speed(self, speed):
        self.speed = speed
        self.canvas.itemconfig(self.rpm_text, text=f"{self.label}: {speed:.2f} MB/s")

        self.draw_speedometer()

    def draw_speedometer(self):
        self.canvas.delete(f"{self.rpm_text}_arc")

        start_angle = 90
        extent_angle = min(self.speed * 3.6, 360)  # Scale to 0-360 degrees
        self.canvas.create_arc(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            start=start_angle, extent=extent_angle,
            outline=self.color, fill=self.color, width=2, tags=f"{self.rpm_text}_arc"
        )

class RoundedButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(relief=tk.FLAT, bd=0, bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white")
        self.config(width=15, height=2, pady=5, padx=10, font=("Helvetica", 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetSpeedTestApp(root)
    root.mainloop()
