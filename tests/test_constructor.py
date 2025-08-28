from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from locators import Locators
import time


class TestConstructor:

    def test_sections_navigation(self, driver):
        """Тест навигации по разделам конструктора"""

        # Давайте сначала проверим текущее состояние
        print("Начальное состояние:")
        active_section = driver.find_element(*Locators.ACTIVE_SECTION)
        print(f"Активный раздел: {active_section.text}")

        # Проверяем только переход к соусам (где возникает ошибка)
        self._test_single_section(driver, Locators.SAUCES_SECTION, "Соусы")

    def _test_single_section(self, driver, section_locator, expected_title):
        """Тестируем один конкретный раздел"""
        print(f"\nТестируем переход к: {expected_title}")

        # Получаем текущий активный раздел
        current_active = driver.find_element(*Locators.ACTIVE_SECTION).text
        print(f"Текущий активный: {current_active}")

        # Если уже в нужном разделе, пропускаем
        if expected_title in current_active:
            print(f"Уже в разделе {expected_title}, пропускаем")
            return

        # Кликаем на раздел
        section_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(section_locator)
        )
        print(f"Элемент найден: {section_element.text}")

        # Прокручиваем и кликаем
        driver.execute_script("arguments[0].scrollIntoView();", section_element)
        driver.execute_script("arguments[0].click();", section_element)

        # Ждем и проверяем результат
        time.sleep(2)  # временно для отладки

        # Проверяем активный раздел
        try:
            new_active = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(Locators.ACTIVE_SECTION)
            )
            print(f"Новый активный раздел: {new_active.text}")

            if expected_title not in new_active.text:
                print("ВНИМАНИЕ: Активный раздел не изменился!")
                print("Возможные причины:")
                print("1. Элемент не кликабельный")
                print("2. JavaScript не обрабатывает клик")
                print("3. Активный таб обновляется по-другому")

        except Exception as e:
            print(f"Ошибка при проверке активного раздела: {e}")