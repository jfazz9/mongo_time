import requests

class Shipdata:
    def __init__(self, db):
        self.db = db

    def get_data(self, page_no):
        starship = requests.get(f"https://swapi.dev/api//starships/?page={page_no}")
        if starship.status_code == 200:
            # If the request was successful, process the data
            data_starships = starship.json()
        return data_starships

    #returns the character name and values of the pilot
    def add_to_dict(self, data, pilot_ships):
        for ships in data['results']:
            pilot_ships[ships['name']] = ships['pilots']
        return pilot_ships

    #function to convert the url to a name
    def url_to_name(self, url_pilot_ships):
        for name, value in url_pilot_ships.items():
            if value not in [[], None]:
                for url in range(len(value)):
                    try:
                        person_url = requests.get(value[url])
    #                     if person_url.status_code == 200 or person_url.status_code == 201:
                        all_person_info = person_url.json()
                        url_pilot_ships[name] += [all_person_info['name']]
                    except ValueError:
                        pass
            else:
                url_pilot_ships[name] = []
        return url_pilot_ships

    def clean_urls(self, pilot_dict): # delete the urls from the dictionary after retrieved names
        for name, value in pilot_dict.items():
            if value == []:
                continue
            else:
                for url in range(len(value)//2):
                    if 'http' in value[0]:
                        del pilot_dict[name][0] 
        return pilot_dict

    def ship_n_pilots(self): # returns a dictionary with the ship and pilot names
        pilot_ships = {}
        page =1
        getting_data = True
        while getting_data:
            current_data = self.get_data(page)
            self.add_to_dict(current_data, pilot_ships)
            self.url_to_name(pilot_ships)
            self.clean_urls(pilot_ships)
            if current_data['next'] != None:
                page += 1
            else:
                getting_data = False
        return pilot_ships

class Character(Shipdata):
    def __init__(self, db):
        self.db = db

    def names_id_dict(self): # name key and id is value for that in
        names_dict = {}
        names = self.db.characters.find({}, {"name":1})
        for name in names:
            names_dict[name['name']] = name['_id']
        return names_dict
    
    #the converter for name to id
    def convert_dict_name_id(names_dict, api_dict):
        for k,v in enumerate(api_dict.items()):
            for a in range(len(v[1])):
                for name, i in names_dict.items():
                    if v[1][a] == name:
                        api_dict[v[0]][a] = i
        return api_dict

class Updateship:
    def __init__(self, db):
        self.db = db

    def create_new_collection(self, name):
        self.db.create_collection(name)

# get the data for each page
    def starship_data_api(self):
        data={}
        page =1
        getting_data = True
        while getting_data:
            data[page] = Shipdata.get_data(page)
            if data[page]['next'] != None:
                page += 1
            else:
                getting_data = False
        return data

    #compile pages
    def compile_pages_to_data(self, data, page):
        all_page = []
        for a in data[page]['results']:
            all_page.append(a)
        return all_page

    def update_collection(self, collection, data):
        collection.insert_many(data)

    def updates_the_pilot_v(self, name_val, collection): # takes in the dictionary of names: object_id
        for k,v in name_val.items():
            found = collection.find({"name":k})
            for a in found:
                collection.update_one(
                    {"name":k},
                    {"$set": {"pilots": v}}
                )

# #test object_id
# pilot_id = collection.find({}, {"pilot":1})
# people_ = db.characters.find({}, {"name":1, "_id": 1})
# # for person in people_:
# for idd in pilot_id:
# #         print(person["_id"])
#     print(idd["_id"])
# #         if person["_id"] == idd["_id"]:
# #             print(person["name"])
