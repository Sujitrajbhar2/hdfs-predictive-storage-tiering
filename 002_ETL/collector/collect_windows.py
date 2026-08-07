from pathlib import Path
import pandas as pd
from datetime import datetime

# Windows Server Path
BASE_DIR = Path("/opt/DataTierAI/001_Data_Sources/windows_server")

records = []

print("="*60)
print("Scanning Windows Enterprise File Server...")
print("="*60)

for department in BASE_DIR.iterdir():

    if department.is_dir():

        for file in department.iterdir():

            stat = file.stat()

            records.append({

                "File_Name": file.name,
                "Department": department.name,
                "Extension": file.suffix,
                "Size_KB": round(stat.st_size / 1024,2),
                "Created_Time": datetime.fromtimestamp(stat.st_ctime),
                "Modified_Time": datetime.fromtimestamp(stat.st_mtime),
                "Source":"Windows Server"

            })

df = pd.DataFrame(records)

output_path = "windows_metadata.csv"

df.to_csv(output_path,index=False)

print(df.head())

print("\nMetadata Saved :",output_path)