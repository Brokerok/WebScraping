from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from multiprocessing import Pool


options = webdriver.ChromeOptions()
options.headless = False


def write_to_json(_data):
    data = []
    try:
        with open("output.json", "r") as file:
            data = json.load(file)
    except:
        pass
    print(len(data))
    data.append(_data)
    with open("output.json", "w") as file:
        json.dump(data, file, indent=4)


def pagin():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    url = 'https://www.allpointsfps.com/search/?sort=score&mpp=300&pg=1'
    driver.get(url)
    paginat = driver.find_element(By.ID, 'ctl00_SearchBody_NavigationTop_lnkLast')
    paginat.click()
    time.sleep(5)
    pagesn = driver.find_elements(By.CLASS_NAME, 'hawk-pageActive')
    pages = pagesn[1].text
    driver.close()
    driver.quit()
    return int(pages)


def main(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    items = driver.find_elements(by=By.CLASS_NAME, value='title-section')
    link_list = []
    for i in range(len(items)):
        link = items[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
        link_list.append(link)
    for link in link_list:
        try:
            driver.get(link)
            name = driver.title
            price = driver.find_element(by=By.XPATH,
                value='/html/body/div[1]/div[1]/main/div/section[2]/section[2]/div[2]/div[2]/div/div[2]/span[2]').text
            description = driver.find_element(by=By.CLASS_NAME, value='description').text
            oem = driver.find_elements(by=By.CLASS_NAME, value='line-value.sku-value')[1].text
            manufacturerName = driver.find_elements(by=By.CLASS_NAME, value='line-label.sku-label')[1].text[:-2]
            try:
                image = driver.find_elements(by=By.CLASS_NAME, value='thumb')[0].get_attribute('src')
            except:
                image = 'null'
            to_json = {"distributor": "Object('5c5ebad9bb2e1f555e656e10')", "manufacturerName": manufacturerName,
                       "oem": oem,
                       "description": description, "image": image, "name": name, "price": price, "url": link,
                       "crossnew": []}
            try:
                crossnew = driver.find_element(by=By.CLASS_NAME, value='list-group')
                listg = crossnew.find_elements(by=By.CLASS_NAME, value='list-group-item.replaces-item')
                for i in range(len(listg)):
                    crossoae = listg[i].find_elements(by=By.CLASS_NAME, value='oem-sku')
                    crossn = listg[i].find_element(by=By.CLASS_NAME, value='oem-name')
                    aes = []
                    for j in crossoae:
                        ae = j.text
                        aes.append(ae)
                    to_json["crossnew"].append({"mn": crossn.text,
                        "oems": aes})
            except:
                crossnew = 'null'
                to_json["crossnew"].append(crossnew)
            write_to_json(to_json)
        except:
            pass


def links(pages):
    links_list = []
    for i in range(pages):
        links_list.append(f'https://www.allpointsfps.com/search/?sort=score&mpp=300&pg={i + 1}')
    return links_list


if __name__ == '__main__':
    thread = int(input("Enter quantity threads: "))
    n = pagin()
    arr = links(n)
    p = Pool(processes=thread)
    p.map(main, arr)

time.sleep(55)

