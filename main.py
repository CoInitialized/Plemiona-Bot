from selenium import webdriver
from time import sleep
import math

name = '' # your login
password = '' #your password
village_cords = '537|748' # coordinates of your village

radius =  15 # radius of attack range
points = 120 # max number of points for a villages to attack
server_name = 'pl148'

ignored_villages = ['532|746'] # coords of villages you don't want to attack but are in range

driver = webdriver.Chrome()


number_spear = "2"
number_sword = "2"
number_knight = "1"


def get_coords(text):
    lista = text.split('|')
    coordy = lista[0][-3:] + '|' + lista[1][:3]
    return coordy

def get_distance(coords1, coords2 = village_cords):

    x1 = float(coords1[:3])
    x2 = float(coords2[:3])
    y1 = float(coords1[4:])
    y2 = float(coords2[4:])

    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def compare_distance(coords1, coords2 = village_cords):

    if get_distance(coords1) > get_distance(coords2):
        return True
    else:
        return False

def template_a():

    driver.find_element_by_xpath('//*[@id="unit_input_spear"]').send_keys(number_spear)
    sleep(1)
    driver.find_element_by_xpath('//*[@id="unit_input_sword"]').send_keys(number_sword)
    sleep(1.5)

def template_b():

    driver.find_element_by_xpath('//*[@id="unit_input_knight"]').send_keys(number_knight)
    sleep(1)



templates = [template_a, template_b]


driver.get('https://plemiona.vopo.pl/village_list/')
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_id('id_world'))
# select by visible text
#select.select_by_visible_text('Banana')
# select by value 
select.select_by_value(server_name)

driver.find_element_by_xpath('//*[@id="id_coords"]').send_keys(village_cords)
driver.find_element_by_xpath('//*[@id="id_size"]').send_keys(radius)
driver.find_element_by_xpath('/html/body/div/div/div/form/button').click()
sleep(2)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[2]/div[7]/div/label[3]').click()
sleep(2)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[2]/div[5]/div/div[2]/div/input').send_keys("\b\b\b\b\b\b"+ str(points))
sleep(8)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[2]/div[8]/button').click()
sleep(1)
all_villages = driver.find_element_by_xpath('//*[@id="export_space_coords"]').get_attribute('value')
sleep(2)

driver.get("https://www.plemiona.pl/")
driver.find_element_by_xpath('//*[@id="user"]').send_keys(name)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('/html/body/div[3]/div[4]/div[10]/div[3]/div[2]/form/div/div/a').click()


sleep(2)
driver.get('https://www.plemiona.pl/page/play/{}'.format(server_name))
sleep(2)
driver.get('https://pl148.plemiona.pl/game.php?village=66423&screen=place')

villages = all_villages.split()
attack_string_to_format = '//*[@id="commands_outgoings"]/table/tbody/tr[{}]/td[1]/span/span/a/span[2]'#.format(str(i+2))

# getting all attacks:
attacked_villages = []
for i in range(len(villages)):
    try:
        tekst = driver.find_element_by_xpath(attack_string_to_format.format(i + 2)).text
        if 'Powr' in tekst:
            continue
        attacked_villages.append(get_coords(tekst))
    except:
        pass
print('Already attacked villages:')
print(attacked_villages)
sleep(1)
villages.sort(key = get_distance)

i = 0



for index, village in enumerate(villages):

    if village in attacked_villages or village in ignored_villages:
        continue


    coords = '//*[@id="place_target"]/input'
    driver.find_element_by_xpath(coords).send_keys(village)
    sleep(1)

    templates[i]()

    attack = '//*[@id="target_attack"]'
    driver.find_element_by_xpath(attack).click()
    try:
        attack_confirm = '//*[@id="troop_confirm_go"]'
        driver.find_element_by_xpath(attack_confirm).click()
        print("Attacking village: {}".format(village))
    except:
        print('Not enough units to run tamplate {}'.format(str(templates[i])))
        i += 1
        if i < len(templates):
            driver.get('https://pl148.plemiona.pl/game.php?village=66423&screen=place')
            coords = '//*[@id="place_target"]/input'
            driver.find_element_by_xpath(coords).send_keys(village)
            sleep(1)
            templates[i]()
            driver.find_element_by_xpath(attack).click()
            driver.get('https://pl148.plemiona.pl/game.php?village=66423&screen=place')
        else:
            break




sleep(2)
driver.quit()