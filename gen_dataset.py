## ===================================================================================
## DATASET GENERATOR
## Developed by Neil Aitken | neil.aitken@gmail.com
## ===================================================================================

import random
import os
import re
import pandas as pd
from anyascii import anyascii 

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

## Define Resource Path
def resource_path(relative_path):
    import sys
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS,os.path.join(ASSETS_DIR,relative_path))
    return os.path.join(ASSETS_DIR, relative_path)

## ===================================================================================
## UTILITY FUNCTIONS
## ===================================================================================

## Select item from given list
def choose(itemlist):
    item = None
    if len(itemlist)>0:
        item = itemlist[random.randint(0,len(itemlist)-1)]
    return item

## Generate a number between 1 and num
def roll(num=6):
    return random.randint(1,num)

## Add the correct article to a word ('an' for words beginning with vowel sounds, 'a' for all others)
def add_article(st):
    import re
    if re.match(r'[aeiou]',st) or st == 'hour':
        result = "an "+st
    else:
        result = "a "+st
    return result

## Returns the plural of a word
def make_plural(word):
    result = ''
    match word:
        case 'fish','deer','catfish','moose':
            result = word
        case 'mouse','louse':
            result = re.sub('ouse','ice',word)
        case 'thief':
            result = word[0:-1]+'ves'
        case 'goose':
            result = 'geese'
        case 'ox':
            result = 'oxen'
        case _:
            if word.endswith('y'):
                if word[-2] == 'e':
                    result = word+'s'
                else:
                    result = word[0:-1]+'ies'            
            elif word.endswith('x') or word.endswith('ch') or word.endswith('ss'):
                result = word+'es'
            else:
                result = word+'s'
    return result    

## ===================================================================================
##    VOCAB: Container object for managing word lists from an external config file. 
##           Should contain NOUNS, ADJECTIVES, ACTORS, PLACES, and GROUP terms
##           Can be extended to contain other categories of words
## ===================================================================================
class Vocab:
    def __init__(self,filename='cfg_gen_base.txt'):
        self.read(filename)

    # read config file and add attributes for each entry        
    def read(self,filename):
        try:     
            lines = open(resource_path(filename),'r',encoding='utf-8')     
                
            for line in lines:                
                if not line.startswith('#') and not line=='\n':  # Ignore comments and empty lines
                    key,value = line.split('=')
                    value = re.sub('\\[','',value)
                    value = re.sub('\\]','',value)                     

                    key = key.strip()
                    value = value.strip().split(',')
                    setattr(self,key,value)
                    
        except:
            print(f'ERROR - {filename} did not finish loading')

    ## optional method for retrieving values by key - returns None if key doesn't exist
    def get(self,key):
        result = None
        if key in self.keys():
            result = getattr(self,key)
        return result
        
