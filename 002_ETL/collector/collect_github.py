import requests
import pandas as pd
import json
import time
from pathlib import Path

# =====================================================
# Load Configuration
# =====================================================

CONFIG_PATH = Path("/opt/DataTierAI/001_Data_Sources/api/github_config.json")
TOKEN_PATH = Path("/opt/DataTierAI/001_Data_Sources/api/github_token.txt")

with open(CONFIG_PATH, "r") as file:
    config = json.load(file)

with open(TOKEN_PATH, "r") as file:
    github_token = file.read().strip()

organizations = config["organizations"]
per_page = config["per_page"]
max_pages = config["max_pages"]
output_file = config["output_file"]

# =====================================================
# GitHub Headers
# =====================================================

headers = {
    "User-Agent": "DataTierAI",
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json"
}

# =====================================================
# Authentication Test
# =====================================================

print("=" * 70)
print("GitHub Authentication Test")
print("=" * 70)

response = requests.get(
    "https://api.github.com/rate_limit",
    headers=headers
)

if response.status_code == 200:

    rate = response.json()

    print("Authentication Successful")
    print(f"Remaining Requests : {rate['rate']['remaining']}")
    print(f"Request Limit      : {rate['rate']['limit']}")

else:

    print("Authentication Failed")
    print(response.text)
    exit()

# =====================================================
# GitHub Collector
# =====================================================

print("\n" + "=" * 70)
print("DataTierAI Enterprise GitHub Collector")
print("=" * 70)

repository_data = []

# =====================================================
# Loop Through Organizations
# =====================================================

for organization in organizations:

    print(f"\nCollecting Organization : {organization}")

    page = 1

    while True:

        if page > max_pages:
            break

        url = (
            f"https://api.github.com/orgs/{organization}/repos"
            f"?per_page={per_page}&page={page}"
        )

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code != 200:

            print(f"Connection Failed : {response.status_code}")
            break

        repositories = response.json()

        if len(repositories) == 0:
            break

        print(f"Page {page} : {len(repositories)} repositories")

        for repo in repositories:

            repository_data.append({

                "Organization": organization,
                "Repository_Name": repo.get("name"),
                "Language": repo.get("language"),
                "Visibility": repo.get("visibility"),
                "Repository_Size_KB": repo.get("size"),
                "Stars": repo.get("stargazers_count"),
                "Forks": repo.get("forks_count"),
                "Open_Issues": repo.get("open_issues_count"),
                "Created_Date": repo.get("created_at"),
                "Updated_Date": repo.get("updated_at"),
                "Default_Branch": repo.get("default_branch"),
                "Repository_URL": repo.get("html_url")

            })

        page += 1

        time.sleep(0.3)

# =====================================================
# Create DataFrame
# =====================================================

master_df = pd.DataFrame(repository_data)

master_df.drop_duplicates(inplace=True)

# =====================================================
# Dataset Summary
# =====================================================

print("\n" + "=" * 70)
print("Dataset Summary")
print("=" * 70)

print(master_df.head())

print("\nTotal Records :", len(master_df))

print("\nColumns")

print(master_df.columns.tolist())

# =====================================================
# Save CSV
# =====================================================

OUTPUT_FOLDER = Path("/opt/DataTierAI/002_ETL/output")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

master_df.to_csv(
    OUTPUT_FOLDER / output_file,
    index=False
)

# =====================================================
# Success Message
# =====================================================

print("\n" + "=" * 70)
print("GitHub Metadata Collection Completed")
print("=" * 70)

print(f"Total Records : {len(master_df)}")
print(f"Output File   : {OUTPUT_FOLDER / output_file}")

print("=" * 70)