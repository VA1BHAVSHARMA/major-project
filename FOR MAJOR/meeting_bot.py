import selenium.webdriver as webdriver
import speech_recognition as sr
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pydub import AudioSegment
import time

def Glogin(driver, password, mail_address):
		# Sign in button
		driver.find_element(By.XPATH,
						'/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[1]/div[2]/div[1]/div/span/span').click()
		print("sign in button pressed")

		# input Gmail
		driver.find_element(By.ID, "identifierId").send_keys(mail_address)
		driver.find_element(By.ID, "identifierNext").click()
		print("email entered")
		driver.implicitly_wait(10)

		# input Password
		driver.find_element(By.XPATH,
			'/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(password)
		driver.implicitly_wait(10)
		driver.find_element(By.ID, "passwordNext").click()
		print("password entered")
		driver.implicitly_wait(4000)


def turnOffMicCam(driver):
    # turn off Microphone
    time.sleep(2)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[7]/div[1]/div/div/div/div/div[1]').click()
    print("mic off")
    driver.implicitly_wait(3000)

    # turn off camera
    time.sleep(1)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div[1]/div/div[1]/div[1]/div/div[7]/div[1]/div/div/div/div/div[1]').click()
    print("cam off")
    driver.implicitly_wait(3000)
    

def joinNow(driver):
    # Join meet
    print(1)
    time.sleep(5)
    driver.implicitly_wait(2000)
    driver.find_element(By.CSS_SELECTOR,
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
    print("joined")
    print(1)


def AskToJoin(driver):
    # Ask to Join meet
    time.sleep(3)
    # driver.implicitly_wait(2000)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/c-wiz/div/div/div[38]/div[4]/div/div[2]/div[4]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/button/span[4]').click()
    # driver.find_element(By.CSS_SELECTOR,
    #     'div.UywwFc-RLmnJb').click()
    
    print("joined")
    # Ask to join and join now buttons have same xpaths


def join_meeting_and_record(platform, link):
    mail_address = 'know.youwu@gmail.com'
    password = 'nounounounou'
    opt = Options()
    opt.add_argument('--disable-blink-features=AutomationControlled')
    opt.add_argument('--start-maximized')
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1
    })
    driver = webdriver.Chrome(options=opt)

    # driver = webdriver.Chrome()
    driver.get(link)
    # time.sleep(5)  # Allow time to join the meeting
    Glogin(driver, password, mail_address)
    turnOffMicCam(driver)
    #joinNow()
    AskToJoin(driver)
    driver.close()
    print('fin')

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording...")
        audio = recognizer.listen(source, timeout=60)

    audio_file = "meeting_audio.wav"
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    driver.quit()

    return convert_audio_to_text(audio_file)

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)