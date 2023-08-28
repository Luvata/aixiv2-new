import os
import re
import numpy as np


def extract_title(content):
    """Extract the title from the markdown content."""
    title_match = re.search(r"# \[(.*?)\]", content)
    return title_match.group(1).replace(":", " ")

def extract_date(arxiv_id):
    """Extract date from arXiv ID."""
    year = "20" + arxiv_id[:2]
    month = arxiv_id[2:4]
    day = int(np.clip(int(arxiv_id[5:7]) + 1, 1, 31))
    return f"{year}-{month}-{day:02d}"

def remove_existing_frontmatter(content):
    """Remove existing frontmatter."""
    frontmatter_pattern = r"---.*?---\n"
    return re.sub(frontmatter_pattern, "", content, flags=re.DOTALL)

folder_path = 'content/'

# List all markdown files in the folder
markdown_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.md')], reverse=True)
markdown_files.remove("index.md")


index_file_str = """---
title: Hello
---

# Hello

"""


for md_file in markdown_files:
    with open(os.path.join(folder_path, md_file), 'r') as file:
        content = file.read()

    # Remove existing frontmatter
    content = remove_existing_frontmatter(content)

    # Extract title and date
    title = extract_title(content)
    arxiv_id = md_file.replace(".md", "")
    date = extract_date(arxiv_id)

    title_str = f"{arxiv_id} {title}"
    # Create new frontmatter
    if title:
        frontmatter = f"---\ntitle: {title_str}\ndate: {date}\n---\n\n"
        content = frontmatter + content.strip()

        # Write back to file
        with open(os.path.join(folder_path, md_file), 'w') as file:
            file.write(content)

        index_file_str += f"[{title_str}]({md_file})\n\n"


with open("content/index.md", "w") as f:
    f.write(index_file_str)

