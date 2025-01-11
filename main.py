import requests
import json
from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup


def get_user_request():
    return input("Hledat: ")


def create_url(msg):
    return f"https://www.google.com/search?q={msg}"


def send_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        return response
    except Exception as e:
        print("Error: Chyba spojeni", e)
        return None


def save_to_file(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(data)
    except Exception:
        print("Error: Chyba souboru")


def save_to_json_file(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception:
        print("Error: Chyba json souboru")


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    organic_results = soup.select("div.tF2Cxc")
    data = []

    for result in organic_results:
        title = result.select_one("h3")
        link = result.select_one("a")
        # snippet = result.select_one("span")

        data.append({
            "title": title.text if title else "No title",
            "link": link.get("href") if link else "No link"
        })

    return data


def main():

    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        error = None
        data = None

        if request.method == "POST":
            query = request.form.get("search")

            if not query:
                error = "Nebylo zadáno žádné hledané slovo"
            else:
                html = send_request(create_url(query))

                if html is None:
                    error = "Chyba spojení"
                else:
                    data = parse_html(html.text)
                    save_to_json_file("data.json", data)

        return render_template("index.html", error=error, data=data)

    app.run(debug=True)


if __name__ == "__main__":
    main()
