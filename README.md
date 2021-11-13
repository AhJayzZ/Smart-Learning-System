###### tags: `專題`
# 智慧學習系統 Smart Learning System

## 簡介 Introduction
本系統主要透過**手勢辨識、文字辨識、網路爬蟲、網站架設來實現**，打造一個適合為學習外文、正在學習說話、識字的幼童或老年人士設計的一個閱讀學習系統，**將手指輕輕滑過一個詞彙或一行文字，便能聽到喇叭發出該詞彙的發音與該詞彙的翻譯(翻譯、時態、音標)**。此外，若想學習外文，可以使用本系統的附加功能——即時翻譯，例如：當手指指到「dictionary」單字時，喇叭或耳機便會唸出「dictionary」和「字典」的發音，期望對學習外文有實質性的幫助。

----------------------------------------

## 環境設定 Environment
- 1.本系統由**Python 3.7.8開發**
- 2.在終端機執行 ```pip install -r requirements.txt``` 安裝會使用到的套件
- 3.使用工具
    - 手部特徵點API ：```Mediapipe```
    - 文字辨識API   ：```Pytesseract```
    - 文字校正API: ```language_tool_python```
    - 影像處理API：```OpenCV```
    - 翻譯API：```googletrans```
    - 文字轉語言API：```gTTS(Google Text-to-Speech)```
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
  
    - #### 1.翻譯結果為單字
        ![](https://i.imgur.com/ASuScYi.png)
    - #### 2.翻譯結果為句子
        ![](https://i.imgur.com/FIUjNVv.png)

- ### 其他功能:
    | 設定 | 使用說明 | 翻譯紀錄 | 打開單字本 |
    | -------- | -------- | -------- |-------- |
    |![](https://i.imgur.com/iopjm5q.png)| ![](https://i.imgur.com/R9Iw2eK.png) | ![](https://i.imgur.com/9P8lVT5.png) | ![](https://i.imgur.com/H5vZpja.png) |


- ### 複習網頁
    | 網頁登入頁面 | 隨機產生單字頁面 | 單字查詢頁面  |
    | -------- | -------- | -------- |
    |![](https://i.imgur.com/6QfkiVl.png)|![](https://i.imgur.com/pMVncRT.png)|![](https://i.imgur.com/wdvDOWA.png)