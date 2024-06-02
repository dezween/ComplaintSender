
# import asyncio
# from playwright.async_api import async_playwright
# import random
# import tkinter as tk
# import tkinter.messagebox as tkm
# import threading

# class ComplaintSenderApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Complaint Sender")
#         self.geometry("400x400")
#         self.resizable(False, False)
#         self.index = 0
#         self.NUMBERS_FILE = "phone_numbers.txt"
#         self.PHRASES_FILE = "random_phrases.txt"
#         self.create_widgets()

#     def create_widgets(self):
#         info_label = tk.Label(self, text="Нажмите старт, чтобы начать отправку запросов. Всего будет отправлено 4 запроса.", wraplength=350, font=("Arial", 12))
#         info_label.pack(pady=20)

#         self.request_btn = tk.Button(self, text="Старт", font=("Arial", 14), command=self.run_loop)
#         self.request_btn.pack(pady=20)

#         self.progress_label = tk.Label(self, text="", font=("Arial", 12))
#         self.progress_label.pack(pady=10)

#     def get_numbers(self, file_path):
#         with open(file_path, "r", encoding="utf-8") as file:
#             return file.read().split("\n")

#     def get_phrases(self, file_path):
#         with open(file_path, "r", encoding="utf-8") as file:
#             return file.read().split("\n")

#     async def wait_for_element(self, page, selector):
#         await page.wait_for_selector(selector)
#         return await page.query_selector(selector)

#     async def fill_fields(self, browser):
#         phone_numbers = self.get_numbers(self.NUMBERS_FILE)
#         phrases_list = self.get_phrases(self.PHRASES_FILE)

#         # Инициализация новой страницы
#         context = await browser.new_context()
#         page = await context.new_page()

#         # Открытие страницы для жалобы
#         await page.goto("https://online.toroslaredas.com.tr/ariza-bildir")

#         # Заполнение полей
#         await (await self.wait_for_element(page, 'xpath=/html/body/div[6]/div/button[1]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="radio-ariza_tipi"]/div[3]/label')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[2]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-1-5"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[3]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-2-8"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[4]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-3-1"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[5]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-4-1"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[6]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-5-38"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[7]/div/button')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-6-10"]')).click()
#         await (await self.wait_for_element(page, 'xpath=//*[@id="binaNo"]')).fill("1")
#         await (await self.wait_for_element(page, 'xpath=//*[@id="IslemDetay"]')).fill(random.choice(phrases_list))
#         await (await self.wait_for_element(page, 'xpath=//*[@id="telefon"]')).fill(phone_numbers[self.index])

#         if self.index > 1:
#             await (await self.wait_for_element(page, 'xpath=//*[@id="arizaBildirmeForm"]/div[2]/div/div/div[7]/div[1]/div[2]/label')).click()

#         tkm.showinfo("Внимание!", "У вас есть 20 секунд чтобы пройти капчу")
#         await asyncio.sleep(20)
#         answer = tkm.askquestion("Капча", "Вы прошли капчу? Если вы не прошли капчу, то запрос не отправится и программа продолжит работу. Нажмите нет если вы ее не прошли, чтобы отправить этот запрос снова и пройти капчу")
#         if answer == "no":
#             raise Exception

#         await (await self.wait_for_element(page, 'xpath=//*[@id="btnArizaBildir"]')).click()
#         await context.close()

#     async def run_async(self):
#         phone_numbers = self.get_numbers(self.NUMBERS_FILE)
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=False)
#             while self.index < len(phone_numbers):
#                 self.progress_label.config(text=f"Отправка запроса {self.index + 1} из {len(phone_numbers)}...")
#                 try:
#                     await self.fill_fields(browser)
#                     self.index += 1
#                 except Exception as e:
#                     tkm.showerror("Ошибка", "Произошла ошибка, пробуем еще раз.")
#             await browser.close()
#             self.progress_label.config(text="Все запросы отправлены.")

#     def run_loop(self):
#         self.request_btn.config(state=tk.DISABLED)
#         threading.Thread(target=self.run_in_thread).start()

#     def run_in_thread(self):
#         asyncio.run(self.run_async())

# if __name__ == "__main__":
#     app = ComplaintSenderApp()
#     app.mainloop()

import sys
import asyncio
from playwright.async_api import async_playwright
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt

