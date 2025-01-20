import requests
from bs4 import BeautifulSoup
import json

def fetch_wikipedia_articles(topics, num_articles=15):
    dataset = []
    for topic in topics:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        print(f"Συλλογή άρθρου: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = " ".join([para.text for para in paragraphs[:num_articles]])
            dataset.append({
                "title": topic,
                "content": content,
                "url": url
            })
        else:
            print(f"Σφάλμα συλλογής για το θέμα: {topic}")
    return dataset

def save_dataset(dataset, file_path='dataset.json'):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
    print(f"Δεδομένα αποθηκεύτηκαν στο {file_path}")
import requests
from bs4 import BeautifulSoup

def crawl_articles():
    urls = [
        "https://en.wikipedia.org/wiki/Rock_music",
        "https://en.wikipedia.org/wiki/Pop_music",
        "https://en.wikipedia.org/wiki/Heavy_metal_music",
        "https://en.wikipedia.org/wiki/Metallica",
        "https://en.wikipedia.org/wiki/Linkin_Park",
        "https://en.wikipedia.org/wiki/Avenged_Sevenfold",
        "https://en.wikipedia.org/wiki/Jazz",
        "https://en.wikipedia.org/wiki/Classical_music",
        "https://en.wikipedia.org/wiki/Guitar",
        "https://en.wikipedia.org/wiki/Violin",
        "https://en.wikipedia.org/wiki/Clarinet"
    ]
    articles = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1').text
        content = ' '.join([p.text for p in soup.find_all('p')])
        articles.append({"title": title, "content": content, "url": url})
        print(f"Συλλογή άρθρου: {url}")

    return articles
