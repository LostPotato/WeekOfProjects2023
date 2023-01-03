# creating the request function that will interact
# with the api
from functools import lru_cache
import requests
from time import sleep
from tqdm import tqdm

base_url = 'https://nominatim.openstreetmap.org/search?'

# wrapping the function in a cache function to allow
# for local acess of data
@lru_cache(maxsize=2000)
def nominatim_geocode(address = None    , format='json', limit=1, prints = True, **kwargs):
    '''thin wrapper around nominatim API.
    Documentation: https://wiki.openstreetmap.org/wiki
    /Nominatim#Parameters
    '''
    
    # setting the parameters for the request
    params = {
        "q": address,
        "format": format,
        "limit": limit,
        **kwargs
    }
    
    # send the get request
    response = requests.get(base_url, params=params)
    #check for a valid response
    response.raise_for_status
    
    #sleeping so we don't get in trouble
    sleep(1)
    
    if prints:
        print(response.json())
    # returning the response in a parsed json
    return response.json()

# using the csv library
from csv import DictReader, DictWriter

def read_csv(path:str):
    """read csv and return it as a list of dictonaries

    Args:
        path (str): this is the file path to csv
    """
    
    # opening and writing to the csv
    with open(path, 'r') as f:
        return list(DictReader(f))

def write_csv(data, path, mode='w'):
    """Write data to csv

    Args:
        data (dict): data dictonary to be written to csv
        path (str): this is the path to new csv
        mode (str, optional): _description_. Defaults to 'w'.

    Raises:
        ValueError: The value for mode is not correct
    """
    
    # Raise error if there isn't a valid write mode
    if mode not in 'wa':
        raise ValueError("mode should be either 'w' or 'a'")
    
    # opens / creates the file and writes to the csv
    with open(path, mode) as f:
        writer = DictWriter(f, fieldnames=data[0].keys())
        if mode == 'w':
            writer.writeheader() 

        for row in data:
            writer.writerow(row)  

def geocode_bulk(data, column='address', verbose=False):
    """assuming all of the data is an iterable of dicts,
    this will attempt to geocode each of them, treating {column}
    as and address

    Args:
        data (dict): dictonary of address
        column (str, optional): column to search on. Defaults to 'address'.
        verbose (bool, optional): displays extra data. Defaults to False.
    """
    result, errors = [], []
    for row in tqdm(data):
            try:
                search = nominatim_geocode(row[column], limit=1, prints=False)
                if len(search) == 0: # no location found:
                    result.append(row)
                    if verbose:
                        print(f"Can't find anything for {row[column]}")
                        
                else:
                    info = search[0] # most "important" result
                    info.update(row) # merge two dicts
                    result.append(info) 
            except Exception as e:
                if verbose:
                    print(e)
                row['error'] = e
                errors.append(row)
        
    if len(errors) > 0 and verbose:
        print(f'{len(errors)}/{len(data)} rows failed')

    return result, errors

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    # define a 'subcommand' for each function
    subparsers = parser.add_subparsers(dest='subcommand')

    # add a 'read' subcommand for the read_csv function
    read_parser = subparsers.add_parser('read', help='read a csv file')
    read_parser.add_argument('input_file', help='the input file to read')

    # add a 'write' subcommand for the write_csv function
    write_parser = subparsers.add_parser('write', help='write data to a csv file')
    write_parser.add_argument('output_file', help='the output file to write to')
    write_parser.add_argument('data', help='the data to write, in the form of a list of dictionaries')

    # add a 'geocode' subcommand for the geocode_bulk function
    geocode_parser = subparsers.add_parser('geocode_bulk', help='geocode a list of addresses')
    geocode_parser.add_argument('data', help='the data to geocode, in the form of a list of dictionaries')
    geocode_parser.add_argument('--column', help='the column to search on', default='address')
    geocode_parser.add_argument('--verbose', help='display extra data', action='store_true')
    
    # adding a 'nomination_geocode' for single addresses
    geocode_parser = subparsers.add_parser('nominatim_geocode', help='geocode an address using the nominatim API')
    geocode_parser.add_argument('address', help='the address to geocode')
    geocode_parser.add_argument('--format', help='the format of the response (json or xml)', default='json')
    geocode_parser.add_argument('--limit', help='the maximum number of results to return', default=1, type=int)

    args = parser.parse_args()

    # add a 'nomination' 

    # check which subcommand was called and call the corresponding function
    if args.subcommand == 'read':
        data = read_csv(args.input_file)
        print(data)
    elif args.subcommand == 'write':
        write_csv(args.data, args.output_file)
    elif args.subcommand == 'geocode':
        result, errors = geocode_bulk(args.data, column=args.column, verbose=args.verbose)
        print(result)
    elif args.subcommand == 'nominatim_geocode':
        response = nominatim_geocode(args.address, format=args.format, limit=args.limit)
