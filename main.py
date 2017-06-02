from collector import *
from data_handler import *


for i in range(1, 10000):
    try:
        url_to_char_id, url_to_char_name = create_dicts_from_character_id(i)
        save_multiple_images(url_to_char_id)
    except:
        print("id {} does not exist".format(i))
