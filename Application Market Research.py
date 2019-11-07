#!/usr/bin/env python
# coding: utf-8

# # Market Research: App Popularity Trends
# Using data compiled from the AppStore and Google Play app markets, we will explore what factors increase the popularity of apps in which markets.

# In[2]:


#Import process for both data sets
import os
import pandas as pd
os.chdir('C:\\Users\\Andrew\\Desktop\\Data-Blog\\AppUsage\\')
from csv import reader

#App Store
opened_file = open('AppleStore.csv', encoding="utf8")
read_file = reader(opened_file)
ios = list(read_file)
header_ios = ios[0]
ios = ios[1:]

#Google Play
opened_file = open('googleplaystore.csv', encoding="utf8")
read_file = reader(opened_file)
android = list(read_file)
header_android = android[0]
android = android[1:]


# After designating the directory, we need to separate the header and body of each data set to allow for easier analysis, and assigning each to a variable. 

# In[3]:


print('IOS DATA')
print(header_ios)
print(ios[:2])
print('Total Rows =',' ', (len(ios)))
print('\n')
print('ANDROID DATA')
print(header_android)
print(android[:2])
print('Total Rows =',' ', (len(android)))


# In[4]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# These data sets give information about 20,000 apps between the AppleStore and Google Play store. Downloaded from separate Kaggle contributers ([here](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home) and [here](https://www.kaggle.com/lava18/google-play-store-apps/home)), these data sets have slightly different column variables. Below is a table giving the full title of each variable:

#                                                              IOS  
#  
# | Column Name | Description |  
# | ----------- | ----------- |  
# | "id"        | App ID      |  
# | "track_name" | App Name    |  
# | "size_bytes" | Size (MB)   |  
# | "currency"  | Sale Currency |  
# | "price"     | Price       |  
# | "rating_count_tot" | # of Ratings | 
# | "rating_count_ver" | # of Ratings on Current Version |
# | "user_rating" |  Rating (1-5) | 
# |"user_rating_ver"| Current Version Rating (1-5)|
# | "ver"       | Update Patch | 
# | "cont_rating" | Recommended User Age | 
# | "prime_genre" | Genre    | 
# | "sup_devices.num" | Number of supported devices | 
# 
# 
#                                                              Android          
# 
# | Column Name | Description |
# | ----------- | ----------- |
# | "app"       | App Name    |
# | "category"  | Category    |
# | "rating"    | Rating (1-5) |
# | "reviews" | # of Reviews |
# | "size"      | Size (MB)   |
# | "installs"  | # of Installs |
# | "type"      | Category    |
# | "price"     | Price       |
# | "content rating" | Recommended User Age |
# | "genres"    | Genre       |
# | "last updated" | Date of last data update |
# | "current ver" | Current Version |
# | "android ver" | Android Version |
# 

# While these datasets are large, they contain several applications for non-English speaking audiences (we are focusing on American consumers) and several repeated entries.

# In[5]:


#Find all duplicate entries:

dup_android = []
unique_android = []

for app in android:
    name = app[0]
    if name in unique_android:
        dup_android.append(name)
    else:
        unique_android.append(name)
print('Number of Android duplicate entries:', ' ', len(dup_android))

dup_ios = []
unique_ios = []

for apps in ios:
    name = apps[2]
    if name in unique_ios:
        dup_ios.append(name)
    else:
        unique_ios.append(name)
print('Number of iOS duplicate entries:', ' ', len(dup_ios))


# In[6]:


print(dup_ios)
for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# As the iOS data set only has two duplicate entries, each only one duplicate, they can easily be removed. However, the Google Play dataset contains multiple duplicates for single apps. Looking at the Instagram duplicates, we see that some entries are more recent. We will be using the number of reviews to ensure we capture the most recent entry for each app.

# In[7]:


#while attempting to run below function, an incorrectly recorded entry was found and removed
del android[10472]


# In[8]:


#isolating the duplicate entries with the highest reviews:
highest_reviews = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
        
    
    if name in highest_reviews and highest_reviews[name] < n_reviews:
        highest_reviews[name] = n_reviews
    elif name not in highest_reviews:
        highest_reviews[name] = n_reviews


