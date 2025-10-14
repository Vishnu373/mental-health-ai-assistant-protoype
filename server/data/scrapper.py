import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException
from .data.sources import medline_urls

def get_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_medline_page(html_content, url):
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get title
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "Title not found"
    
    # Find Summary and Start Here - try different variations
    summary = (soup.find('h2', string='Summary') or 
              soup.find('h3', string='Summary') or
              soup.find('h2', string=lambda x: x and 'summary' in x.lower()) or
              soup.find('h3', string=lambda x: x and 'summary' in x.lower()))
    
    start_here = (soup.find('h2', string='Start Here') or 
                 soup.find('h3', string='Start Here') or
                 soup.find('h2', string=lambda x: x and 'start here' in x.lower()) or
                 soup.find('h3', string=lambda x: x and 'start here' in x.lower()))    
    
    if not summary:
        return {"title": title, "url": url, "content": "No Summary found"}
    
    # Get all paragraphs and lists in the entire document
    content_parts = []
    all_content = soup.find_all(['p', 'ul', 'ol'])
    
    # Simple approach: get content that comes after Summary in document order
    summary_index = None
    start_here_index = None
    
    for i, elem in enumerate(soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol'])):
        if elem == summary:
            summary_index = i
        elif elem == start_here:
            start_here_index = i
            break
    
    if summary_index is not None:
        for elem in soup.find_all(['p', 'ul', 'ol']):
            elem_index = None
            for i, all_elem in enumerate(soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol'])):
                if all_elem == elem:
                    elem_index = i
                    break
            
            if elem_index and elem_index > summary_index:
                if start_here_index and elem_index >= start_here_index:
                    break
                text = elem.get_text(strip=True)
                if text and len(text) > 5:
                    content_parts.append(text)
    
    content = '\n'.join(content_parts)
    
    return {
        "title": title,
        "url": url,
        "content": content if content else "No content found"
    }

def main():
    all_data = []
    
    for i, url in enumerate(medline_urls):
        html = get_page_content(url)
        data = parse_medline_page(html, url)
        if data:
            all_data.append(data)
        time.sleep(1)
    
    with open("data/knowledge_base.txt", 'w', encoding='utf-8') as f:
        for data in all_data:
            f.write(f"{data['title']}\n")
            f.write(data['content'])
            f.write(f"\n\n")
    
if __name__ == "__main__":
    main()