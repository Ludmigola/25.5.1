"""
Написать тест, который проверяет, что на странице http://petfriends.skillfactory.ru/my_pets со списком питомцев пользователя:

1. Присутствуют все питомцы.
2. Хотя бы у половины питомцев есть фото.
3. У всех питомцев есть имя, возраст и порода.
4. У всех питомцев разные имена.
5. В списке нет повторяющихся питомцев. (Сложное задание).

Дополнительно:

В написанном тесте (проверка карточек питомцев) добавьте неявные ожидания всех элементов (фото, имя питомца, его возраст).
В написанном тесте (проверка таблицы питомцев) добавьте явные ожидания элементов страницы.

"""

"""
python -m pytest -s -v --driver Chrome
--driver-path <chromedriver_directory>/chromedriver test_selenium_petfriends.py
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def test_number_of_pets(web_browser):
    '''
    функция проверяет количество питомцев указанных в статистеке пользователя и сравнивает с количеством записей в таблице 
    '''

    # прочтем значение всех питомцев
    web_browser.implicitly_wait(2)
    my_all_pets = web_browser.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    my_all_pets = my_all_pets.text.split('\n')[1].split(':')[1]

    # найдем количество записей в таблице
    web_browser.implicitly_wait(1)
    shown_pets = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # количество найденых записей соответсвует количеству всех питоцмев полученных ранее
    assert int(my_all_pets) == len(shown_pets)


def test_at_least_half_images_present(web_browser):
    '''
    хотя бы у половины есть 
    '''

    # найдем все элементы с изображениями
    web_browser.implicitly_wait(1)
    all_images = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img')

    # теперь составим список только с непустыми изображениями   
    valid_images = [element for element in all_images if element.get_attribute('src') != '' ]

    # количество непустых изображений должно быть больше или равно половине списка всех питомцев
    assert len(valid_images) >= len(all_images) / 2



def test_all_pets_have_data(web_browser):
    '''
    у всех питомцев есть имя, порода и возраст
    '''

    # теперь соберем имена, породы и возраст всех питомцев
    # сначала имена
    web_browser.implicitly_wait(1)
    names = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')  

    #  затем порода
    web_browser.implicitly_wait(1)
    breeds = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]')

    # и возраст
    web_browser.implicitly_wait(1)
    ages = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]')

    # У всех питомцев есть имя, возраст и порода
    for i in range(len(names)):
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''


def test_all_names_different(web_browser):
    '''
    у всех питомцев разные имена
    '''

    web_browser.implicitly_wait(1)
    names = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')

    # для каждого имени проверим количество повторений
    all_names = [name.text for name in names]
    unique_names = {name.text for name in names}
    # если количество уникальных имен равно коичеству всех то все верно
    assert len(unique_names) == len(all_names)
    

def test_unique_pets(web_browser):
    '''
    в списке нет повторяющихся питомцев
    '''

    web_browser.implicitly_wait(1)
    shown_pets = web_browser.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # уберем питомцев с одиннаковыми именами с использованием множества, исключающего повторение элеменов
    unique_pets = {pet.text for pet in shown_pets}

    # сравним количество элементов множества с количество элементов списка чтоб изнать есть ли повторяющиеся
    assert len(unique_pets) == len(shown_pets)
