import pymongo
from starwars_challenge import Shipdata, Character, Updateship




if __name__=="__main__":
    try:
        client = pymongo.MongoClient()
    except:
        print('failed')
    db = client.starwars # selecting the database
    db_init = Shipdata(db) # initialise the database
    ship_pilot_id = db_init.ship_n_pilots() # returns the ship and pilot
    get_char = Character(db) #initialise new query for names and char _id
    name_id = get_char.names_id_dict() #creates dict for k,v; char name and char id all!
    name_val = Character.convert_dict_name_id(name_id, ship_pilot_id) #compile ship name with object_id for pilots
    
    '''create and update the values'''
    lets_update = Updateship(db) #initialise all updates
    lets_update.create_new_collection("starships") #
    data_api = lets_update.starship_data_api()

    data_sort = []
    for page in range(1, len(data_api)+1):
        data_sort += lets_update.compile_pages_to_data(data_api, page)
    
    collection = db.starships # location for new collection
    lets_update.update_collection(collection, data_sort)
    lets_update.updates_the_pilot_v(name_val,collection) #Replaces values into the db.starship.pilots
