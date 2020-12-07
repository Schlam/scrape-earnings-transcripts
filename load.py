from pymongo import MongoClient
from datetime import datetime as dt
import os

# Name for mongo database to be created/updated
DATABASE_NAME = 'earnings_call_transcripts'


def connect_database(db_name, port = 27017):

    # URI for database
    URI = f'mongodb://localhost:{port}'

    try:
        
        # Create client
        client = MongoClient(URI)

        # Connect to database
        database = client[db_name]
        print("Successfully connected to database")
        

    except Exception as e:
        
        database = None
        # Handle database connection error
        print(f"{type(e)}: Failed connecting to {URI}\nError message: {e}")
        
    return database

def get_datetime():
    # Get date/time 
    today = dt.today() # today
    date = today.date().strftime('%D') # todays date
    time = today.time().strftime("%H:%M") # current time


    datetime = f'{date}_{time}'

    return datetime

def get_earnings_call_dict(verbose=False):
    
    
    transcripts_by_sector = {}

    for sector in sectors:


        dirname = f"transcripts/{sector}"
        sector_transcripts = os.listdir(dirname)
        earnings_calls = []

        print(f"Writing data for {sector} sector:") if verbose else None

        for transcript in sector_transcripts:

            fname = f"{dirname}/{transcript}"
            ind = transcript.find('_')
            name = transcript[:ind]
            q = transcript[ind+1:-4]


            with open(fname,'r') as f:
                text = f.read()   
            
            earnings_call_obj = {
                "name":name, 
                "quarter":q,
                "transcript":text
            }

            earnings_calls.append(earnings_call_obj)

            print(f"${name}, {q} written") if verbose else None

        transcripts_by_sector[sector] = earnings_calls
        print(f"Finished {sector} data\n") if verbose else None

    print("Finished writing all transcripts")
    
    return transcripts_by_sector

def save_to_database(data, db, time):
    
    
    for sector,earnings_call_objects in data.items():
        
        sector_collection = db[sector]
        sector_collection.insert_one({
            'sector': sector,
            'earnings_calls': earnings_call_objects,
            'time_added': time
        })
        
        
    print("Successfully saved to database")




if __name__ == "__main__":
    
    earnings_call_dict = get_earnings_call_dict(verbose=True)
    earning_call_db = connect_database(DATABASE_NAME)
    datetime = get_datetime()


    save_to_database(
        data = earnings_call_dict,
        db = earning_call_db, 
        time = datetime
    )