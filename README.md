# hsr_ticket

## Function  
以下皆為預設功能 需要更改程式以便進行訂票
- [x] 選擇啟程、到達站
- [x] 選擇出發日期、時間
- [ ] 選擇班次
- [x] 選擇**成人/兒童/敬老/大學生**票數
- [x] 輸入驗證碼
- [x] 選取可訂班次
- [x] 輸入身分證字號
- [x] 輸入手機號碼
- [x] 輸入信箱
- [x] 儲存會員資料
- [ ] 程式運行後指定時間觸發

## Warning
由於高鐵網站會檔selenium 因此需透過特定JS方法來迴避網站偵測透過stealth.min.js避免被網站偵測  
stealth.min.js檔案製作方法為透過Node.js Command 運行
```
npx extract-stealth-evasions
```

Reference:  
https://github.com/maxmilian/thsrc_captcha  (如果要自動辨識驗證碼模型在這)  
https://github.com/BreezeWhite/THSR-Ticket  
https://youtu.be/yhL6VO8xeHA
