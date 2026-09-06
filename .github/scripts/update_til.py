import os
import sys
import urllib.parse
from datetime import datetime

changed_files = sys.argv[1:]

target_folders = {
    "Computer-science": "Computer Science",
    "Data-structure-and-algorithm": "DSA",
    "System-design": "System Design"
}

new_pdfs = {}
for f in changed_files:
    if f.endswith('.pdf'):
        folder = f.split('/')[0]
        if folder in target_folders:
            if folder not in new_pdfs:
                new_pdfs[folder] = []
            new_pdfs[folder].append(f)

if not new_pdfs:
    sys.exit(0)

today_str = datetime.now().strftime("%Y-%m-%d")
md_filename = "README.md"

if os.path.exists(md_filename):
    with open(md_filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
else:
    lines = ["# 📚 Today I Learned (TIL)", "", "<!-- TIL START -->", ""]

try:
    start_idx = lines.index("<!-- TIL START -->")
except ValueError:
    lines.extend(["", "<!-- TIL START -->", ""])
    start_idx = lines.index("<!-- TIL START -->")

date_summary = f"<summary><b>📅 {today_str}</b></summary>"
date_exists = False
date_idx = -1

for i in range(start_idx, len(lines)):
    if date_summary in lines[i]:
        date_exists = True
        date_idx = i
        break

if not date_exists:
    
    for i in range(start_idx, len(lines)):
        if "<details open>" in lines[i]:
            lines[i] = lines[i].replace("<details open>", "<details>")

    new_block = [
        "",
        "<details open>",
        date_summary,
        ""
    ]
    
    for folder, files in new_pdfs.items():
        header = f"### {target_folders[folder]}"
        new_block.append(header)
        for path in files:
            filename = os.path.basename(path).replace('.pdf', '')
            encoded_path = urllib.parse.quote(path)
            new_block.append(f"- [{filename}]({encoded_path})")
        new_block.append("")
    
    new_block.append("</details>")
    
    lines = lines[:start_idx+1] + new_block + lines[start_idx+1:]
    
else:
    
    end_details_idx = -1
    for i in range(date_idx, len(lines)):
        if "</details>" in lines[i]:
            end_details_idx = i
            break
            
    if end_details_idx == -1:
        end_details_idx = len(lines)
        
    block_lines = lines[date_idx:end_details_idx]
    
    for folder, files in new_pdfs.items():
        header = f"### {target_folders[folder]}"
        
        header_idx = -1
        for i, line in enumerate(block_lines):
            if line.startswith(header):
                header_idx = i
                break
                
        if header_idx == -1:
            block_lines.append(header)
            for path in files:
                filename = os.path.basename(path).replace('.pdf', '')
                encoded_path = urllib.parse.quote(path)
                block_lines.append(f"- [{filename}]({encoded_path})")
            block_lines.append("")
        else:
            insert_idx = header_idx + 1
            for path in files:
                filename = os.path.basename(path).replace('.pdf', '')
                encoded_path = urllib.parse.quote(path)
                link_str = f"- [{filename}]({encoded_path})"
                
                if link_str not in block_lines:
                    block_lines.insert(insert_idx, link_str)
                    insert_idx += 1
                    
    lines = lines[:date_idx] + block_lines + lines[end_details_idx:]

with open(md_filename, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines) + "\n")