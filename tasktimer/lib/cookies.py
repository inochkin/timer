import json
from typing import Union
from streamlit_javascript import st_javascript
from lib.static import COOKIE_TASK_END_DATETIME, COOKIE_TASK_START_DATETIME, \
    COOKIE_HOURS_MINUTES, COOKIE_DESC, COOKIE_PRIORITY, USER_NAME, USER_EMAIL, USER_ID, USER_AUTH_DATA_ENCRYPTED, \
    COOKIE_TASK_IS_CREATED
from cryptography.fernet import Fernet

# -- encrypt
key_session = b'wVXBaBRl-PVU78CuCNUTYZt3uG1nnJxUVkgApOD_B8o='
cipher = Fernet(key_session)


"""
Особенность st_javascript пакета.
st_javascript() - созлается веб элемент который должен иметь уникальный ключ.
если ключ не уникальный падает еррор.
Если генерировать случайные ключи для st_javascript() то будет циключеское зависание,\
т.к. на каждое изменение strimlit делает запрос.

"""



def run_st_javascript(js_code: str, key_element_js: str):
    # print('>>>>> unique_key =', key_element_js)
    return st_javascript(js_code, key=key_element_js)


def set_cookie(key: str, value: str, key_element_js: str, age: int = (3600 * 168)):  # 1 week
    run_st_javascript(f'document.cookie = "{key}={value}; path=/; max-age={age}"', key_element_js)


def _get_all_cookies(key_element_js: str) -> dict:
    all_cookies_str = run_st_javascript("document.cookie", key_element_js)
    dict_cookies = {}
    if all_cookies_str:
        for item in all_cookies_str.split("; "):
            if "=" in item:
                key, value = item.split("=", 1)  # разделяем по 1 знаку =. т.к. значение может содержать =.
                dict_cookies[key] = value
    return dict_cookies


def get_cookie(key_get: str, key_element_js: str):
    dict_cookies = _get_all_cookies(key_element_js)
    if dict_cookies:
        try:
            # print('!!!! >>>> dict_cookies =', dict_cookies)
            value = dict_cookies[key_get]
        except KeyError:
            value = ''

        # print('>>> get value =', value)
        return value
    else:
        return ''


def get_list_cookies(list_keys_cookies: list, key_element_js: str) -> list:
    dict_cookies = _get_all_cookies(key_element_js)
    list_result = []
    for keys_cookie in list_keys_cookies:
        try:
            value = dict_cookies[keys_cookie]
            list_result.append(value)
            # print(' >>>> value =', value)
        except KeyError:
            value = ''
    return list_result


def delete_cookie(key: str, key_element_js: str):
    run_st_javascript(f'document.cookie = "{key}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"', key_element_js)


# --------------- save task
def get_cookies_task_values_and_clear_cookies():
    # need get list of cookies by one request.
    list_key_cookies = [COOKIE_HOURS_MINUTES,
                        COOKIE_DESC,
                        COOKIE_PRIORITY,
                        COOKIE_TASK_START_DATETIME,
                        COOKIE_TASK_END_DATETIME,
                        COOKIE_TASK_IS_CREATED]
    cookies_values = get_list_cookies(list_key_cookies, '1')
    len_cookies_values = len(cookies_values)

    if len_cookies_values == 6:
        (hours_minutes, desc, priority, task_start_datetime,
         task_end_datetime, task_is_created) = cookies_values
        # print('>>>> ', hours_minutes, desc, task_start_datetime, priority, task_end_datetime)

        # need date only one cookie status.
        delete_cookie(COOKIE_TASK_IS_CREATED, '6')

        if task_is_created == '1':
            return hours_minutes, desc, priority, task_start_datetime, task_end_datetime


# ----------------- user auth

def save_cookies_user_creds_encrypted(username: str, email: str, user_id: str):
    cookie_data = {USER_NAME: f'{username}',
                   USER_EMAIL: f'{email}',
                   USER_ID: f'{user_id}'}

    encrypted_data = cipher.encrypt(json.dumps(cookie_data).encode())
    encrypted_data = encrypted_data.decode("utf-8")  # Сохраняем как строку
    set_cookie(USER_AUTH_DATA_ENCRYPTED, encrypted_data, '11')


def check_cookie_user_is_authorised() -> Union[tuple[str, str, str], False]:
    user_auth_cookie_encrypted = get_cookie(USER_AUTH_DATA_ENCRYPTED, '12')
    if not user_auth_cookie_encrypted:
        # if no cookie key.
        return False
    try:
        # print('>>> check_user_is_authorised try')
        decrypted_data = cipher.decrypt(user_auth_cookie_encrypted.encode()).decode()
        user_data = json.loads(decrypted_data)

        return (user_data[USER_NAME],
                user_data[USER_EMAIL],
                user_data[USER_ID])
    except Exception:
        # print('>>> check_user_is_authorised Exception')
        # if decrypt is wrong.
        return False


