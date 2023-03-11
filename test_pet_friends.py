from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Получаем api ключ и сохраняем в переменную auth_key. Используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Igor', animal_type='horse', age='4', pet_photo='images/111.jpg'):
    """Проверяем возможность добавления питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Малыш', 'слон', '3', 'images/222.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()
def test_successful_update_self_pet_info(name='GoGo', animal_type='mare', age='5'):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert  result['name'] == name
    else:
        raise Exception('There is no my pets')
def test_create_pet_simple(name='Малыш', animal_type='слон', age='6'):
    """Проверяем, что можно добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name,animal_type, age)
    assert status == 200
    assert result['name'] == name
def test_add_new_pet_no_data(name='', animal_type='', age=''):
    """Проверка с негативным сценарием. Проверяем, что можно добавить питомца с пустыми данными в поле имя, тип животного и возраст"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert  result['name'] == name
def test_get_api_key_for_data_user_empty(email='', password=''):
    """ Проверка с негативным сценарием. Проверяем что запрос api ключа c пустыми значениями логина и пароля возвращает статус 403
    и в результате не содержится слово key """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
def test_add_pet_invalid_age(name='Kuzma', animal_type='dog', age='2345'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert  result['age'] == age
    number = result['age']

def test_get_api_key_invalid_email(email=invalid_email, password=valid_email):
    '''Проверяем запрос с невалидным емейлом и с валидным паролем.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
def test_get_api_key_invalid_password(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
def test_add_pet_number_animal_type(name='Kuzma', animal_type='739757', age='5'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в поле animal_type.'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200

