###### tags: `專題`
# 智慧學習系統 Smart Learning System

## 簡介 Introduction
本系統主要透過**手勢辨識、文字辨識、網路爬蟲、網站架設來實現**，打造一個適合為學習外文、正在學習說話、識字的幼童或老年人士設計的一個閱讀學習系統，**將手指輕輕滑過一個詞彙或一行文字，便能聽到喇叭發出該詞彙的發音與該詞彙的翻譯(翻譯、時態、音標)**。此外，若想學習外文，可以使用本系統的附加功能——即時翻譯，例如：當手指指到「dictionary」單字時，喇叭或耳機便會唸出「dictionary」和「字典」的發音，期望對學習外文有實質性的幫助。

![](https://i.imgur.com/6AFZYzn.jpg)

----------------------------------------

## 環境設定 Environment
- 1.開發環境:**Python 3.7.8**
- 2.在終端機執行 ```pip install -r requirements.txt``` 安裝會使用到的套件
- 3.使用工具:
    - 手部辨識 ：```Mediapipe```
    - 文字辨識：```Pytesseract```
    - 文字校正: ```language_tool_python```
    - 影像處理：```OpenCV```
    - 句意翻譯：```googletrans```
    - 文字轉語言：```gTTS(Google Text-to-Speech)```
    - 容器化工具：```Docker```
    - 爬蟲工具：```BeautifulSoup、Selenium``` 
    - 網站框架：```Django```
    - Python GUI：```PyQt5```
    - 版本管理工具：```Git```
    - 資料庫：```MySQL 8.0.26```
    - 資料庫管理工具：```phpMyAdmin 5.1.1```
    - 函數關係圖輸出工具：```pycallgraph```

----------------------------------------

## 系統開發 Develop
- ### 架構圖 Architecture
    ![](https://i.imgur.com/21JEcl9.jpg)

- ### 流程圖 Flow Chart
    ![](https://i.imgur.com/XdzdwdB.png)
    
- ### 手勢辨識演算法 Gesture Algorithm
    - #### **通過判斷手指彎曲判斷為何種手勢**
        - 正面
            ![](https://i.imgur.com/pMEwfZp.png)
        - 側面
            ![](https://i.imgur.com/vIMCe2b.png)

- ### 主要檔案 Files
    * ```main_program.py```: py檔，主程式py直譯檔
    * ```conf.cfg```: 參數檔，程式參數調整檔
    * ```image_recognition``` 資料夾，存放影像辨識主程式
    * ```word_transtale```: 資料夾，存放爬蟲與googletrans程式
    * ```GUI```: 資料夾，存放GUI程式與資料
    * ```localDictionary.txt```: 記事本，存放本地端單字本

----------------------------------------

## 成果 Result
- ### 使用說明:
  #### 手指比1可以進行框格選取要翻譯的內容，並比2的手勢可以進行影像截圖，辨識結果與翻譯結果將呈現在GUI上，同時也會由gTTS發音。
    
    - #### 1.手指框畫
        ![](https://i.imgur.com/era666k.png)
    - #### 2.影像截圖
        ![](https://i.imgur.com/S3YpONX.png)
  
- #### a.翻譯結果為單字
    ![](https://i.imgur.com/ASuScYi.png)
- #### b.翻譯結果為句子
    ![](https://i.imgur.com/FIUjNVv.png)

- ### 其他功能:
    | 設定 | 使用說明 | 翻譯紀錄 | 打開單字本 |
    | -------- | -------- | -------- |-------- |
    |![](https://i.imgur.com/iopjm5q.png)| ![](https://i.imgur.com/R9Iw2eK.png) | ![](https://i.imgur.com/9P8lVT5.png) | ![](https://i.imgur.com/H5vZpja.png) |


- ### 複習網頁
    | 網頁登入頁面 | 隨機產生單字頁面 | 單字查詢頁面  |
    | -------- | -------- | -------- |
    |![](https://i.imgur.com/6QfkiVl.png)|![](https://i.imgur.com/pMVncRT.png)|![](https://i.imgur.com/wdvDOWA.png)
    
----------------------------------------

## 結論 Summary
此系統的設計，使用了MediaPipe(手部特徵點辨識)、Pytesseract(文字辨識)、language_tool_python(文字校正)、googletrans(句意翻譯)、gTTS(文字轉語音)、Request(請求網站)、BeautifulSoup(解析物件)、PyQT(GUI開發)……等諸多Library，透過這些Library以及演算法的相互結合，才有了這個閱讀系統的雛型。在網站方面，採用Python網頁框架－Django，並同時架設到VPS(1C/1G/25G SSD Linode Ubuntu Server)，同時，我們也會將本專題的程式容器化，用以提供使用者方便部屬與使用。不過，預計成果有些許落差——文字辨識成功率過低，主要原因有：
- 1.**影像畫質**
    如果使用相機畫質不夠高，對於較小的文字，拍攝起來往往會是模糊狀態，進而導致文字無法辨識出結果
- 2.**字型問題**
    遇到非標準英文字型（例如：少女體、藝術字體）時，高機率會辨識不出結果

----------------------------------------

## 未來展望 Expectation
期待隨著未來技術的進步，讓影像畫質能持續提升，使得本專題能夠辨識出更小的文字，也期待未來會出現一種通用型文字辨識模型，進而能辨識出更多字型的文字，提升辨識的準確率