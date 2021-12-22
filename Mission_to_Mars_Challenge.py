#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### News Headlines and Summaries

# In[ ]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[ ]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[ ]:


slide_elem.find('div', class_='content_title')


# In[ ]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[ ]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[ ]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[ ]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[ ]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[ ]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[ ]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[ ]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[ ]:


df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[3]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[4]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemis_soup = soup(html, 'html.parser')
hemi_links = hemis_soup.find_all('div', class_="item")

for link in hemi_links:
    hemispheres = {}
    
    # Determine hemisphere link
    href_link = link.a['href']
    
    # Go to hemisphere's page
    browser.visit(f'{url}{href_link}')
    
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    # Searches through 'li' to find correct image, saves image url to dictionary
    for li in hemi_soup.find_all('li'):
        if 'Sample' in li.text:
            image = li.find('a')['href']
            hemispheres['img_url'] = f'{url}{image}'
    
    # Finds title, saves title to dictionary
    title_line = hemi_soup.find('h2', class_="title")
    title_text = title_line.text
    hemispheres['title'] = title_text
    
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# In[5]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[6]:


# 5. Quit the browser
browser.quit()

