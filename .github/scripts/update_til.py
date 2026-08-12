import os
import sys
import urllib.parse
from datetime import datetime

# GitHub Actions에서 전달받은 변경된 파일 목록
changed_files = sys.argv[1:]

# 폴더명과 마크다운 내 섹션 헤더 매핑 (Screenshot 기준)
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

# 파일명에 사용할 오늘 날짜
today_str = datetime.now().strftime("%Y-%m-%d")
md_filename = f"{today_str}.md"

# 기존 파일 읽기 혹은 새 파일 템플릿 생성
existing_lines = []
if os.path.exists(md_filename):
    with open(md_filename, 'r', encoding='utf-8') as f:
        existing_lines = [line.rstrip('\n') for line in f.readlines()]
else:
    existing_lines = [f"# TIL - {today_str}"]

# 각 폴더별로 마크다운에 내용 추가
for folder, files in new_pdfs.items():
    header = f"## {target_folders[folder]}"
    
    # 해당 섹션(헤더)이 파일에 없으면 추가
    if header not in existing_lines:
        existing_lines.append("")
        existing_lines.append(header)
        existing_lines.append("")
    
    header_idx = existing_lines.index(header)
    insert_idx = header_idx + 2
    
    for path in files:
        # 파일명에서 확장자(.pdf) 제거
        filename = os.path.basename(path).replace('.pdf', '')
        # URL 안전 문자열로 인코딩 (띄어쓰기 등 처리)
        encoded_path = urllib.parse.quote(path)
        link_str = f"- [{filename}]({encoded_path})"
        
        # 중복 입력 방지
        if link_str not in existing_lines:
            existing_lines.insert(insert_idx, link_str)
            insert_idx += 1

# 업데이트된 내용 저장
with open(md_filename, 'w', encoding='utf-8') as f:
    f.write("\n".join(existing_lines) + "\n")