import psycopg2

connection = psycopg2.connect(host='localhost',port=5432, database='fyyur', user='postgres', password='aria1828')

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS Venue;')

cursor.execute('''
CREATE TABLE Venue (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    city VARCHAR,
    state VARCHAR,
    address VARCHAR,
    phone VARCHAR,
    image_url VARCHAR,
    facebook_url VARCHAR,
    website VARCHAR,
    seeking_talent BOOLEAN,
    seeking_description VARCHAR);
''')

cursor.execute('''
INSERT INTO Venue (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'The Musical Hop',
    'San Francisco',
    'CA',
    '1015 Folsom Street',
    '123-123-1234',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    'https://www.facebook.com/TheMusicalHop',
    'https://www.themusicalhop.com',
    TRUE,
    'We are on the lookout for a local artist to play every two weeks. Please call us.'
    );

INSERT INTO Venue (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'The Dueling Pianos Bar',
    'New York',
    'NY',
    '335 Delancey Street',
    '914-003-1132',
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    'https://www.facebook.com/theduelingpianos',
    'https://www.theduelingpianos.com',
    FALSE,
    'n/a'
    );

INSERT INTO Venue (
    name,
    city,
    state,
    address,
    phone,
    image_url,
    facebook_url,
    website,
    seeking_talent,
    seeking_description
    )

VALUES (
    'Park Square Live Music & Coffee',
    'San Francisco',
    'CA',
    '34 Whiskey Moore Ave',
    '415-000-1234',
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    'https://www.parksquarelivemusicandcoffee.com',
    FALSE,
    'n/a'
    );
''')


connection.commit()

connection.close()
cursor.close()