#using the list of highest reviews to ensure only the most recent data gets added to android_clean
android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (highest_reviews[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

        #now we can double check to ensure all duplicates have been removed:
print(len(android_clean))


# We also see there are non-English applications included in this data set. Because we would like to focus on the English-speaking market for this analysis, we will need to remove apps with non-English names and characters.

# In[9]:


#create a function find strings in which there is more than 3 non-English characters, according to the ASCII system (range 0-127)
def is_english(string):
    non_ascii = 0
    
    for char in string:
        if ord(char) > 127:
            non_ascii += 1
            
            
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# In[10]:


ios_english = []
android_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)

for app in ios:
    name = app[2]
    if is_english(name):
        ios_english.append(app)
        

print('Remaining iOS apps:')
print(len(ios_english))
print('\n')
print('Remaining Android apps:')
print(len(android_english))


# The last change to our android and ios data sets will be to isolate all free to download applications. For the purpose of this analysis, we'd like to focus on the market for free apps.

# In[11]:


#loop through each data set in order to remove non-free applications.

#iOS

ios_final = []

for app in ios_english:
    price = app[5]
    
    if price == "0":
        ios_final.append(app)

#Google Play

android_final = []

for app in android_english:
    price = app[7]

    if price == "0":
        android_final.append(app)

print('Final Number of iOS apps:')
print(len(ios_final))

print('Final Number of Android apps:')
print(len(android_final))


# Now that we have our final data sets for each store, we'll need to focus on shared qualities that suceed in both markets.
# 
# We'll start with apps filtered by Genre:

# In[12]:


#create function to develop frequency tables within datasets:

def freq_table(dataset, index):
    f_table = {}
    total = 0
    
    for row in dataset:
        total += 1
        variable = row[index]
        
        if variable in f_table:
            f_table[variable] += 1
        else:
            f_table[variable] = 1

       #return as percentages
    f_percentage = {}
    for key in f_table:
        percentage = (f_table[key] / total) * 100
        f_percentage[key] = percentage
    
    return f_percentage

#create function to sort data in f_percentage dictionary alphabetically

def display_table(dataset, index):
    f_table = freq_table(dataset, index)
    table_display = []
    for key in f_table:
        key_val_as_tuple = (f_table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
print('Android Genre: Frequency Table:')        
print(display_table(android_final, 1))
print('\n')
print('iOS Genre: Frequency Table:')   
print(display_table(ios_final, 12))


# Comparing the two markets, iOS users focus many of their app downloads on games focused around entertainment or family. While Games is still the most popular category on the google play store, many Android users prioritize practical apps for utilities and finance.
# 
# After isolating areas of interest, we can look into specific apps in these Genres. We will order these by total installs to gauge popularity and assess what features these specific apps have in common.

# In[13]:


#iOS data set does not have a number of installs column, so 
#using the number of ratings we'll create a function to find 
#the average number of ratings per genre: 
genre_ios = freq_table(ios_final, 12)

for genre in genre_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[12]
        if genre_app == genre:
            n_ratings = float(app[6])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# At first glance, we see that Navigation, Reference, and Social have a large number of average reviews. However, looking deeper into it, we see that each of these categories have extremely popular apps that skew the results:

# In[16]:


for app in ios_final:
    if app[12] == 'Navigation':
        print(app[2], ':', app[6])


# In[14]:


for app in ios_final:
    if app[12] == 'Social Networking':
        print(app[2], ':', app[6])


# We can see that 'Games' and 'Family' are extremely popular across both Android and iPhone users, and offers a lot more versatility than other popular categories.
# 
# Now we need to look deeper into the games category:

# In[15]:


for app in ios_final:
    if app[12] == 'Games':
        print(app[2], ':', app[6])


# For the Android data set we have a column designating the number of installs, index 5.
# Although the data is collected in ranges, we can create and approximation of the average number of downloads for each genre.

# In[17]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[20]:


for app in android_final:
    if app[1] == 'GAME' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# As in iOS, games generate a large number of downloads, even more so if they are 'family-friendly' and are marketed towards children and their parents.

# ## Conclusions:
#   
#     Based off of the entirely of both data sets presented, an app designed for the genres "Family" and "Games" has to potential to be hugely successful for each platform, requiring only additional backend in order to make each compatible with both iOS and Android phones.
# 
#     While games can be a volitile investment due to the sheer number of gaming apps already on the market, it has a large profit margin if able to reach both parents and children as well as both major phone operating systems.

# In[ ]:




