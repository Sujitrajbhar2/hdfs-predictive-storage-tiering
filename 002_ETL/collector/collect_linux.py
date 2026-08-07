from pathlib import Path
import pandas as pd
from datetime import datetime

# =====================================
# Linux Server Path
# =====================================

BASE_DIR = Path("/opt/DataTierAI/001_Data_Sources/linux_server")

records = []

print("="*60)
print("Scanning Linux Enterprise Server...")
print("="*60)

for folder in BASE_DIR.iterdir():

    if folder.is_dir():

        for file in folder.iterdir():

            stat = file.stat()

            records.append({

                "File_Name": file.name,
                "Folder": folder.name,
                "Extension": file.suffix,
                "Size_KB": round(stat.st_size/1024,2),
                "Created_Time": datetime.fromtimestamp(stat.st_ctime),
                "Modified_Time": datetime.fromtimestamp(stat.st_mtime),
                "Source":"Linux Server"

            })

df = pd.DataFrame(records)

output_file = "linux_metadata.csv"

df.to_csv(output_file,index=False)

print(df.head())

print("\nMetadata Saved :",output_file)