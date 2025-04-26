import asyncio
from playwright.async_api import async_playwright, Playwright
import random
import time
from urllib.parse import urlparse

# Функция для короткой задержки при прогрузке интерфейса
def short_random_sleep():
    time.sleep(random.uniform(0.5, 2))

# Функция для задержки с таймером
def countdown_sleep(min_seconds=60, max_seconds=180):
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Ожидание следующего профиля: {int(delay)} секунд")
    while delay > 0:
        print(f"Осталось: {int(delay)} секунд", end="\r")
        time.sleep(1)
        delay -= 1
    print("Ожидание завершено, продолжаем...")

# Функция для парсинга прокси-строки
def parse_proxy(proxy_str):
    # Формат: http://username:password@host:port
    if not proxy_str:
        return None
    parsed = urlparse(proxy_str)
    if not parsed.scheme or not parsed.hostname or not parsed.port:
        raise ValueError(f"Некорректный формат прокси: {proxy_str}")
    return {
        "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
        "username": parsed.username or "",
        "password": parsed.password or ""
    }

# Основная функция для регистрации
async def register_email(playwright: Playwright, email: str, proxy_str: str):
    try:
        # Парсинг прокси
        proxy_config = parse_proxy(proxy_str) if proxy_str else None

        # Запуск браузера с прокси
        browser = await playwright.chromium.launch(
            headless=False,
            proxy=proxy_config
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # Переход на сайт
        await page.goto("https://pingnetwork.io/#waitlist")
        short_random_sleep()

        # Нажатие на кнопку "Join waitlist"
        await page.locator("a.tn-atom[href='#waitlist'][role='button']:has-text('Join waitlist')").first.click()
        short_random_sleep()

        # Ожидание загрузки формы
        await page.wait_for_selector("div[data-elem-id='1738779213397'] input[placeholder='Email']", timeout=30000)
        short_random_sleep()

        # Заполнение формы
        await page.locator("div[data-elem-id='1738779213397'] input[placeholder='Email']").fill(email)
        short_random_sleep()

        # Нажатие кнопки "Join"
        await page.locator("div[data-elem-id='1738779213397'] button.t-submit:has-text('Join')").click()
        short_random_sleep()

        # Проверка сообщения об успехе
        await page.wait_for_selector("div.tn-atom[field='tn_text_1738779069122']:has-text('Thanks for joining the waitlist')", timeout=30000)
        short_random_sleep()

        print(f"[{email}] Регистрация успешна")
        await browser.close()
        return True
    except Exception as e:
        print(f"[{email}] Ошибка: {e}")
        return False
    finally:
        await browser.close()

# Функция для обработки списка емейлов и прокси
async def process_emails(email_file, proxy_file):
    # Чтение списка емейлов
    try:
        with open(email_file, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f.readlines() if line.strip()]
        print(f"Загружено {len(emails)} email-адресов")
    except Exception as e:
        print(f"Ошибка чтения файла {email_file}: {e}")
        return

    # Чтение списка прокси
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        print(f"Загружено {len(proxies)} прокси")
    except Exception as e:
        print(f"Ошибка чтения файла {proxy_file}: {e}")
        return

    # Проверка, что списки не пусты
    if not emails or not proxies:
        print("Ошибка: один из файлов пуст или не содержит данных")
        return

    # Запуск Playwright
    async with async_playwright() as playwright:
        proxy_index = 0
        for email in emails:
            try:
                proxy_str = proxies[proxy_index % len(proxies)]  # Циклический выбор прокси
                print(f"Обрабатывается email: {email}, прокси: {proxy_str}")
                proxy_index += 1

                success = await register_email(playwright, email, proxy_str)
                if not success:
                    print(f"[{email}] Ошибка регистрации")
                
                # Задержка с таймером между профилями
                countdown_sleep(60, 180)
            except Exception as e:
                print(f"Ошибка в цикле обработки для {email}: {e}")
                continue  # Продолжаем с следующим email

# Запуск программы
if __name__ == "__main__":
    asyncio.run(process_emails('emails.txt', 'proxies.txt'))