## ===================================================================================
##     NAMEGENERATOR:  Used to generate names. Relies on external config file.
## ===================================================================================
class NameGenerator:
    def __init__(self,config_file='cfg_gen_names.txt'):        
        self.read(config_file)     
        self.vocab = Vocab()    

    # Read external config file and create new object attributes based on key/value pairs
    def read(self,filename):
        try:     
           lines = open(resource_path(filename),'r',encoding='utf-8')         
           for line in lines:                
                if not line.startswith('#') and not line=='\n':  # Ignore comments and empty lines
                    key,value = line.split('=')
                    value = re.sub('\\[','',value)     # Anything between [] is interpreted as a list/array
                    value = re.sub('\\]','',value)                
                    setattr(self,key.strip(),value.strip().split(','))

        except:
            print(f'ERROR - {filename} did not finish loading')

    # Returns a given/first name based on gender and language/group      
    def get_given(self,gender='random',group='random'):
        result = ''
        name_group = group
        if not group in self.name_groups:
            name_group = choose(self.name_groups)
        
        name_type = gender        
        match(name_type):
            case 'male':
                subcat = name_group+'MaleGiven'
                result = choose(getattr(self,subcat))
            case 'female':
                subcat = name_group+'FemaleGiven'
                result = choose(getattr(self,subcat))
            case _:
                sex = choose(['male','female'])
                result = self.get_given(sex)
        return result
    
    # Returns a family name
    def get_family(self,group='random'):
        result = ''
        name_group = group
        if not group in self.name_groups:
           name_group = choose(self.name_groups)

        family = name_group+"Family"
        result = choose(getattr(self,family))
        return result

    # Returns a full name (first and last)
    def get_fullname(self,gender='random'):
        name_group = choose(self.name_groups)
        family_name = self.get_family()
        first_name = self.get_given(gender,name_group)
        result = first_name+" "+family_name
        return result
    
    # Returns a nickname (useful for generating email accounts, social media handles, etc)
    def get_nickname(self,gender="random",name='random'):
        result = ''
        index = roll(14)
        ADJECTIVES = self.vocab.adjectives
        NOUNS = self.vocab.nouns
        fullname = name
        if name == 'random':
            fullname = nameGen.get_fullname()
        names = fullname.split(' ')
        given = names[0]
        family = names[1]

        match index:
            case 1: 
                result = choose(self.vocab.adjectives)+given
            case 2:
                result = given+str(roll(100))
            case 3:
                birthdate = fake_date('1930-01-01','2007-12-31')
                birthyear,birthmonth,birthday = birthdate.split('-')
                result = given+birthyear
            case 4:
                result = fullname
                result = re.sub(' ','_',result)
            case 5:
                result = given+str(roll(100))
            case 6:
                result = given+"_the_"+choose(NOUNS)
            case 7:
                result = given+'_'+choose(['likes','loves','saves','hearts','digs','eats','sells'])+'_'+make_plural(choose(NOUNS))
            case 8:
                result = "the_"+choose(ADJECTIVES)+"_"+given
            case 9:
                prefix = ['not','alt','fake','robot','your_favorite','dire','geeky']
                result = choose(prefix)+given
            case _:
                result = given+family[0]+str(roll(100))

        return result

## ===================================================================================
##       Create a NameGenerator instance to be called globally
## ===================================================================================
nameGen = NameGenerator()

## ===================================================================================
##       Functions for generating numbers, text, emails, accounts, and more
## ===================================================================================
 
# In order to create fake views or likes that reflect the possibility of virality,
# fake numbers are defined with a 'min','max', and 'median' (most common value) - which then are used
# by fake_num and fake_exp to create plausible counts.

# Return a fake viral/high end result for a count
def fake_exp(median,max):
    import math

    # Select a power that's between the natural log of the median and the natural log of the max
    pow = random.randint(int(math.log(median)),int(math.log(max)))      
    num = math.exp(pow)

    # Insurance - if num somehow ends up bigger than max, choose a number randomly between median and max
    # but without relying on explosive growth calculation
    if num > max:
        waffle = 200
        if max-median < 200:
            waffle = max-min
        num = max-random.randint(1,waffle)
    return num

# Returns a number that falls within a range
def fake_num(dmin=0,dmedian=50,dmax=35000,dsize=3000):
    result = ''
    test = random.randint(0,20)

    # Bottom half of the results fall below the median
    if test < 10:
        result = str(int(random.randint(0,dmedian)))
    # Another set fall between the median and a calculated submax threshold
    elif test < 15:
        submax = int(dmax/dmedian + (random.randint(0,dmedian-1)))
        if dmedian > submax:
            submax = dmax
        result = str(int(random.randint(dmedian,submax)))
    # Another cluster falls within 2 deviations from the median
    elif test < 20:
        buffer = int((dmax-dmedian)*0.5)
        new_max = buffer+dmedian
        if new_max>dmax:
            new_max = dmax
        result = str(int(random.randint(dmedian,buffer+dmedian)))
    # At the top, fake explosive growth and virality with fake_exp
    else:        
        result = str(int(fake_exp(dmedian,dmax)))
    return result

# Returns a fake date as a string between two given dates in YYYY-MM-DD format
def fake_date(start_date='2000-01-01',end_date='2024-12-31'):
    import datetime as dt    
    first_date = dt.date.fromisoformat(start_date)
    last_date = dt.date.fromisoformat(end_date)
    date_diff = last_date - first_date
    offset = random.randint(0,date_diff.days)
    new_date = first_date+dt.timedelta(offset)
    return new_date.isoformat()

# Returns a properly formatted twitter/instagram account name (@username)
def fake_account():
    result=''
    index=roll(10)    
    ADJECTIVES = nameGen.vocab.adjectives
    NOUNS = nameGen.vocab.nouns       
    ACTORS =  nameGen.vocab.actors

    match index:
        case 1: 
            result = choose(ADJECTIVES)+choose(['','_'])+choose(NOUNS)
        case 2: 
            result = choose(ADJECTIVES)+choose(['','_'])+choose(ACTORS)
        case 3: 
            result = choose(NOUNS)+choose(ACTORS)
        case _: 
            result = anyascii(nameGen.get_nickname())
    result = re.sub(' ','_',result)
    result = '@'+result.lower()
    return result

