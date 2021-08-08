from urllib.request import urlretrieve

word_str = "fish"
download_url = "https://dictionary.blob.core.chinacloudapi.cn/media/audio/tom/81/29/812964E469EDC09F7627878F07C58503.mp3"
file_name = word_str + "-ame_pr_url.mp3"

response = urlretrieve(download_url, file_name)
print(response)
