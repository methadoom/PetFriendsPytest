from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Кот', animal_type='Кот', age='1', pet_photo='images\cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Пёс', animal_type='Кошка', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Пёс", "Кошка", "5", "images\cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


# 1 удаление несуществующего животного
def test_delete_non_existent_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кот", "Кот", "1", "images\P1040103.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

 # 2 загрузить видео вместо фото питомца
def test_add_new_pet_with_video_image(name='Вася', animal_type='Кот', age='3', pet_photo='images\кот.mp4'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500

# 3 назвать питомца спец символами
def test_add_new_pet_with_invalid_name(name='!"№;%:?*', animal_type='Кот', age='1', pet_photo='images\cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

# 4 возраст питомца буквами
def test_add_new_pet_with_invalid_age(name='Кот', animal_type='Кот', age='один год', pet_photo='images\cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

# 5 попробоват изменить питомца не из списка my_pets
def test_successful_update_self_pet_info(filter ='', name='Пёс', animal_type='Кошка', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    if len(result['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, filter[0]['id'], name, animal_type, age)

        assert status == 400


