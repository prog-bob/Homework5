from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# открывает основную страницу и проверяет,
# что мы находимся именно на странице приложения.
def test_run_browser(browser, url):
    browser.get(url)
    # print(browser.title)
    # print(browser.current_url)
    assert browser.current_url == url
    print(browser.title)
    assert browser.title == "Your Store"


# тест Главной страницы приложения
def test_main_page(browser, url):
    browser.get(url)
    # наличие кнопки Search
    el = browser.find_element_by_xpath("//input[@name='search'][@type='text']")

    # количество выпадающих списков в меню навигации
    el = browser.find_elements_by_css_selector("ul.nav.navbar-nav li.dropdown")
    assert len(el) == 4, "Неверное количество элементов в меню навигации"

    # наличие кнопок dropdown-toggle
    browser.find_elements_by_class_name("dropdown-toggle")

    # наличие кнопки Корзина
    browser.find_element_by_id("cart")

    # наличие кнопки Корзина
    el = browser.find_elements_by_link_text("https://demo.opencart.com/index.php?route=product/product&product_id=40")


# тест Каталога
def test_catalog(browser, url):

    browser.get(url+"/index.php?route=product/category&path=20")

    # наличие кнопки Search
    el = browser.find_element_by_xpath("//input[@name='search'][@type='text']")

    # поиск iPhone
    el = browser.find_element_by_css_selector("input.form-control.input-lg")
    search_str = "iPhone"
    el.send_keys(search_str)
    el.send_keys(Keys.ENTER)
    sleep(1)
    browser.save_screenshot(search_str + ".png")
    browser.back()

    # количество Категорий с выпадающим списком
    el = browser.find_elements_by_css_selector("ul.nav.navbar-nav li.dropdown")
    assert len(el) == 4, "Неверное количество Категорий со списком"

    # количество элемента Currency
    el = browser.find_elements_by_id("form-currency")

    # сортировка товара
    el = browser.find_element_by_css_selector("select#input-sort.form-control")
    el.send_keys(Keys.ARROW_DOWN)
    el.send_keys(Keys.ENTER)
    # поиск кнопки Закладки
    browser.find_element_by_id("wishlist-total")

    # количество товаров на текущей странице
    el = browser.find_elements_by_class_name("product-layout")
    assert len(el) == 12
    # print(f"len(el) = {len(el)}")


# тест Карточки товара
def test_product(browser, url):

    browser.get(url+"/index.php?route=product/product&path=57&product_id=49")

    # наличие описания товара
    el = browser.find_element_by_xpath("//div[@id='tab-description']")

    # наличие в описании товара сведений о телефоне
    content = "Samsung Galaxy Tab 10.1"
    assert el.text.count(content) > 0

    # Наличие кнопки Добавить товар
    el = browser.find_element_by_xpath("//button[@id='button-cart']")

    # Добавить 2 телефона в корзину
    el = browser.find_element_by_css_selector("input#input-quantity.form-control")
    product_cnt = "2"
    el.send_keys(product_cnt)
    el.send_keys(Keys.ENTER)

    # наличие кнопки Корзина
    browser.find_element_by_id("cart")


# тест Страницы логина
def test_login(browser, url):

    browser.get(url+"/index.php?route=account/login")

    # Наличие кнопки E-Mail Address
    email_btn = browser.find_element_by_xpath("//input[@id='input-email']")

    # Наличие кнопки Password
    password_btn = browser.find_element_by_xpath("//input[@id='input-password']")

    # Наличие кнопки Login
    login_btn = browser.find_element_by_xpath("//input[@class='btn btn-primary']")

    credentials = {"fake_email": "demo@mail.ru", "fake_password": "demo"}

    # Логиирование
    email_btn.clear()
    email_btn.send_keys(credentials["fake_email"])
    password_btn.clear()
    password_btn.send_keys(credentials["fake_password"])
    login_btn.send_keys(Keys.ENTER)

    # sleep(5)
    timeout = 5
    text = "Change your password"
    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, text)))

    # Наличие ссылки "Change your password"
    assert browser.find_element_by_link_text(text)


# тест Страницы логина
def test_admin_login(browser, url):

    browser.get(url+"/admin/")

    # Наличие кнопки Username
    email_btn = browser.find_element_by_xpath("//input[@id='input-username']")

    # Наличие кнопки Password
    password_btn = browser.find_element_by_xpath("//input[@id='input-password']")

    # Наличие кнопки Login
    login_btn = browser.find_element_by_xpath("//button[@class='btn btn-primary']")

    credentials = {"fake_email": "demo@mail.ru", "fake_password": "demo"}

    # Логиирование
    email_btn.clear()
    email_btn.send_keys(credentials["fake_email"])
    password_btn.clear()
    password_btn.send_keys(credentials["fake_password"])
    login_btn.send_keys(Keys.ENTER)

    # sleep(5)
    timeout = 5

    # Проверка логина раздела
    login_xpath = "//li[@class='dropdown']/a[@class='dropdown-toggle'][@href='#']"
    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, login_xpath)))
    link_profile = browser.find_element_by_xpath(login_xpath)
    link_profile.click()

    # Проверка разлогина раздела
    logout_xpath = "//a[contains(@href,'logout&user_token')]"
    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, logout_xpath)))
    link_logout = browser.find_element_by_xpath(logout_xpath)
    link_logout.click()

    browser.find_element_by_xpath("//input[@id='input-username']")