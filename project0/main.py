import argparse

import project0 as p

def main(url):
    # Download data
    incident_data = p.fetchincidents(url)

    # Extract data
    incidents = p.extractincidents(incident_data)
	
    # Create new database
    db = p.createdb()
	
    # Insert data
    p.populatedb(db, incidents)
	
    # Print incident counts
    p.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
