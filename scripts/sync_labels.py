import requests
import os

# Get GitHub token from environment variable
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"}

SOURCE_REPO = "TestRepoProject/meta-sync-source"
TARGET_REPOS = [
    "TestRepoProject/meta-sync-target-1",
    "TestRepoProject/meta-sync-target-2"
]

# Fetch all labels from a repo
def get_labels(repo):
    url = f"https://api.github.com/repos/{repo}/labels"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Failed to fetch labels from {repo}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return []

    return response.json()

# Create or update label in target repo
def create_or_update_label(repo, label):
    label_name = label["name"]
    label_data = {
        "name": label_name,
        "color": label.get("color", "ffffff"),
        "description": label.get("description", "")
    }

    # Check if label exists
    existing_labels = get_labels(repo)
    existing_names = [lbl["name"] for lbl in existing_labels]

    if label_name in existing_names:
        # Update label
        url = f"https://api.github.com/repos/{repo}/labels/{label_name}"
        response = requests.patch(url, headers=HEADERS, json=label_data)
        action = "updated"
    else:
        # Create label
        url = f"https://api.github.com/repos/{repo}/labels"
        response = requests.post(url, headers=HEADERS, json=label_data)
        action = "created"

    if response.status_code not in [200, 201]:
        print(f"❌ Failed to {action} label '{label_name}' in {repo}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    else:
        print(f"✅ Successfully {action} label '{label_name}' in {repo}")

# Sync labels from source repo to all target repos
def sync_labels():
    source_labels = get_labels(SOURCE_REPO)
    if not source_labels:
        print("⚠️ No labels found or failed to fetch. Stopping sync.")
        return

    for repo in TARGET_REPOS:
        print(f"\n🔄 Syncing labels to {repo}...")
        for label in source_labels:
            create_or_update_label(repo, label)

if __name__ == "__main__":
    sync_labels()
