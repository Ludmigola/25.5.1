
import pytest
import uuid

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# добавм имя и пароль для входа
from settings import valid_password, valid_username


@pytest.fixture
def chrome_options(chrome_options):
    #chrome_options.binary_location = '../web-drivers/chromedriver_win32/chromedriver.exe'
    #chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    #chrome_options.add_argument('--headless')
    return chrome_options


@pytest.fixture
def driver_args():
    return ['--log-level=ALL']



@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    browser.get("https://petfriends.skillfactory.ru/")

    # дождемся появления кнопки и нажмем
    btn_newuser = WebDriverWait(browser, timeout=3).until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")))
    btn_newuser.click()
    
    # Дождемся следующей кнопки, чтоб указать логин и пароль
    btn_exist_acc = WebDriverWait(browser, timeout=3).until(EC.element_to_be_clickable((By.LINK_TEXT, u"У меня уже есть аккаунт")))
    btn_exist_acc.click()


    # ждем поле ввода логина
    field_email = WebDriverWait(browser, timeout=3).until(EC.presence_of_element_located((By.ID, "email")))
    field_email.clear()
    field_email.send_keys(valid_username)
    
    # теперь ждем поле ввода пароля
    field_pass = WebDriverWait(browser, timeout=3).until(EC.presence_of_element_located((By.ID, "pass")))
    field_pass.clear()
    field_pass.send_keys(valid_password)
    
    # ожидаем кнопку для отправки логина и пароля
    btn_submit = WebDriverWait(browser, timeout=3).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    btn_submit.click()

    # проверим, что мы зашли на страницу с правильными логином и паролем
    assert browser.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"

    # перейдем к "Мои питомцы" после ожидания
    my_pets_link = WebDriverWait(browser, timeout=3).until(EC.element_to_be_clickable((By.LINK_TEXT, u"Мои питомцы")))
    my_pets_link.click()

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here