from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import tkinter as tk
import tkinter.messagebox as tkm


window = tk.Tk()
window.title("Complaint Sender")
window.geometry("300x300")
window.resizable(False, False)

def get_numbers(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().split("\n")

def get_phrases(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().split("\n")

def wait_for_element(driver, element_xpath):
    wait = WebDriverWait(driver, 10)
    return wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))


def fill_fields():
    global index, NUMBERS_FILE
    phone_numbers = get_numbers(NUMBERS_FILE)
    phrases_list = get_phrases(PHRASES_FILE)

    # Инициализация драйвера (в данном случае Chrome)
    driver = webdriver.Chrome()

    # Открытие страницы для жалобы
    driver.get("https://online.toroslaredas.com.tr/ariza-bildir")

    # Заполнение полей
    policy_button = wait_for_element(driver, '/html/body/div[6]/div/button[1]')
    policy_button.click()

    home_choice = wait_for_element(driver, '//*[@id="radio-ariza_tipi"]/div[3]/label')
    home_choice.click()

    il_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[2]/div/button')
    il_dd_choice.click()

    mersin_option_choice = wait_for_element(driver, '//*[@id="bs-select-1-5"]')
    mersin_option_choice.click()

    ilce_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[3]/div/button')
    ilce_dd_choice.click()

    mezitli_option_choice = wait_for_element(driver, '//*[@id="bs-select-2-8"]')
    mezitli_option_choice.click()

    bucak_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[4]/div/button')
    bucak_dd_choice.click()

    merkez_option_choice = wait_for_element(driver, '//*[@id="bs-select-3-1"]')
    merkez_option_choice.click()

    koy_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[5]/div/button')
    koy_dd_choice.click()

    merkez2_option_choice = wait_for_element(driver, '//*[@id="bs-select-4-1"]')
    merkez2_option_choice.click()

    mahalle_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[6]/div/button')
    mahalle_dd_choice.click()

    viran_option_choice = wait_for_element(driver, '//*[@id="bs-select-5-38"]')
    viran_option_choice.click()

    sokak_dd_choice = wait_for_element(driver, '//*[@id="farkliAdresDiv"]/div/div[7]/div/button')
    sokak_dd_choice.click()

    sn_option_choice = wait_for_element(driver, '//*[@id="bs-select-6-10"]')
    sn_option_choice.click()

    bina_input = wait_for_element(driver, '//*[@id="binaNo"]')
    bina_input.send_keys("1")

    detayi_text = wait_for_element(driver, '//*[@id="IslemDetay"]')
    detayi_text.send_keys(random.choice(phrases_list))

    phone_input = wait_for_element(driver, '//*[@id="telefon"]')
    phone_input.send_keys(phone_numbers[index])

    if index > 1:
        notifications_enable = wait_for_element(driver, '//*[@id="arizaBildirmeForm"]/div[2]/div/div/div[7]/div[1]/div[2]/label')
        notifications_enable.click()

    print("У вас есть 20 секунд чтобы пройти капчу")
    tkm.showinfo("Внимание!", "У вас есть 20 секунд чтобы пройти капчу")
    time.sleep(20)
    print("Если вы успели пройти капчу, все отлично!")
    tkm.showinfo("Внимание!", "Если вы успели пройти капчу, все отлично!")
    answer = tkm.askquestion("Капча", "Вы прошли капчу? Если вы не прошли капчу, то запрос не отправится и программа продолжит работу. Нажмите нет если вы ее не прошли, чтобы отправить этот запрос снова и пройти капчу")
    print(answer)
    if answer == "no":
        raise Exception

    # раскоментировать когда скрипт будет готов
    # submit_btn = wait_for_element(driver, '//*[@id="btnArizaBildir"]')
    # submit_btn.click()
    driver.quit()

def run_loop():
    global index, NUMBERS_FILE
    request_btn.config(state=tk.DISABLED)
    phone_numbers = get_numbers(NUMBERS_FILE)
    while index < len(phone_numbers):
        time.sleep(1)
        try:
            fill_fields()
            index += 1
            print("index = ", index)
        except Exception as e:
            print('Произошла ошибка, пробуем еще раз')
            tkm.showerror("Ошибка", "Произошла ошибка, пробуем еще раз. Для успешной отправки запроса рекомендую не трогать ничего в процессе заполнения формы.")
    request_btn.config(state=tk.NORMAL)

index = 0
NUMBERS_FILE = "phone_numbers.txt"
PHRASES_FILE = "random_phrases.txt"

info_label = tk.Label(window, text="Нажмите старт, чтобы начать отправку запросов. Всего будет отправлено 4 запроса.", wraplength=300, font=("Arial", 12))
info_label.pack(pady=10)
request_btn = tk.Button(window, text="Старт", font=("Arial", 14), command=run_loop)
request_btn.pack(pady=10)


window.mainloop()
