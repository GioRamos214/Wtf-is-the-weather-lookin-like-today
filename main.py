import requests
import json
import os
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

# Load credentials
load_dotenv()
api_key = os.getenv("API_KEY")

cwd = os.getcwd() + "/"

def cityForecast(city, key):
    # Careful uploading this on github, my API token is in here. 
    while True:
        try:
            data = loadJsonFile('data.json')
            unit = data['User']['preferredUnit']
            url = f"https://api.tomorrow.io/v4/weather/forecast?location={city}&units={unit}&apikey={api_key}"
            
                    

            if unit == 'imperial':
                unit_var = 'Farhenheit'
            elif unit == 'metric':
                unit_var = 'Celcius'
            
            headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate"
            }

            response = requests.get(url, headers=headers)
            data = response.json()
            
            # Go to the timelines array, go to the minutely array and select the first item. From that item, find the value of the key named temperature.
            temperature = data['timelines']['minutely'][0]['values']['temperature']
            print(f"The weather in {city} is {temperature} {unit_var}.")
            break
            
        except KeyError:
            city = input("Please input a valid city name: ") 

def createUserJsonFile():
    data = {}

    data['History'] = {}
    data['User'] = {}

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
        
def loadJsonFile(file_name):
    with open(f'{file_name}', 'r') as f:
        data = json.load(f)
        return data

def addDictToJSON(file_name, dict):
    data = loadJsonFile(file_name)
    
    if dict not in data:
        data[dict] = {}
        
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# File_name + dict + key + value
def updateKeyValue(file_name, dict, key, value):
    
    # Add the dict if it doesn't exist
    addDictToJSON(file_name, dict)
    
    data = loadJsonFile(file_name)
        
    data[dict][key] = value
    
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, )
    
def preferredUnits(unit_pref):
    
    units = ['imperial', 'metric']
    
    while True:
        if unit_pref in units:
            updateKeyValue(f'data.json', 'User', 'preferredUnit', unit_pref)
            break
        else:
            unit_pref = input(str("Please input a valid reponse (imperial/metric). "))

def checkKeyInJson(file_name, key):
    data = loadJsonFile(file_name)

    if 'User' in data:

        if key not in data['User']:
            print(f"The key, {key} does not exist. Creating Key." )
            data['User'][key] = "no_value"
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
                
        else:
            None
    
def lastLogin():
    now = str(datetime.now())
    
    checkKeyInJson('data.json','lastLogin')
    data = loadJsonFile('data.json')
    
    # Check to see if User dict exists, otherwise return an empty string + get lastLogin key, otherwise return none. 
    lastLoginDate = data.get('User', {}).get('lastLogin', None)
    
    if lastLoginDate == "no_value":
        print('')
        data['User']['lastLogin'] = now
        with open('data.json','w') as f:
            json.dump(data, f, indent=4)
            
    else:
        print(f'\nYour last login was on {lastLoginDate}')
        data['User']['lastLogin'] = now
        with open('data.json','w') as f:
            json.dump(data, f, indent=4)
        
def newUser():
    # Empty dictionary
    website_URL = 'https://www.tomorrow.io/'
    print(cwd)
    
    while True:
        welcomePage = str(input("This is your first time visiting this program. You will need to create an account with Tomorrow.io. \nWould you like to be redirected to make an account (y/n): "))
        welcomePage = welcomePage.lower()
        
        if welcomePage == 'y':
            webbrowser.open(website_URL)
            break
        elif welcomePage == 'n':
            break
        else:
            print("Pleaes enter a valid option.")
            continue
    
    while True:    
        print("\nTo properly use this program, you'll need to use an API_KEY. Your API key will be stored in a .env file located at the root folder of this folder. ")
        print("If you want to skip this process, hit ENTER.")
        get_api_key = input("Input API_KEY: ")
        
        if get_api_key == "":
            print("Please provide your API key to use this application. You will be unable to use any of the features until you do so. Closing for now.")
            
            # Update json file. Change key to false since user did not provide API key.
            updateKeyValue('data.json','User','createdAPIKEY','FALSE')
            
            exit()
        else:
            with open('.env','w') as f:
                f.write(f"API_KEY='{get_api_key}'")
                print(f"\nYour API key has been created. It is stored in the following directory: {cwd}")
            break
        
        # TODO give user the option to reset their key incase they fuck up. It's bound to happen. 

def getUnitValue():
    data = loadJsonFile('data.json')
    
    UnitData = data.get('User', {}).get('preferredUnit', None)
    
    if UnitData == None:
        newUnitValue = str(input("What unit do you prefer (imperial/metric) : "))
        newUnitValue = newUnitValue.lower()
        # This functions ensures the user is providing a valid unit.
        preferredUnits(newUnitValue)
        data['User']['preferredUnit'] = newUnitValue
        
    elif 'imperial' in data['User']['preferredUnit']:
        None
    elif 'metric' in data['User']['preferredUnit']:
        None
    # wtf does this mean??? Bozo
    else:
        None

def main():
    # TODO Create a main menu page. From here, the user can select what they want to do.
    # TODO Add a modification page
    # TODO Create history of user
        ## TODO If the user wants to see history. Pull latest record, otherwise, pull based on their filter (last 7 days, last month, last 3 months, last 6 months, all time.)
    if os.path.exists(os.path.join(cwd, 'data.json')):
        None
    else:
        createUserJsonFile()
    
    lastLogin()
    print("Welcome to the weather app!")
    
    # If its the users first time visiting, run the function, otherwise continue.
    if os.path.exists(os.path.join(cwd, '.env')):
        None
    else:
        newUser()
    
    city_name = str(input("What city would you like to receive weather updates for? Please input a city name or zip code: "))
    getUnitValue()
    # TODO Create a history of cities the user looked up. 
    # TODO Remember the users most recent city. Upon script start up, present them with the weather of that city. 
    # TODO Prompt users with the option to see if they want a weather window to pop up on their screen during laptop startup. 

    cityForecast(city_name, api_key)


if __name__ == '__main__':
    main()