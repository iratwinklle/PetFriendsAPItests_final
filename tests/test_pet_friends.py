import os
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

class TestPetFriends:
    def setup(self):
        self.pet = PetFriends


def test_get_api_key_correctly(email = valid_email, password = valid_password):
    '''Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list_pets_valid(filter=''):
    '''Проверяем что запрос всех питомцев возвращает список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' '''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_new_pets_correctly(name='Document', animal_type='dog', age='3', pet_photo='images\kit.jpg'):
    '''Проверяем, что можно создать карточку питомца с корректными данными'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pets(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_delete_pet_successfully():
    '''Проверяем, что можно удалить существующую карточку питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_new_pets(auth_key, "Суперкот", "кот", "3", "images/oto.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_put_update_pet_info_correctly(name='Change', animal_type='cat', age='5'):
    '''Проверяем возможность внесения изменений в существующую карточку питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][-1]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pet')

#Homework 19.7.2

def test_negative_get_api_key_with_incorrect_password(email = valid_email, password = '12345'):
    '''Проверяем возможность получения API ключа при условии ввода неправильного пароля'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result

def test_negative_get_api_key_with_incorrect_email(email = 'invalid_email@mail.ru', password = valid_password):
    '''Проверяем возможность получения API ключа при условии ввода несуществующего email'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result

def test_negative_get_api_key_with_empty_email_password(email = '', password = ''):
    '''Проверяем возможность получения API ключа при условии ввода пустных значений email и пароль'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'This user wasn&#x27;t found in database' in result

def test_negative_get_list_pets_with_invalid_auth_key(filter=''):
    '''Проверяем возможность получение списка питомцев при вводе неверного API ключа'''
    _, _ = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': '12345'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result

def test_negative_get_list_pets_with_empty_auth_key(filter=''):
    '''Проверяем возможность получение списка питомцев при вводе пустого значения API ключа'''
    _, _ = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result


def test_negative_post_add_new_pets_with_invalid_auth_key(name='Документ', animal_type='dog',
                                                          age='1', pet_photo = 'images/oto.jpg'):
    '''Проверяем возможность создания карточки нового питомца при вводе неверного API ключа'''
    _, _ = pf.get_api_key(valid_email, valid_password)
    auth_key = {'key': '12345'}
    status, result = pf.post_add_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result

def test_negative_delete_pet_with_invalid_auth_key():
    '''Проверяем возможность удаления существующей карточки  питомца при вводе неверного API ключа'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][-1]['id']
    auth_key_wrong = {'key': '12345'}
    status, result = pf.delete_pet(auth_key_wrong, pet_id)

    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result

def test_negative_put_update_pet_info_with_invalid_auth_key(name='Change', animal_type='cat', age='5'):
    '''Проверяем возможность внесения изменений в карточку существующего питомца при вводе неверного API ключа'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key_wrong = {'key': '12345'}
    status, result = pf.put_update_pet_info(auth_key_wrong, my_pets['pets'][-1]['id'], name, animal_type, age)
    assert status == 403
    assert 'Please provide &#x27;auth_key&#x27; Header' in result


def test_negative_post_add_new_pets_with_incorrect_file_of_photo(name='Document',
                    animal_type='dog', age='3', pet_photo='images\document.docx'):
    '''Проверяем возможность создания карточки питомца при вводе корректного API ключа,
    при вооде корректных значений параметров name, animal_type, age,
    но при условии добавления неверного формата файла в pet_photo (.docx)'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo

def test_negative_post_add_new_pets_with_incorrect_name_file_of_photo(name='Document',
                    animal_type='dog', age='3', pet_photo='images\капи.jpg'):
    '''Проверяем возможность создания карточки питомца при вводе корректного API ключа,
    при вооде корректных значений параметров name, animal_type, age,
    но при условии добавления файла в pet_photo с именем файла на криллице'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pets(auth_key, name, animal_type, age, pet_photo)
    assert status == 500 #при добавлении фото с именем на кириллице, возвращается ошибка от сервера с кодом 500