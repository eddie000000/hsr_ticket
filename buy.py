import time, cv2, csv, datetime
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from keras.models import load_model
from preprocessBatch import preprocessing
from time import sleep
from selenium.webdriver import Chrome
import matplotlib.pyplot as plt

WIDTH = 140
HEIGHT = 48
allowedChars = '234579ACFHKMNPQRTYZ';

print('model loading...')
model = load_model("thsrc_cnn_model.hdf5")
print('loading completed')

delay = 0.5

option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=option)


with open('F:/hsrticket/stealth.min.js') as f:
    js = f.read()

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    
    
    
    
driver.get('https://irs.thsrc.com.tw/IMINT/?locale=tw')
sleep(5)  #加入等待

driver.find_element_by_id("btn-confirm").click()
sleep(delay)
driver.save_screenshot('tem.png')  #擷取螢幕後存檔
captchaid = driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode')  #驗證碼圖形id
#取得圖形位置
x1 = captchaid.location['x']
y1 = captchaid.location['y']
x2 = x1 + captchaid.size['width']
y2 = y1 + captchaid.size['height']
image1 = Image.open('tem.png')  #讀取螢幕圖形
image2 = image1.crop((x1, y1, x2, y2))  #擷取驗證碼圖形
image2.save('captcha.png')  #圖形存檔
plt.imshow(image2)
#plt.show()



image2 = image2.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
image2 = image2.convert('RGB')
image2.save('captchargb.jpg', "JPEG")

preprocessing('captchargb.jpg', 'preprocessing.jpg')

train_data = np.stack([np.array(cv2.imread("preprocessing.jpg"))/255.0])
prediction = model.predict(train_data)

predict_captcha = ''
for predict in prediction:
    value = np.argmax(predict[0])
    predict_captcha += allowedChars[value]
print(predict_captcha)
#captchatext = input('輸入驗證碼：')  
captchatext = predict_captcha
# <option value="1">南港</option>
# <option value="2">台北</option>
# <option value="3">板橋</option>
# <option value="4">桃園</option>
# <option value="5">新竹</option>
# <option value="6">苗栗</option>
# <option value="7">台中</option>
# <option value="8">彰化</option>
# <option value="9">雲林</option>
# <option value="10">嘉義</option>
# <option value="11">台南</option>
# <option value="12">左營</option>
driver.find_element_by_name("selectStartStation").click()
sleep(delay)

driver.find_element_by_xpath("(//option[@value='4'])[1]").click() #桃園
sleep(delay)

driver.find_element_by_name("selectDestinationStation").click()
sleep(delay)

driver.find_element_by_xpath("(//option[@value='8'])[2]").click() #彰化
sleep(delay)

#seatRadio0:無 seatRadio1:靠窗優先 seatRadio2:走道優先
driver.find_element_by_id("seatRadio0").click()
sleep(delay)

#訂票日期
driver.find_element_by_css_selector('#toTimeInputField').clear()
sleep(delay)
inputDate = driver.find_element_by_css_selector('#toTimeInputField')
inputDate.send_keys('2022/02/10')
sleep(delay)

# driver.find_element_by_id("ToTimePicker").click()
# sleep(delay)

# driver.find_element_by_xpath("//tbody/tr[3]/td[3]").click()
# sleep(delay)

# <name="toTimeTable">
# <option value="1201A">00:00</option>
# <option value="1230A">00:30</option>
# <option value="500A">05:00</option>
# <option value="530A">05:30</option>
# <option value="600A">06:00</option>
# <option value="630A">06:30</option>
# <option value="700A">07:00</option>
# <option value="730A">07:30</option>
# <option value="800A">08:00</option>
# <option value="830A">08:30</option>
# <option value="900A">09:00</option>
# <option value="930A">09:30</option>
# <option value="1000A">10:00</option>
# <option value="1030A">10:30</option>
# <option value="1100A">11:00</option>
# <option value="1130A">11:30</option>
# <option value="1200N">12:00</option>
# <option value="1230P">12:30</option>
# <option value="100P">13:00</option>
# <option value="130P">13:30</option>
# <option value="200P">14:00</option>
# <option value="230P">14:30</option>
# <option value="300P">15:00</option>
# <option value="330P">15:30</option>
# <option value="400P">16:00</option>
# <option value="430P">16:30</option>
# <option value="500P">17:00</option>
# <option value="530P">17:30</option>
# <option value="600P">18:00</option>
# <option value="630P">18:30</option>
# <option value="700P">19:00</option>
# <option value="730P">19:30</option>
# <option value="800P">20:00</option>
# <option value="830P">20:30</option>
# <option value="900P">21:00</option>
# <option value="930P">21:30</option>
# <option value="1000P">22:00</option>
# <option value="1030P">22:30</option>
# <option value="1100P">23:00</option>
# <option value="1130P">23:30</option>


driver.find_element_by_xpath("(//option[@value='430P'])[1]").click()
sleep(delay)
# 張數 
# 全票 1F~10F
# 孩童票 1H~10H
# 愛心票 1W~10W
# 敬老票 1E~10E
# 大學生優惠票 1P~10P
driver.find_element_by_xpath("(//option[@value='0F'])[1]").click()
driver.find_element_by_xpath("(//option[@value='1P'])[1]").click()
sleep(delay)

#送驗證碼
# driver.find_element_by_name("homeCaptcha:securityCode").send_keys("\n")
# sleep(delay)
driver.find_element_by_name("homeCaptcha:securityCode").clear()
sleep(delay)
driver.find_element_by_name("homeCaptcha:securityCode").send_keys(captchatext)
sleep(delay)
#開始查詢
driver.find_element_by_id("SubmitButton").click()
sleep(delay)

#第幾班車
driver.find_element_by_xpath("(//input[@name='TrainQueryDataViewPanel:TrainGroup'])[2]").click()
sleep(delay)
#確認車次
driver.find_element_by_name("SubmitButton").click()
sleep(delay)

#ID
driver.find_element_by_id("idNumber").click()
sleep(delay)
driver.find_element_by_id("idNumber").clear()
sleep(delay)
driver.find_element_by_id("idNumber").send_keys("A11325201")
sleep(delay)
#mobile
driver.find_element_by_id("mobileInputRadio").click()
sleep(delay)
driver.find_element_by_id("mobilePhone").click()
sleep(delay)
driver.find_element_by_id("mobilePhone").clear()
sleep(delay)
driver.find_element_by_id("mobilePhone").send_keys("0972455782")
sleep(delay)
#email
driver.find_element_by_id("name2622").click()
sleep(delay)
driver.find_element_by_id("name2622").send_keys("abc123@gmail.com")
sleep(delay)
#membership info
driver.find_element_by_id("memberSystemCheckBox").click()
sleep(delay)
driver.find_element_by_id("memberShipCheckBox").click()
sleep(delay)

#我已明確了解
driver.find_element_by_name("agree").click()
sleep(delay)


driver.find_element_by_id("isSubmit").click()
sleep(2)
# driver.find_element_by_name("//*[@id="btn-custom2"]").click()
driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div/table/tbody/tr/td[3]/input").click()
print('完成訂票！')