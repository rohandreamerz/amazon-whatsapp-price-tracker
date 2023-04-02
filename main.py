#!/usr/bin/env python
# coding: utf-8

# ### Step 1: Function to get Product details from ONE Amazon Search Results Page

# In[28]:


def getPandaDfForSearchResults(searchResultsPage):
    import pandas as pd
    from selenium import webdriver as wd
    import chromedriver_binary
    from bs4 import BeautifulSoup
    
    rows=[]
    for result in searchResultsPage:
        title = result.find("span", {"class": "a-text-normal"})
        sponsored = result.find("span", {"class": "a-color-base"}, text="Sponsored")
        price = result.find("span", {"class": "a-price-whole"})
        url = result.find("a", {"class": "a-link-normal"})
        if price:
            row= [title.text, bool(sponsored), price.text, "https://amazon.in/" + url['href']]
            rows.append(row)
    
    df=pd.DataFrame.from_records(rows, columns=["Title", "Sponsored", "Price", "URL"])
    return df


# ### Step 2: Function to Generate a Pandas Dataframe from All Results Pages

# In[36]:


def getDFfromURL():
    
    import pandas as pd
    from selenium import webdriver as wd
    import chromedriver_binary
    from bs4 import BeautifulSoup
    
    wd=wd.Chrome()
    
    url="https://www.amazon.in/s?k=prs+se+custom+24&crid=3LJ2MTZTGCQA3&sprefix=prs+se%2Caps%2C237&ref=nb_sb_ss_ts-doa-p_2_6"
    
    
    wd.get(url) #fetch the amazon search page
    
    nextPageCssClasses=[] 
    
    try:
        nextPageLink = wd.find_element_by_class_name("a-last") #try to find next page button
        
    except:
        pass


    df_all_search_results = pd.DataFrame(columns=["Title", "Sponsored", "Price","URL"]) #initialize a dataframe

    while not "a-disabled" in nextPageCssClasses:
        soup = BeautifulSoup(wd.page_source)
        searchResultsPage = soup.findAll("div", {"data-component-type": "s-search-result"})
        df = getPandaDfForSearchResults(searchResultsPage)
        df_all_search_results = pd.concat([df_all_search_results, df])

        # go to next page
        try:
            nextPageLink.click()
            nextPageLink = wd.find_element_by_class_name("a-last")
            nextPageCssClasses = nextPageLink.get_attribute("class").split()
            time.sleep(2)
        except:
            nextPageCssClasses.append("a-disabled")

    if "a-disabled" in nextPageCssClasses:
        print("Reached last page of search results")

    df_all_search_results['Price'] = df_all_search_results['Price'].str.replace(",","")
    df_all_search_results['Price'] = df_all_search_results['Price'].astype(float)
    
    return df_all_search_results


# ### Step 3: Function to Send Whatsapp Message (with Screenshot)

# In[35]:


def sendWhatsAppMessage(df):
    import pywhatkit as kit
    import os
    try:
        os.mkdir("images")
    except:   
        pass
    my_phone_number="+9198921XXXXX"
    from selenium import webdriver as wd
    wd=wd.Chrome()
    path=os.getcwd()
    img_path=path+'\\images'
    for index, guitarrow in df.iterrows():
        print(guitarrow.URL)
        wd.get(guitarrow.URL)
        screenshotFilepath=img_path+"\\"+f"screenshot_{index}.png"
        wd.save_screenshot(screenshotFilepath)
        kit.sendwhats_image(my_phone_number, screenshotFilepath, guitarrow.URL, tab_close=True)


# ### Step 4: Function to Execute the Whole Process

# In[31]:


def start():
    
    while (True):
    
        df = getDFfromURL()

        df_query = df[(df.Title.str.contains("Custom 24")) & (df.Price <= 86000)]

        if (not df_query.empty):
            print("Found products that I want to buy")
            sendWhatsAppMessage(df_query)
            print(df_query)
            break

        else:

            time.sleep(60)
            
    return None


# ### Final Step: Run!

# In[34]:


start()


# In[ ]:




