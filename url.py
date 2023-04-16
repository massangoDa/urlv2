import os
import requests
import cssbeautifier
import jsbeautifier
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

url = "https://eromanga-numa.com/%e3%83%ac%e3%82%a4%e3%83%97/585137"

# URLからHTMLコードを取得する
response = requests.get(url)
html_code = response.text

# HTMLの中からCSSとJavaScriptのリンクを探す
css_code = ""
js_code = ""
soup = BeautifulSoup(html_code, "html.parser")
for link in soup.find_all("link"):
    if link.get("rel") == ["stylesheet"]:
        css_url = link.get("href")
        if not css_url.startswith("http"):
            css_url = urljoin(url, css_url)
        css_response = requests.get(css_url)
        css_code += css_response.text

for script in soup.find_all("script"):
    if script.get("src"):
        js_url = script.get("src")
        if not js_url.startswith("http"):
            js_url = urljoin(url, js_url)
        js_response = requests.get(js_url)
        js_code += js_response.text

# コードを整形する
formatted_html_code = html_code
formatted_css_code = cssbeautifier.beautify(css_code)
formatted_js_code = jsbeautifier.beautify(js_code)

# ファイル名を生成する
file_name = urlparse(url).path.split("/")[-1]
if not file_name:
    file_name = "index.html"
if not file_name.endswith(".html"):
    file_name += ".html"

# ダウンロードフォルダーを指定する
download_folder = "./test"

# ダウンロードフォルダーが存在しなければ作成する
if not os.path.exists(download_folder):
    os.makedirs(download_folder)


#保存
with open(os.path.join(download_folder, file_name), "w", encoding="utf-8") as f:
    f.write(formatted_html_code)

with open(os.path.join(download_folder, "styles.css"), "w", encoding="utf-8") as f:
    f.write(formatted_css_code)

with open(os.path.join(download_folder, "script.js"), "w", encoding="utf-8") as f:
    f.write(formatted_js_code)






print("ダウンロードが完了しました。")
