from selenium import webdriver              #### webdriver links up with the browserand performs the necessary actions.
from bs4 import BeautifulSoup               #### BeautifulSoup is a Python library for parsing HTML and XML documents.
import lxml                                 #### lxml is a HTML Parser

import time


IMAGE_PATH = []
CHROMEPATH = '/Users/eben.emmanuel/Downloads/chromedriver'

#### Webbrowser is Chrome and the webdriver is in the Path specified.
driver = webdriver.Chrome(executable_path= CHROMEPATH)

get_URL = 'https://www.google.com/search?rlz=1C5CHFA_enIN984IN984&source=univ&tbm=isch&q=pan+card'
driver.get(get_URL)

a = input("Press Enter to continue...")     ## When the webdriver opens up, scroll down to the bottom of the page. This will help to load all the images.

### Scroll all the way up
driver.execute_script("window.scrollTo(0, 0);")

pageHTML = driver.page_source           ## Get full HTML of the page.

### Using BeautifulSoup to Obtain the Image HTML        
soup = BeautifulSoup(pageHTML, 'lxml')
image_containers = soup.find_all('div', class_='isv-r PNCib MSM1fd BUooTd')     ## Find all the image containers of the specified Class.

len_image_containers = len(image_containers)
print(f'Found a total of {len_image_containers} images')            ## Understanding this will help us t click on the images in the future.

for i in range(1,len_image_containers):
    if i%25 == 0:
        continue
    Image_xpath = f'//*[@id="islrg"]/div[1]/div{[i]}'          ## Image xpath

    ## Grabbing the Small Preview URL
    previewImage_xpath = f'//*[@id="islrg"]/div[1]/div{[i]}/a[1]/div[1]/img'
    previewImage_Element = driver.find_element_by_xpath(previewImage_xpath)
    previewImage_URL = previewImage_Element.get_attribute('src')
    
    ## Click on the image.
    driver.find_element_by_xpath(Image_xpath).click()       

    ## Start While loop until URL inside is different from the Preview URL.
    start_time = time.time()
    while True:

        ImageElement = driver.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img'
            )
        ImageURL = ImageElement.get_attribute('src')

        if ImageURL != previewImage_URL:
            print("High Resolution Image URL", ImageURL)
            IMAGE_PATH.append(ImageURL)
            ### CAN ADD THE OCR CODE HERE ####
            break           ### Break out of the While loop and later Download the image.
        else:
            ## Making a timeout if the High Resolution Image URL is not loaded.
            if time.time() - start_time > 10:       ### 10 seconds timeout.
                print("Timeout")
                print("Low Resolution Image URL")
                #### CAN ADD THE OCR CODE HERE ####
                break
            


## Close the browser.
driver.quit()

print(IMAGE_PATH)