# Returns a fake message string. This can be modified to suit the needs of the dataset
def fake_sentence():
    result = ''
    index = roll(4)
    DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    DAY_ADJS = ['terrible','horrible','terrific','brilliant','great','bad']
  
    ADJECTIVES = nameGen.vocab.adjectives
    NOUNS = nameGen.vocab.nouns
    PLACES = nameGen.vocab.places 

    match index:
        case 1: 
            result = choose(NOUNS).capitalize()+" in "+choose(PLACES).capitalize()+". What a "+choose(DAY_ADJS)+" idea!"
        case 2: 
            result = "Another "+choose(DAYS)+". Another "+choose(ADJECTIVES)+" "+choose(NOUNS)
        case 3: 
            result = "Too close for comfort "+fake_account()
        case 4:
            result = fake_account()+" Have you seen this?!"
        case _:
            result = 'Check out the '+choose(NOUNS)+' in '+choose(PLACES)+'! '+fake_account()
    
    return result

# Returns a fake domain name. Useful for creating fake URLs and email addresses
def fake_domain():
    result = ''    
    dotwhat = ['com','net','org']
    dotorg = ['org','edu','gov']

    ADJECTIVES = nameGen.vocab.adjectives
    NOUNS = nameGen.vocab.nouns
    ACTORS = nameGen.vocab.actors

    index = roll(9)
    match index:
        case 1: 
            result = choose(ADJECTIVES)+choose(NOUNS)+"."+choose(dotwhat)
        case 2:
            result = choose(ADJECTIVES)+choose(ACTORS)+"."+choose(dotwhat)
        case 3:
            result = nameGen.get_family()+"."+choose(dotwhat)
        case 4:
            result = nameGen.get_fullname().lower()+"."+choose(dotwhat)
        case 5:
            result = choose(NOUNS)+"."+choose(dotorg)
        case 6:
            result = nameGen.get_family()+"."+choose(dotorg)
        case _:
            result = choose(NOUNS)+"."+choose(dotwhat)
    result = re.sub(' ','',result)
    result = anyascii(result.lower())
    return result

# Returns a fake email address - relying on nickname and fake_domain. 
# If a full name is passed in, it will use it as a potential seed for 
# creating an email (the whole name or part of it)
def fake_email(uname='random'):
    index = roll(4)    
    email_domains=['gmail.com','hotmail.com','aol.com','outlook.com','yahoo.com']

    match index:
        case 1:
            domain = fake_domain()
        case _:
            domain = choose(email_domains)

    index = roll(4)
    nickname = uname
    if uname == 'random':
        nickname = nameGen.get_fullname()
    names = nickname.split(' ')        
    firstname = names[0]
    lastname = names[1]

    match index:
        case 1: 
            nickname = firstname+"."+lastname
        case 2:
            nickname = firstname+lastname[0]
        case _:
            nickname = nameGen.get_nickname(name=nickname)    
    nickname = str(anyascii(nickname))    
    result = nickname.lower()+"@"+domain
    result = re.sub(' ','',result)
    return result

# Returns a fake hashtag with a # prefix
def fake_hashtag():
    result = '#'
    index = roll(4)
    NOUNS = nameGen.vocab.nouns
    ACTORS = nameGen.vocab.actors
    PLACES = nameGen.vocab.places 
    ADJECTIVES = nameGen.vocab.adjectives
    match index:
        case 1: 
            result = choose(ADJECTIVES)+choose(NOUNS)
        case 2:
            result = choose(ADJECTIVES)+choose(ACTORS)
        case 3:
            result = choose(PLACES)
        case 4:
            result = choose(ADJECTIVES)+choose(PLACES)
        case 5:
            result = choose(ADJECTIVES)+nameGen.get_family()
        case 6:
            result = choose(ADJECTIVES)+choose(['times','accidents','people','fates','cats','films','books'])
        case _:
            result = choose(NOUNS)
    result = "#"+re.sub(' ','',result)
    return result

