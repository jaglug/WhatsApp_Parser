from selenium import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re

# Функция для преобразования HTML файла. "Я запускаюсь под конец"
def converter(name):
    # Открываем HTML-файл
    with open(f'C:\\WhatsApp\\pages\\page_source_{name}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Находим все теги <img> с атрибутом crossorigin и удаляем их
    for img_tag in soup.find_all('img', {'crossorigin': True}):
        img_tag.decompose()

    for img_tag in soup.find_all('img', {'src': lambda x: x and x.startswith('blob')}):
        img_tag.decompose()

    for div_tag in soup.find_all('div', {'aria-label': 'Открыть изображение'}):
        div_tag.decompose()

    for div_tag in soup.find_all('div', {'role': 'button'}):
        div_tag.decompose()

    for div_tag in soup.find_all('div', {'class': '_38vwC yTWyz'}):
        div_tag.decompose()

    for div_tag in soup.find_all('svg', {'fill': 'none'}):
        div_tag.decompose()

    for div_tag in soup.find_all('canvas', {'draggable': 'false'}):
        div_tag.decompose()

    # Находим все теги span с атрибутом data-icon="tail-out"
    for span_tag in soup.find_all('span', {'data-icon': 'tail-out'}):
        # Создаем новый тег p с текстом "ВЫ"
        new_p_tag = soup.new_tag('p')
        new_p_tag.string = 'ВЫ'

        # Добавляем стили к новому тегу p
        new_p_tag['style'] = 'color: green; font-size: 20px; font-weight:700'

        # Заменяем тег <span> на новый тег p
        span_tag.replace_with(new_p_tag)

    for span_tag in soup.find_all('span', {'data-icon': 'tail-in'}):
        # Создаем новый тег p с текстом "ВЫ"
        new_p_tag = soup.new_tag('p')
        new_p_tag.string = 'ВАМ'

        # Добавляем стили к новому тегу p
        new_p_tag['style'] = 'color: red; font-size: 20px; font-weight:700'

        # Заменяем тег span на новый тег p
        span_tag.replace_with(new_p_tag)

    for span_tag in soup.find_all('span', class_='_11JPr'):
        # Добавляем стили к найденному тегу span
        if 'style' in span_tag.attrs:
            span_tag['style'] += 'font-size: 20px; color: blue;'
        else:
            span_tag['style'] = 'font-size: 20px; color: blue;'

    for span_tag in soup.select('span._11JPr:not([class*=" "])'):
        # Добавляем стили к найденному тегу span
        if 'style' in span_tag.attrs:
            span_tag['style'] += 'font-size: 30px; color: brown;'
        else:
            span_tag['style'] = 'font-size: 30px; color: brown;'

    # Записываем измененный HTML обратно в файл
    with open(f'C:\\WhatsApp\\Диалог_{name}.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

# Параметры для запуска браузера
# Список прокси, если используется
#PROXY_LIST = ["127.0.0.1:1080", "127.0.0.1:1081"]
#PROXY = random.choice(PROXY_LIST)
# Рандомный useragent, можно отключить, так как браузер может запуститься с useragent, который не поддерживает whatsapp
useragent = UserAgent()
options = webdriver.ChromeOptions()
#Если убираем Useragent, то и удаляем строку внизу
options.add_argument(f"user-agent=useragent={useragent.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
#options.add_argument("--headless")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")
#options.add_argument(f"--proxy-server=socks5://{PROXY}")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  #  interactive

# Путь к браузеру
s=Service(executable_path=r"C:\\Projects\\WhatsApp1\\WhatsApp\\chromedriver.exe")
driver = webdriver.Chrome(service=s,
                    options=options)
# Открываем сайт whaysapp
driver.get('https://web.whatsapp.com/')
# Ожидание для сканрования QR-кода и загрузки профиля
time.sleep(20)

# Если появился данный элемент, то выводим сообщения
try:
    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Список чатов"]'))
    )
    print('Авторизация прошла успешно')
except:print('Не удалось авторизоваться')

all_chats = []
try:
    # Инициализируем начальные значения
    last_translateY = 0

    while True:
        # Ищем элементы с текущим значением translateY
        chats = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="x10l6tqk xh8yej3 x1g42fcv"][role="listitem"][style*="translateY(' + str(last_translateY) + 'px"]'))
        )
        # Пока есть новые чаты
        if chats:
            print('Нашли чаты')
            for chat in chats:
                # scope = chat.find_element(By.CSS_SELECTOR, '[class="p357zi0d r15c9g6i"]')
                # spans = scope.find_elements(By.CSS_SELECTOR, 'span')
                # has_colon = any(': ' in span.text for span in spans)
                chat.click()
                # Определяем это группа или обычный чат
                header_first= WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="_amid"]'))
                        )
                header_first.click()
                time.sleep(1)
                is_group= WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class="enbbiyaj e1gr2w1z hp667wtd"]'))
                        )
                group_text=is_group.text
                close_elem_first= WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="button"][aria-label="Закрыть"]'))
                                )
                close_elem_first.click()
                if 'Группа' in group_text:
                    #Если это группа
                    print('Это группа')
                    # chat.click()
                    div=driver.find_element(By.CSS_SELECTOR, '[id="main"]')
                    name=div.find_element(By.CSS_SELECTOR,'span[dir="auto"][class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr"]').text
                    print(name)
                    time.sleep(20)
                    header= WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[class="AmmtE"]'))
                        )
                    header.click()
                    try:
                        #Если группа большая
                        show_all_button= WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[class="ggj6brxn ljrqcn24 jq3rn4u7"]'))
                            )
                        show_all_button.click()
                        time.sleep(2)
                        last_translateY_members = 0
                        # Обнуляем списки
                        all_members=[]
                        all_spans=[]
                        all_numbers=[]
                        valid_numbers=[]
                        valid_spans=[]
                        try:
                            div_to_scroll = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, '[class="g6kkip0l p357zi0d f8m0rgwh ppled2lx tkdu00h0 gfz4du6o r7fjleex jv8uhy2r lhggkp7q qq0sjtgm ln8gz9je _3cjY2 copyable-area"]'))
                            )
                            # Прокрутка окна с участниками группы, пока они есть
                            while True:
                                try:
                                    chat_members = div_to_scroll.find_element(By.CSS_SELECTOR, '[role="listitem"][style*="translateY(' + str(last_translateY_members) + 'px"]')
                                    if chat_members:
                                        # all_members.extend(chat_members)
                                        last_member = chat_members
                                        last_translateY_members += 72
                                        try:
                                            driver.execute_script("arguments[0].scrollIntoView();", last_member)
                                            print('Идет прокрутка участников группы')
                                        except:
                                            print('Прокрутка не работает')
                                        try:
                                        # Ищем тег span с номерами телефонов
                                            div_span=chat_members.find_elements(By.CSS_SELECTOR,'div[role="gridcell"][class="Dvjym"]')
                                            for i in div_span:
                                                text = i.find_elements(By.CSS_SELECTOR, 'span[class="_2h0YP"]')
                                                all_spans.append(text.text)
                                                print(text.text)
                                        except:
                                            print('Тег не найден')
                                        try:
                                        # Ищем тег span с номерами телефонов
                                            numbers = chat_members.find_elements(By.CSS_SELECTOR,'div[role="gridcell"][aria-colindex="2"][class="y_sn4"]')
                                            for i in numbers:
                                                print(i.text)
                                                all_numbers.append(i.text)
                                        except:
                                            print('Тег не найден')

                                    else:
                                        break
                                except:
                                    print('Больше нет элементов')
                                    break
                            # try:
                            #     # Ищем тег span с номерами телефонов
                            #     div_span=driver.find_elements(By.CSS_SELECTOR,'div[role="gridcell"][class="Dvjym"]')
                            #     for i in div_span:
                            #         text = i.find_elements(By.CSS_SELECTOR, 'span[class="_2h0YP"]')
                            #         all_spans.append(text.text)
                            #         print(text.text)
                            # except:
                            #     print('Тег не найден')
                            # try:
                            #     # Ищем тег span с номерами телефонов
                            #     numbers = driver.find_elements(By.CSS_SELECTOR,'div[role="gridcell"][aria-colindex="2"][class="y_sn4"]')
                            #     for i in numbers:
                            #         print(i.text)
                            #         all_numbers.append(i.text)
                            # except:
                                # print('Тег не найден')
                            # Открываем файл для записи участников группы
                            phone_pattern = re.compile(r'^\+\d')

                            # Фильтруем тексты, оставляем только те, которые соответствуют шаблону
                            valid_spans = [span for span in all_spans if phone_pattern.match(span)] 
                            valid_numbers = [span for span in all_numbers if phone_pattern.match(span)] 
                            with open(f'C:\\WhatsApp\\Участники группы_{name}.txt', 'w', encoding='utf-8') as file:
                                for i in valid_spans:
                                    file.write(i+'\n')
                            file.close()
                            with open(f'C:\\WhatsApp\\Участники группы_{name}.txt', 'a', encoding='utf-8') as file:
                                for i in valid_numbers:
                                    file.write(i+'\n')
                            file.close()
                            # Закрываем лишние окна
                            close_elem= WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="x"]'))
                            )
                            close_elem.click()
                            time.sleep(1)
                            try:
                                close_elem_2= WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="button"][aria-label="Закрыть"]'))
                                )
                                close_elem_2.click()
                                time.sleep(1)
                            except Exception as e:
                                print(e)
                                time.sleep(1)
                        except Exception as e:
                            print(f'Ошибка: {e}')
                            time.sleep(1)

                    except:
                            #Если группа маленькая
                            # Обнуляем списки
                            all_members=[]
                            all_spans=[]
                            all_numbers=[]
                            valid_numbers=[]
                            valid_spans=[]
                            try:
                                # Ищем кнопку со стрелкой вниз
                                show_all_button= WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-icon="down"]'))
                                    )
                                show_all_button.click()
                            except:
                                # Если не нашли, то ничего не делаем
                                pass
                            # Ищем теги span с номерами телефонов
                            div_num=driver.find_element(By.CSS_SELECTOR,'div[class="tt8xd2xn dl6j7rsh mpdn4nr2 avk8rzj1"]')
                            list_of_spans=div_num.find_elements(By.CSS_SELECTOR, 'span[dir="auto"][style="min-height: 0px;"][aria-label][class="_11JPr"]')
                            for i in list_of_spans:
                                all_spans.append(i.text)
                            try:
                                # Ищем теги span с номерами телефонов
                                div_num=driver.find_element(By.CSS_SELECTOR,'div[class="tt8xd2xn dl6j7rsh mpdn4nr2 avk8rzj1"]')
                                numbers = div_num.find_elements(By.CSS_SELECTOR,'div[role="gridcell"][aria-colindex="2"][class="y_sn4"]')
                                for i in numbers:
                                    print(i.text)
                                    all_numbers.append(i.text)
                            except:
                                print('Тег не найден')
                            # Записываем номера в файл
                            phone_pattern = re.compile(r'^\+\d')
                            valid_numbers = [span for span in all_numbers if phone_pattern.match(span)] 
                            valid_spans = [span for span in all_spans if phone_pattern.match(span)] 
                            with open(f'C:\\WhatsApp\\Участники группы_{name}.txt', 'w', encoding='utf-8') as file:
                                for list in valid_spans:
                                    file.write(list + '\n')
                            file.close()
                            with open(f'C:\\WhatsApp\\Участники группы_{name}.txt', 'a', encoding='utf-8') as file:
                                for list in valid_numbers:
                                    file.write(list + '\n')
                            file.close()
                            
                            close_elem= WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="button"][aria-label="Закрыть"]'))
                                )
                            close_elem.click()
                            time.sleep(1)


                    # Начинаем прокрутку страницы вверх
                    div=driver.find_element(By.CSS_SELECTOR, '[id="main"]')
                    time.sleep(1)
                    # Здесь b означает количество прокруток, 1 прокрутка примерно 5-10 сообщений
                    a=0
                    b=30
                    num=1
                    executed=False
                    while a<b:
                        try:
                            # Ждем, пока все диалоги не будут присутствовать
                            dialogs = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="UzMP7 _1uv-a _3m5cz"]'))
                            )
                            if dialogs:
                                # Прокручиваем к первому диалогу
                                first_dialog = dialogs[0]
                                driver.find_element(By.CSS_SELECTOR, '[class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]').send_keys(Keys.HOME)
                                print('Прокрутка чата вверх')
                                # Ожидание пока прогрузятся новые сообщения
                                time.sleep(0.5)
                                a+=1
                            else:
                                break
                        except Exception as e:
                            print(f"Произошла ошибка: {str(e)}")
                            break
                else:
                    # Если обычный чат
                        # chat.click()
                        time.sleep(30)
                        # Если все таки обычный сайт
                        print('Обычный чат')
                        div=driver.find_element(By.CSS_SELECTOR, '[id="main"]')
                        name=div.find_element(By.CSS_SELECTOR,'[class="ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr"]').text
                        print(name)
                        time.sleep(1)
                        a=0
                        b=30
                        num=1
                        executed=False
                        while a<b:
                            try:
                                # Ждем, пока все диалоги не будут присутствовать
                                dialogs = WebDriverWait(driver, 10).until(
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="UzMP7 _1uv-a _3m5cz"]'))
                                )
                                if dialogs:
                                    # Прокручиваем к первому диалогу
                                    first_dialog = dialogs[0]
                                    driver.find_element(By.CSS_SELECTOR, '[class="n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]').send_keys(Keys.HOME)
                                    print('Прокрутка чата вверх')
                                    # Ожидание пока прогрузятся новые сообщения
                                    time.sleep(0.5)
                                    a+=1
                                else:
                                    break
                            except Exception as e:
                                print(f"Произошла ошибка: {str(e)}")
                                # Прерывание бессконесного цикла, когда уже нет новых элементов
                                break
            # Java script для получения содержимого блока с перепиской
            div_content = driver.execute_script("return document.getElementById('main').innerHTML;")
            with open(f'C:\\WhatsApp\\pages\\page_source_{name}.html', 'w', encoding='utf-8') as file:
                file.write(div_content)

            all_chats.extend(chats)
            last_chat = chats[-1]

            # Получаем значение translateY последнего элемента и прибавляем 72px
            last_translateY += 72

            # Прокручиваем страницу, чтобы появился новый элемент
            driver.execute_script("arguments[0].scrollIntoView();", last_chat)

            # Вызываем функци convertert, для редактирования файла HTML
            converter(name=name)
        else:
            break  # Прерываем цикл, если больше нет новых элементов
except Exception as e:

    print('Ошибка:', e)

driver.close()