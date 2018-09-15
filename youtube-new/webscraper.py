import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict


url_list = []
with open('USvideos.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        url_list.append(row[0])


# Opens chrome (MUST have selenium plugin in PATH or will cause an error)
driver = webdriver.Chrome()

vid_dict = defaultdict(list)
url_list = url_list[1:]
count = 0

for i in range(300, 500):
    url = url_list[i]
    vid_dict[url] = []
    try:
        driver.get("https://www.youtube.com/watch?v=" + url)
    except:
        print("website failed to load")
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        continue


    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/yt-view-count-renderer/span[1]'))
        wait(driver, 5).until(element_present)
        views = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
        vid_dict[url].append(str(views).split(" ")[0])
    except:
        print("views failed: ", url)
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        vid_dict[url].append(str(0))
        continue

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a'))
        wait(driver, 5).until(element_present)
        likes = driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[1]/a').find_element_by_id("text").get_attribute("aria-label")
        vid_dict[url].append(str(likes).split(" ")[0])
    except:
        print("likes failed: ", url)
        vid_dict[url].append(str(0))

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a'))
        wait(driver, 5).until(element_present)
        dislikes = driver.find_element_by_xpath('//*[@id="top-level-buttons"]/ytd-toggle-button-renderer[2]/a').find_element_by_id("text").get_attribute("aria-label")
        vid_dict[url].append(str(dislikes).split(" ")[0])
    except:
        print("dislikes failed: ", url)
        vid_dict[url].append(str(0))

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="count"]/yt-formatted-string'))
        wait(driver, 5).until(element_present)
        comments = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string').text
        vid_dict[url].append(str(comments).split(" ")[0])
    except:
        print("comments failed: ", url)
        vid_dict[url].append(str(0))


csv_file = open('new_vid_data.csv', 'a')
writer = csv.writer(csv_file)
# writer.writerow(["video id", "views", "likes", "dislikes", "comment_count"])
for key, value in vid_dict.items():
    value.insert(0, key)
    writer.writerow(value)

csv_file.close()
driver.close()
