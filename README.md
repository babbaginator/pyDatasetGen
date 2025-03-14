**pyDatasetGen** is a free and open-source library for producing customizable randomly generated datasets to be used in testing and development. 

Created by Neil Aitken (neil.aitken@gmail.com) 

## Development
pyDatasetGen was originally created by Neil Aitken to provide a simple way to generate customized datasets to test data mining and data visualization code. Sometimes we need 
to test our code, but want to avoid unnecessary interaction with a dataset that might contain private, proprietary, sensitive, or restricted information. Provided we know the 
general format of the dataset (categories of data and column names), we create small or large test datasets that mimic the real dataset, without endangering the original dataset,
making unauthorized copies, or having to file repeated requests for access.

## Features
**pyDatasetGen** supports the random generation of the following variable types
1. **comment**: a string typical of a message or caption
2. **int**: an integer value generated from the provided min and max
3. **count**: an integer value to represent view counts or likes generated from a min, max, and median (most common value)
4. **date**: a date string (YYYY-MM-DD) generated from the provided start date and end date (both provided in YYYY-MM-DD format)
5. **email**: a properly formatted email address using only ASCII characters. Email tends to use some part of the user's generated name as part of the account name
6. **url**: a properly formatted URL, with the possibility of a subpage
7. **hashtag**: a short randomly generated hashtag that has a '#' prefix
8. **fullname**: a randomly generated name featuring a first name followed by a last name. Names are drawn from a variety of languages and cultures and represent different genders.
9. **fullname_rev**: like fullname, but name string displays last name first, followed by a comma, then the first name (eg. "LastName, FirstName"). Good if the column is to be sorted
10. **firstname**: generates just a first name
11. **lastname**: generates just a last name (surname)
12. **streetaddress**: generates a street address (eg. 123 Mill Bay)
13. **phonenum**: generates a phone number (eg. 626-123-4567)
14. **booktitle**: generates a book title

## Configuration

### CFG_GEN_DATASET
This file defines the columns in the dataset and how they should be generated. Entries can be defined as lists (denoted by [] with comma separated elements) or a generated element (? followed by type). 
Any line can be commented out (disabled) by placing a # at the start.

Example
```
platform=[twitter,instagram,facebook,youtube,telegram]
hashtags=[#edmonton,#canada,#chickenwar,#badmonkey,#15minrice,#oilers,#bigoil,#sanctuary,#immigration,#fireisland,#tradewar,#badidea,#sadnews]
#hashtags=?hashtag
message=?sentence
email=?email
url=?url
name=?fullname
date=?date(2023-01-01,2024-12-31)
comment_count=?int(0,50,2500)
like_count=?int(0,200,14000)
```

### CFG_GEN_BASE.TXT
This file defines the basic building blocks for hashtags, messages, and other types of non-name random text. At the very least, the following entries must be present: 
- adjectives (adjectives that should be used for building descriptive phrases, user handles, hashtags, etc)
- nouns (nouns that should be used for creating phrases, user handles, hashtags, etc)
- actors (people or creatures that perform actions)
- group (words that represent organizations, categories of people, or other collectives)
- places (usually specific geographic locations, but any location would work)

Example
```
adjectives=[new,old,fiery,smoky,ancient]
nouns=[cloud,can,box,door]
actors=[driver,banker,scientist,professor,dog,cat]
group=[police,students,immmigrants,big industry]
places=[Vancouver,Toronto,NYC,Greenland,Berlin,Canada,Scotland]
```

If additional categories are added, the code can be extended to access these categories.

### CFG_GEN_NAMES
This file contains the lists of male, female, and family names for a variety of different language/heritage groups. The first two entries should be **name_groups** and **name_subgroups** which 
list the languages/heritages prefixes that you want used in name generation. **name_subgroups** simply stores the naming convention suffixes you are using (eg. MaleGiven, FemaleGiven, Family). 
All the remaining entries should follow the pattern where  the entry is named: <name_group><name_subgroup> -- eg. americanMaleGiven.

Example
```
americanMaleGiven=[James,John,Robert,Michael,William,David,Richard,Charles,Joseph
americanFemaleGiven=[Mary,Patricia,Linda,Barbara,Elizabeth,Jennifer,Maria,Susan
americanFamily=[Abell,Ackworth,Adams,Addicock,Alban,Aldebourne,Alfray,Alicock
chineseMaleGiven=[Aiguo,An,Angúo,Bai,Bingwen,Bo,Bohai,Bojing,Bolin,Boqin
chineseFemaleGiven=[Ai,An,Baozhai,Bi,Biyu,Bo,Changchang,Changying,Chao-xing
chineseFamily=[Lǐ,Wáng,Zhāng,Liú,Chén,Yáng,Huáng,Zhào,Zhōu,Wú,Xú,Sūn,Zhū
germanMaleGiven=[Abelard,Adie,Adler,Alaric,Albert,Albrecht,Alger
germanFemaleGiven=[Adalgisa,Adelaide,Adolfina,Aemilia,Alberta
germanFamily=[Abel,Aber,Achen,Ackert,Adelberg,Ahlgrim,Aller
```


