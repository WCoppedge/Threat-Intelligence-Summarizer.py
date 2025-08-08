from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# Load summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Get the CISA alerts page
base_url =  "https://www.cisa.gov/news-events/alerts/2025/08/07/cisa-issues-ed-25-02-mitigate-microsoft-exchange-vulnerability"
url = f"{base_url}/news-events/alerts"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# Find the first alert link
first_link_tag = soup.find("a", href=True)
if first_link_tag:
    alert_link = base_url + first_link_tag['href']
    print(f"Fetching alert from: {alert_link}")

    # Fetch alert page content
    alert_html = requests.get(alert_link).text
    alert_soup = BeautifulSoup(alert_html, "html.parser")

    # Grab all paragraph text
    paragraphs = [p.get_text() for p in alert_soup.find_all("p")]
    full_text = " ".join(paragraphs)

    # Only summarize if we have text
    if len(full_text) > 100:
        summary = summarizer(full_text, max_length=100, min_length=30, do_sample=False)
        print("\nSummary:\n", summary[0]['summary_text'])
    else:
        print("No enough text found to summarize.")
else:
    print("No alert links found.")
