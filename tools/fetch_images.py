#!/usr/bin/env python3
"""Download your existing images from the live WordPress site into src/assets/img/
under the clean file names the new pages expect.

Run this once from the project folder, on a machine that can reach augello.net:

    python3 tools/fetch_images.py

Safe to re-run: files that already exist are skipped. Do this BEFORE you shut
WordPress down. Where WordPress only shows a resized copy (names ending in
-1024x576 and similar), check the Media Library for the original and drop it in
with the same new file name for the sharpest result.
"""
import sys, urllib.parse, urllib.request
from pathlib import Path

BASE = "https://augello.net/wp-content/uploads/"
LRM = "‎"  # invisible character WordPress left in the Design Thinking file names

IMAGES = {
    "favicon.gif": "2022/08/cropped-CA-270x270.gif",
    "headshot.png": "2024/09/IMG_4230.png",
    "design-workshop.png": "2026/11/DesignWorkshop-1-1024x683.png",
    # product design
    "product-design-hero.png": "2025/01/Screen-Shot-2025-01-27-at-3.50.21-PM.png",
    # ui design
    "ui-design-hero.png": "2025/01/Screen-Shot-2025-01-27-at-2.52.28-PM.png",
    "fund-profile.png": "2016/12/FundProfile.png",
    "recruiter-ipad-app.png": "2016/12/RecruiterApp.png",
    "outback-app-home.png": "2016/12/01_Home-Earn-Badge.png",
    "bonefish-grill-app-home.png": "2016/12/BFG-Home-Track-Badge-576x1024.png",
    # ux design
    "affinitization-exercise.png": "2025/01/AffinitizationExercise.png",
    "card-sort-analysis.png": "2025/01/CardSortAnalysis.png",
    "experience-mapping.png": "2025/01/ExperienceMapping.png",
    "sketches.png": "2025/01/Sketches.png",
    "user-experience.jpg": "2025/01/user-experience-scaled.jpg",
    "ux-design-process.png": "2016/12/UX_Design_Process-1024x834.png",
    "collaborative-ux-process.png": "2016/12/CollaborativeUXProcess.png",
    # user research
    "user-research.jpg": "2025/01/user-research-scaled.jpg",
    "user-research-framework.png": "2025/01/Screen-Shot-2025-01-27-at-2.29.02-PM.png",
    "information-architecture.png": "2025/02/IA.png",
}
for n in range(3, 15):
    IMAGES[f"design-thinking-{n:02d}.jpeg"] = f"2024/09/{LRM}Design-Thinking-Overview.{LRM}{n:03d}-1024x576.jpeg"

out = Path(__file__).resolve().parent.parent / "src" / "assets" / "img"
out.mkdir(parents=True, exist_ok=True)
failed = 0
for name, rel in IMAGES.items():
    dest = out / name
    if dest.exists():
        print("skip  ", name)
        continue
    url = BASE + urllib.parse.quote(rel)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        dest.write_bytes(urllib.request.urlopen(req, timeout=30).read())
        print("saved ", name)
    except Exception as e:
        failed += 1
        print("FAILED", name, "-", e)
print(f"\n{len(IMAGES) - failed}/{len(IMAGES)} images ready in {out}")
sys.exit(1 if failed else 0)
