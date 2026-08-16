import os
import sys
import urllib.parse
from datetime import datetime

# GitHub Actions에서 전달받은 변경된 파일 목록
changed_files = sys.argv[1:]

# 폴더명과 마크다운 내 섹션 헤더 매핑
target_folders = {
    "Computer-science": "Computer Science",
    "Data-structure-and-algorithm": "DSA",
    "System-design": "System Design"
}

# 대상 폴더의 PDF 파일만 필터링
new_pdfs = {}
for f in changed_files:
    if f.endswith('.pdf'):
        folder = f.split('/')[0]
        if folder in target_folders:
            if folder not in new_pdfs:
                new_pdfs[folder] = []
            new_pdfs[folder].append(f)

if not new_pdfs:
    sys.exit(0) # 업데이트할 대상 파일이 없으면 정상 종료

today_str = datetime.now().strftime("%Y-%m-%d")
md_filename = "README.md"

# README.md 파일 읽기
if os.path.exists(md_filename):
    with open(md_filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
else:
    # 파일이 없는 경우 기본 템플릿 생성
    lines = ["# 📚 Today I Learned (TIL)", "", "<!-- TIL START -->", ""]

# <!-- TIL START --> 위치 찾기
try:
    start_idx = lines.index("<!-- TIL START -->")
except ValueError:
    lines.extend(["", "<!-- TIL START -->", ""])
    start_idx = lines.index("<!-- TIL START -->")

date_summary = f"<summary><b>📅 {today_str}</b></summary>"
date_exists = False
date_idx = -1

# 오늘 날짜의 블록이 이미 존재하는지 확인
for i in range(start_idx, len(lines)):
    if date_summary in lines[i]:
        date_exists = True
        date_idx = i
        break

if not date_exists:
    # 1. 오늘 날짜 블록이 없을 때 (새로 생성)
    
    # 이전 날짜의 열려있는 토글(<details open>)을 닫힘(<details>) 상태로 변경
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
    
    # <!-- TIL START --> 바로 아래에 삽입
    lines = lines[:start_idx+1] + new_block + lines[start_idx+1:]
    
else:
    # 2. 오늘 날짜 블록이 이미 있을 때 (기존 블록에 추가/업데이트)
    
    # 현재 날짜 블록이 끝나는 </details> 위치 찾기
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
        
        # 헤더가 이미 존재하는지 확인
        header_idx = -1
        for i, line in enumerate(block_lines):
            if line.startswith(header):
                header_idx = i
                break
                
        if header_idx == -1:
            # 헤더가 없으면 블록 맨 끝에 헤더와 파일 추가
            block_lines.append(header)
            for path in files:
                filename = os.path.basename(path).replace('.pdf', '')
                encoded_path = urllib.parse.quote(path)
                block_lines.append(f"- [{filename}]({encoded_path})")
            block_lines.append("")
        else:
            # 헤더가 있으면 그 아래에 중복 확인 후 추가
            insert_idx = header_idx + 1
            for path in files:
                filename = os.path.basename(path).replace('.pdf', '')
                encoded_path = urllib.parse.quote(path)
                link_str = f"- [{filename}]({encoded_path})"
                
                if link_str not in block_lines:
                    block_lines.insert(insert_idx, link_str)
                    insert_idx += 1
                    
    # 원본 라인 리스트 업데이트
    lines = lines[:date_idx] + block_lines + lines[end_details_idx:]

# 업데이트된 내용 README.md에 덮어쓰기
with open(md_filename, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines) + "\n")