# Returns a fake website URL (possibly with subpage)
def fake_url():
    result = 'www.'+fake_domain()
    index = roll(7)
    NOUNS = nameGen.vocab.nouns
    PLACES = nameGen.vocab.places 

    match index:
        case 1: 
            result = result + '/'+choose(NOUNS)+'/'+choose(NOUNS)+'.html'
        case 2:
            result = result + '/'+choose(PLACES)+'.html'
        case 3:
            result = result + '/'+choose(nameGen.vocab.adjectives)+choose(NOUNS)+'.html'
        case _:
            result = result
    result = re.sub(' ','',result)
    return result

# Returns a full name, given/first name, family/last name, nickname, or reversed name format
def fake_name(kind='full'):
    result = nameGen.get_fullname()
    match kind:
        case 'full_rev':
            result = nameGen.get_family()+', '+nameGen.get_given()
        case 'first':
            result = nameGen.get_given()
        case 'last':
            result = nameGen.get_family()
        case 'nick':
            result = nameGen.get_nickname()
        case _:
            result = nameGen.get_fullname()
    return result


## ===================================================================================
##     FAKEUSER: Used to create internally consistent names, email addresses, 
##     and account names.
## ===================================================================================
 
class FakeUser:
    def __init__(self):
        self.generate()
    
    # Generate names, email, and nickname
    def generate(self):
        self.name = fake_name('full')
        namelist = self.name.split(' ')
        self.given = namelist[0]
        self.family = namelist[1]
        self.rev_name = self.family+', '+self.given
        self.email = fake_email(uname=self.name)
        self.handle = nameGen.get_nickname(name=self.name)

    # Dump info 
    def dump(self):
        result = f'{self.name} | {self.email} | {self.handle}'
        return result
    
    # Print contents to screen
    def print(self):
        print(self.dump())

## ===================================================================================
##   DATASET GENERATOR: Generates datasets based on externally defined parameters
## ===================================================================================

class DatasetGenerator:
    def __init__(self):
        self.datatypes = {}
        self.user = FakeUser()
        self.load()

    # Load configuration file
    def load(self,filename='cfg_gen_dataset.txt'):   
        try:     
            lines = open(resource_path(filename),'r')
        except:
            print(f'ERROR - {filename} does not exist')
        
        for line in lines:
            if not line.startswith('#') and not line=='\n':  # Ignore comments and empty lines
                key, value = line.split('=')   
                value = value.rstrip()
                if value.startswith('['):
                    value = value.replace('[','')
                    value = value.replace(']','')
                    list_values = value.split(',')
                    self.datatypes[key] = list_values
                elif value.startswith('?'):
                   self.datatypes[key] = value
                else:
                    self.datatypes[key] = value
    
    # Interpret variable elements
    def parse(self,value):
        val = value.replace('?','')
        parens = re.search('\\(',val)
        result = ''
        if parens: 
            val_type,params = val.split('(')
        else:
            val_type = val                                
        match val_type:
            case 'sentence': 
                result = fake_sentence()                                
            case 'int':
                vmin,vmax,vmedian = params[0:-1].split(',')
                result = fake_num(int(vmin),int(vmax),int(vmedian))
            case 'date':
                vstart,vend = params[0:-1].split(',')
                result = fake_date(vstart,vend)
            case 'email':
                result = self.user.email
            case 'url':
                result = fake_url()
            case 'hashtag':
                result = fake_hashtag()
            case 'fullname':
                result = self.user.name
            case 'fullname_rev':
                result = self.user.rev_name
            case 'firstname':
                result = self.user.given
            case 'lastname':
                result = self.user.family
            case _:
                result = val
        return result
    
    # Generate each dataset entry
    def gen(self):
        result = {}        
        self.user = FakeUser()
        for key in self.datatypes.keys():
            value = self.datatypes[key]            
            if type(value) is list:
                result[key] = choose(value)
            elif value.startswith("?"):
                result[key] = self.parse(value)
            else:
                result[key] = value
        return result
    
    # Generate dataset
    def generate(self,num=100):
        results = []
        for ind in range(0,num):
            results.append(self.gen())
        return results
    
    # Print contents of the dataset
    def print(self):
        print(self.datatypes)

## ===================================================================================
##    Main Program
## ===================================================================================

dataset = DatasetGenerator()
results = dataset.generate(100)
df = pd.DataFrame(results)
df.to_csv('generated_dataset.csv')
