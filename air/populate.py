import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Hotel, DogSitter
from django.contrib.auth.models import User



def populate():

    hotel_users = [
        {"username":"happypuppy",
        "hotel_name": "Happy Puppy",
        "first_name":"Iren",
        "last_name":"Smith",
		"address":"234 Great Western Road",
		"city":"Glasgow",
		"picture":"happy_puppy.jpg",
		"phone_number":+14151234567,
		"email":"happy_puppy@gmail.com",
        "password":"h123456",
		"available_rooms":15,
		"description":"Our hotel is perfect for small dogs",
		"price_pounds":25,
		},
		{"username":"littlepaw",
        "hotel_name": "Little Paw",
        "fist_name":"David",
        "last_name":"Smith",
		"address":"131 Argyle Street",
		"city":"Glasgow",
		"picture":"little_paw.jpg",
		"phone_number":+14151234567,
		"email":"little_paw@gmail.com",
        "password":"l123456",
		"available_rooms":10,
		"description":"Small dogs, big dogs, old and puppies, all are welcome to stay in out hotel and enjoy the  dog spa.",
		"price_pounds":30,
		},
		{"username":"lechateau",
        "hotel_name": "Le Chateau Du Chien",
		"address":"18 Wild Street",
        "first_name":"Clara",
        "last_name":"May",
		"city":"London",
		"picture":"chateau_du_chien.jpg",
		"phone_number":+14151234567,
		"email":"le_chateau_du_chien@gmail.com",
        "password":"c123456",
		"available_rooms":76,
		"description":"The highest rated dog hotel in the UK. ",
		"price_pounds":45,
		},

    ]

    sitter_users = [

        {"username":"inna",
        "password":"i123456",
        "first_name":"Inna",
        "last_name":"Green",
		 "age":23,
		 "picture":"inna_green.jpg",
		 "bio":"Hello, my name is Inna, I have worked with dogs for 5 years and I would love to take care of your furry best friend  while you are away.",
		 "dog_preferences":('S', 'Small'),
         "email":"user@gmail.com",
		 "availability":" Friday, Saturday, Sunday",
		 "phone_number":+14151234567,
		 "price_pounds":20,
		 "city":"London",
		 },
		{"username":"zoe",
        "password":"z123456",
        "first_name":"Zoe",
        "last_name":"Jones",
		 "age":32,
		 "picture":"zoe_jones.jpg",
		 "bio":"Hello, my name is Zoe, I have a passion for dogs and a big garden where they can run and play.I work at home so I can take care of you dog whenever you are busy.",
		  "dog_preferences":('M', 'Medium'),
          "email":"user@gmail.com",
		 "availability":" All week  except for Sundays.",
		 "phone_number":+14151234567,
		 "price_pounds":15,
		 "city":"Edinburgh",
		 },
		 {"username":"john",
         "password":"j123456",
         "first_name":"John",
         "last_name":"Wilson",
		 "age":65,
		 "picture":"john_wilson.jpg",
         "email":"user@gmail.com",
		 "bio":"My name is John Wilson and I have taken care of dogs all my life.I have a lot of free time and I will be happy to help you ",
		 "dog_preferences":('S', 'Small'),
		 "availability":" All week.",
		 "phone_number":+14151234567,
		 "price_pounds":20,
		 "city":"Edinburgh",
		 },
    ]

    for user in sitter_users:
        add_sitter(user)

    for user in hotel_users:
        add_hotel(user)


def add_user(user):
    u = User.objects.get_or_create(username=user["username"], first_name=user["first_name"], last_name =user["last_name"], email=user["email"])[0]
    u.set_password(user["password"])
    u.save()
    print('- New user created/updated:', user['username'])
    return u


def add_sitter(user):
    try:
        newuser = add_user(user)
        sitter = DogSitter.objects.get_or_create(
                user=newuser,
                age=user["age"],
                picture=user["picture"],
                bio=user["bio"],
            	dog_preferences=user["dog_preferences"],
                availability =user["availability"],
                #phone_number=user["phone_number"],
                price_per_night=user["price_pounds"],
                city=user["city"]
                )[0]
        sitter.save()
    except django.db.utils.IntegrityError:
            print("- User "+user["username"]+" already exists.")

def add_hotel(user):
    try:
        newuser = add_user(user)
        hotel = Hotel.objects.get_or_create(
                user=newuser,
                hotel_name=user["hotel_name"],
                address=user["address"],
                city=user["city"],
                picture=user["picture"],
            	#phone_number=user["phone_number"],
                available_rooms=user["available_rooms"],
                description=user["description"],
                price=user["price_pounds"]
                )[0]
        hotel.save()
    except django.db.utils.IntegrityError:
            print("- User "+user["username"]+" already exists.")



if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    print("population successfull.")
