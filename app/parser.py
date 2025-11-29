from bs4 import BeautifulSoup

def parse_quiz(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    links = [a["href"] for a in soup.find_all("a", href=True)]
    submit_url = None
    for a in soup.find_all("a", href=True):
        if "submit" in a["href"]:
            submit_url = a["href"]

    return {
        "question": text,
        "links": links,
        "submit_url": submit_url
    }
