"""
Automated GitHub API Uploader & Deployment Engine
Reads secure GITHUB_TOKEN from CLI argument or .env file, creates GitHub repository,
and uploads all project files directly via GitHub REST API.
"""

import sys
import os
import json
import base64
from pathlib import Path
import urllib.request
import urllib.error

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

ENV_FILE = config.BASE_DIR / ".env"

def load_env_variables():
    """Reads GITHUB_TOKEN and settings from local .env file."""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

def make_github_request(url, method="GET", data=None, token=None):
    """Sends authenticated HTTP request to GitHub REST API."""
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "Business-Growth-Analytics-Suite")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")

    body_bytes = None
    if data:
        req.add_header("Content-Type", "application/json")
        body_bytes = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, data=body_bytes) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": True, "code": e.code, "message": err_msg}

def push_to_github():
    print("=" * 65)
    print("🚀 AUTOMATED GITHUB DEPLOYMENT ENGINE")
    print("=" * 65)

    env_vars = load_env_variables()
    token = sys.argv[1] if len(sys.argv) > 1 else (os.getenv("GITHUB_TOKEN") or env_vars.get("GITHUB_TOKEN"))
    username = env_vars.get("GITHUB_USERNAME", "vipulpratapsingh-1")
    repo_name = env_vars.get("GITHUB_REPO", "business-growth-analytics-suite")

    if not token or token == "YOUR_PERSONAL_ACCESS_TOKEN_HERE":
        print("\n❌ GITHUB_TOKEN not found!")
        sys.exit(1)

    print(f"[1/4] Authenticating with GitHub API as user: {username}...")
    user_info = make_github_request("https://api.github.com/user", token=token)
    if user_info.get("error"):
        print(f"❌ Authentication Failed: {user_info.get('message')}")
        sys.exit(1)
    
    print(f"✅ Authenticated successfully as: {user_info.get('login')}")

    # Check if Repo Exists
    print(f"[2/4] Checking repository status: {username}/{repo_name}...")
    repo_info = make_github_request(f"https://api.github.com/repos/{username}/{repo_name}", token=token)
    
    if repo_info.get("error") and repo_info.get("code") == 404:
        print(f"[+] Repository '{repo_name}' not found. Creating new repository on GitHub...")
        create_res = make_github_request(
            "https://api.github.com/user/repos",
            method="POST",
            data={
                "name": repo_name,
                "description": "Business Growth Analytics Suite - Enterprise Multi-Region Sales & ML Platform",
                "private": False,
                "auto_init": False
            },
            token=token
        )
        if create_res.get("error"):
            print(f"❌ Repository Creation Failed: {create_res.get('message')}")
            sys.exit(1)
        print(f"✅ Created repository: https://github.com/{username}/{repo_name}")
    else:
        print(f"✅ Found existing repository: https://github.com/{username}/{repo_name}")

    # Gather files to commit
    print(f"[3/4] Indexing files for commit to GitHub 'main' branch...")
    ignore_files = [".git", "__pycache__", ".pytest_cache", ".env", "venv"]
    
    files_to_upload = []
    for root, dirs, files in os.walk(config.BASE_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_files]
        for f in files:
            full_path = Path(root) / f
            rel_path = full_path.relative_to(config.BASE_DIR).as_posix()
            
            # Skip large raw CSV files or python cache or workflows requiring special scopes
            if rel_path.startswith("data/sales_data.csv") or rel_path.startswith(".github/workflows") or f.endswith(".pyc"):
                continue
            
            try:
                with open(full_path, "rb") as file_data:
                    content_base64 = base64.b64encode(file_data.read()).decode("utf-8")
                files_to_upload.append((rel_path, content_base64))
            except Exception as e:
                print(f"[WARN] Skipping {rel_path}: {e}")

    print(f"📦 Prepared {len(files_to_upload)} files for upload...")

    # Upload files using GitHub Contents API
    print(f"[4/4] Uploading files to https://github.com/{username}/{repo_name}...")
    uploaded_count = 0
    for rel_path, content_b64 in files_to_upload:
        url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{rel_path}"
        
        # Check if file exists to get SHA
        existing = make_github_request(url, token=token)
        sha = existing.get("sha") if not existing.get("error") else None
        
        payload = {
            "message": f"Update {rel_path} for Render/Vercel production build",
            "content": content_b64,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        put_res = make_github_request(url, method="PUT", data=payload, token=token)
        if not put_res.get("error"):
            uploaded_count += 1
            print(f"  • Uploaded ({uploaded_count}/{len(files_to_upload)}): {rel_path}")
        else:
            print(f"  ⚠️ Error uploading {rel_path}: {put_res.get('message')}")

    print("=" * 65)
    print(f"✨ SUCCESS! Uploaded {uploaded_count} files to GitHub repository:")
    print(f"👉 GitHub URL: https://github.com/{username}/{repo_name}")
    print("=" * 65)

if __name__ == "__main__":
    push_to_github()
