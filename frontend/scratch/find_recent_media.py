import os
import glob

artifacts_dir = r"C:\Users\nihar\.gemini\antigravity\brain\e36329fd-eee3-482b-ad15-fc583f746f17"
files = glob.glob(os.path.join(artifacts_dir, "media__*"))
# Sort by modification time desc
files.sort(key=os.path.getmtime, reverse=True)

print("Recent media files in artifacts:")
for f in files[:5]:
    print(f, os.path.getmtime(f), os.path.getsize(f))
