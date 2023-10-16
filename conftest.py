from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pytest

driver = webdriver.Chrome(executable_path="C:/Users/Виталий/PycharmProjects/Driver/chromedriver.exe")

@pytest.fixture(autouse=True, scope="session")
def testing():
    '''Вход на страницу Мои питомцы - один раз на всю сессию'''
    pytest.driver = webdriver.Chrome('C:/Users/Виталий/PycharmProjects/Driver/chromedriver.exe')

    # активируем неявное ожидание
    pytest.driver.implicitly_wait(10)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    # Очищаем поле и вводим email
    field_email = pytest.driver.find_element(By.ID, 'email')
    field_email.clear()
    field_email.send_keys(valid_email)

    # Очищаем поле и вводим пароль
    field_pass = pytest.driver.find_element(By.ID, 'pass')
    field_pass.clear()
    field_pass.send_keys(valid_password)
    time.sleep(2)

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Проверяем, что находимся на главной странице пользователя
    if not pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        pytest.driver.quit()
        raise Exception("Некорректный email или пароль")

    # Нажимаем на ссылку "Мои питомцы"
    # pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    pytest.driver.find_element(By.XPATH, '//*[@href="/my_pets"]').click()

    # Проверяем, что перешли на страницу "Мои питомцы"
    if not pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets':
        pytest.driver.quit()
        raise Exception("Это не страница Мои питомцы")

    yield

    pytest.driver.quit()