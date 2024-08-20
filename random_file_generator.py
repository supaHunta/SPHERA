import os
import random
import rand

root = '/Users/fusion_tech/Desktop/FOTKI_NAFIG/'
wrong_root = '/Users/fusion_tech/Downloads/'
random_file_result = None
rename_file = None
files_list = []
wrong_list = []

print('++++++++++++++++2')
for photos in files_list:
    orig_photo = root+photos
    new_photo = os.rename(str(orig_photo), root +
                          str(rand.generate_random_string(5)+".png"))

for items in os.listdir(root):
    if not items.startswith('.'):
        files_list.append(items)
print(1)
for files in os.listdir(wrong_root):
    if files.endswith('.dmg'):
        wrong_list.append(files)
    

def get_a_random_file():
    print('++++++++++++++++4')
    global random_file_result
    random_file = random.choice(files_list)
    random_file_result = root+random_file
    return random_file_result

def get_a_random_wrong_file():
    global wrong_file_result
    wrong_file = random.choice(wrong_list)
    wrong_file_result = wrong_root+wrong_file
    return wrong_file_result

print(wrong_list)