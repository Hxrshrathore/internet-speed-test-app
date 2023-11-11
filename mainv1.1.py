import tkinter as tk
from tkinter import Canvas
import speedtest

class InternetSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")

        self.canvas = Canvas(root, width=300, height=300)
        self.canvas.pack()

        self.download_label = tk.Label(root, text="Download Speed: ")
        self.download_label.pack()

        self.upload_label = tk.Label(root, text="Upload Speed: ")
        self.upload_label.pack()

        self.run_button = tk.Button(root, text="Run Speed Test", command=self.run_speed_test)
        self.run_button.pack()

    def update_speedometer(self, download_speed, upload_speed):
        self.canvas.delete("all")

        center_x, center_y = 150, 150
        radius = 120

        # Draw speedometer circle
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black", width=2)

        # Draw download speed indicator
        self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius, start=0, extent=download_speed * 2.7, fill="blue")

        # Draw upload speed indicator
        self.canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius, start=180, extent=upload_speed * 2.7, fill="green")

    def run_speed_test(self):
        st = speedtest.Speedtest()
        
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps

        self.download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")

        self.update_speedometer(download_speed, upload_speed)

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetSpeedTestApp(root)
    root.mainloop()
