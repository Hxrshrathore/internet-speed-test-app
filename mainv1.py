import speedtest

def get_speed():
    st = speedtest.Speedtest()
    
    # Get download speed in bits per second
    download_speed = st.download()
    
    # Get upload speed in bits per second
    upload_speed = st.upload()
    
    # Convert speeds to kilobits per second (1 byte = 8 bits)
    download_speed_kbps = download_speed / 1024
    upload_speed_kbps = upload_speed / 1024
    
    return download_speed_kbps, upload_speed_kbps

def main():
    print("Running Internet Speed Test...")
    download_speed, upload_speed = get_speed()
    
    print(f"Download Speed: {download_speed:.2f} Kbps")
    print(f"Upload Speed: {upload_speed:.2f} Kbps")

if __name__ == "__main__":
    main()
