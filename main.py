import requests
import json
from bs4 import BeautifulSoup

def get_user_request():
    return input("Hledat: ")

def create_url(msg):
    return f"https://www.google.com/search?q={msg}"

def send_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors 
        return response
    except Exception as e:
        print("Error: Chyba spojeni")
        return None

def save_to_file(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        print("Error: Chyba souboru")

def save_to_json_file(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error: Chyba json souboru")
   

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    organic_results = soup.select("div.tF2Cxc")
    data = []

    for result in organic_results:
        title = result.select_one("h3")
        link = result.select_one("a")
        #snippet = result.select_one("span")

        data.append({
            "title": title.text if title else "No title", 
            "link": link.get("href") if link else "No link"
        })

    return data

def main():

    query = get_user_request()
    html = send_request(create_url(query))

    if html is not None:
        #print(parse_html(html.text))
        save_to_json_file("data.json", parse_html(html.text))
        #save_to_file("data", html.text)

if __name__ == "__main__":
    main()