class ComplaintSenderApp(QWidget):
    update_progress_signal = pyqtSignal(str)
    captcha_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.index = 0
        self.NUMBERS_FILE = "phone_numbers.txt"
        self.PHRASES_FILE = "random_phrases.txt"
        self.captcha_event = asyncio.Event()
        self.initUI()
        self.update_progress_signal.connect(self.update_progress)
        self.captcha_signal.connect(self.show_captcha_dialog)

    def initUI(self):
        self.setWindowTitle('Complaint Sender')
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()

        self.info_label = QLabel("Нажмите старт, чтобы начать отправку запросов. Всего будет отправлено 4 запроса.", self)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        self.request_btn = QPushButton("Старт", self)
        self.request_btn.clicked.connect(self.run_loop)
        layout.addWidget(self.request_btn)

        self.progress_label = QLabel("", self)
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

    def get_numbers(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().split("\n")

    def get_phrases(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().split("\n")

    async def wait_for_element(self, page, selector):
        await page.wait_for_selector(selector)
        return await page.query_selector(selector)

    async def fill_fields(self, browser):
        phone_numbers = self.get_numbers(self.NUMBERS_FILE)
        phrases_list = self.get_phrases(self.PHRASES_FILE)

        # Инициализация новой страницы
        context = await browser.new_context()
        page = await context.new_page()

        # Открытие страницы для жалобы
        await page.goto("https://online.toroslaredas.com.tr/ariza-bildir")

        # Заполнение полей
        await (await self.wait_for_element(page, 'xpath=/html/body/div[6]/div/button[1]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="radio-ariza_tipi"]/div[3]/label')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[2]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-1-5"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[3]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-2-8"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[4]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-3-1"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[5]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-4-1"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[6]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-5-38"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="farkliAdresDiv"]/div/div[7]/div/button')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="bs-select-6-10"]')).click()
        await (await self.wait_for_element(page, 'xpath=//*[@id="binaNo"]')).fill("1")
        await (await self.wait_for_element(page, 'xpath=//*[@id="IslemDetay"]')).fill(random.choice(phrases_list))
        await (await self.wait_for_element(page, 'xpath=//*[@id="telefon"]')).fill(phone_numbers[self.index])

        if self.index > 1:
            await (await self.wait_for_element(page, 'xpath=//*[@id="arizaBildirmeForm"]/div[2]/div/div/div[7]/div[1]/div[2]/label')).click()

        self.update_progress_signal.emit("Пожалуйста, пройдите капчу.")
        self.captcha_event.clear()

        # Запуск диалогового окна для прохождения капчи
        self.captcha_signal.emit()

        # Ожидание прохождения капчи
        await self.captcha_event.wait()

        # Продолжение выполнения скрипта после прохождения капчи
        # await (await self.wait_for_element(page, 'xpath=//*[@id="btnArizaBildir"]')).click()
        await context.close()

    def update_progress(self, message):
        self.progress_label.setText(message)

    def show_captcha_dialog(self):
        self.captcha_dialog = CaptchaDialog(self)
        self.captcha_dialog.accepted.connect(self.on_captcha_accepted)
        self.captcha_dialog.rejected.connect(self.on_captcha_rejected)
        self.captcha_dialog.setWindowFlags(self.captcha_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.captcha_dialog.exec_()

    def on_captcha_accepted(self):
        self.captcha_event.set()

    def on_captcha_rejected(self):
        self.captcha_event.set()

    async def run_async(self):
        phone_numbers = self.get_numbers(self.NUMBERS_FILE)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            while self.index < len(phone_numbers):
                self.update_progress_signal.emit(f"Отправка запроса {self.index + 1} из {len(phone_numbers)}...")
                try:
                    await self.fill_fields(browser)
                    self.index += 1
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", "Произошла ошибка, пробуем еще раз.")
            await browser.close()
            self.update_progress_signal.emit("Все запросы отправлены.")

    def run_loop(self):
        self.request_btn.setEnabled(False)
        self.thread = AsyncRunner(self.run_async)
        self.thread.finished.connect(lambda: self.request_btn.setEnabled(True))
        self.thread.start()

class AsyncRunner(QThread):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro

    def run(self):
        asyncio.run(self.coro())

class CaptchaDialog(QDialog):
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Капча")
        self.setGeometry(100, 100, 300, 150)
        
        layout = QVBoxLayout()

        self.captcha_label = QLabel("У вас есть 20 секунд, чтобы пройти капчу.", self)
        layout.addWidget(self.captcha_label)

        self.confirm_button = QPushButton("Я прошел капчу", self)
        self.confirm_button.clicked.connect(self.accept_captcha)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

        # Запуск таймера на 20 секунд
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 20
        self.timer.start(1000)

    def update_timer(self):
        if self.time_left > 0:
            self.setWindowTitle(f"Капча (осталось {self.time_left} секунд)")
            self.time_left -= 1
        else:
            self.timer.stop()
            self.reject()

    def accept_captcha(self):
        self.timer.stop()
        self.accept()

    def accept(self):
        super().accept()
        self.accepted.emit()

    def reject(self):
        super().reject()
        self.rejected.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ComplaintSenderApp()
    window.show()
    sys.exit(app.exec_())
