import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Hotel, DogSitter


def populate():

    hotel_pages = [
        {"hotel_name": "Happy Puppy",
		"address":"234 Great Western Road",
		"city":"Glasgow",
		"picture":"happy_puppy.jpg",
		"phone_number":+14151234567,
		"email":"happy_puppy@gmail.com",
		"available_rooms":15,
		"description":"Our hotel is perfect for small dogs",
		"price_pounds":25,
		},
		{"hotel_name": "Little Paw",
		"address":"131 Argyle Street",
		"city":"Glasgow",
		"picture":"little_paw.jpg",
		"phone_number":+14151234567,
		"email":"little_paw@gmail.com",
		"available_rooms":10,
		"description":"Small dogs, big dogs, old and puppies, all are welcome to stay in out hotel and enjoy the  dog spa.",
		"price_pounds":30,
		},
		{"hotel_name": "Le Chateau Du Chien",
		"address":"18 Wild Street",
		"city":"London",
		"picture":"chateau_du_chien.jpg",
		"phone_number":+14151234567,
		"email":"le_chateau_du_chien@gmail.com",
		"available_rooms":76,
		"description":"The highest rated dog hotel in the UK. ",
		"price_pounds":45,
		},

    ]

    sitter_pages = [

        {"name":"Inna Green",
		 "age":23,
		 "picture":"inna_green.jpg",
		 "bio":"Hello, my name is Inna, I have worked with dogs for 5 years and I would love to take care of your furry best friend  while you are away.",
		 "dog_preference":"S",
		 "availability":" Friday, Saturday, Sunday",
		 "phone number":+14151234567,
		 "price_pounds":20,
		 "city":"London",
		 },
		{"name":"Zoe Jones",
		 "age":32,
		 "picture":"zoe_jones.jpg",
		 "bio":"Hello, my name is Zoe, I have a passion for dogs and a big garden where they can run and play.I work at home so I can take care of you dog whenever you are busy.",
		 "dog_preference":"M",
		 "availability":" All week  except for Sundays.",
		 "phone number":+14151234567,
		 "price_pounds":15,
		 "city":"Edinburgh",
		 },
		 {"name":"John Wilson",
		 "age":65,
		 "picture":"john_wilson.jpg",
		 "bio":"My name is John Wilson and I have taken care of dogs all my life.I have a lot of free time and I will be happy to help you ",
		 "dog_preference":"L",
		 "availability":" All week.",
		 "phone number":+14151234567,
		 "price_pounds":20,
		 "city":"Edinburgh",
		 },
    ]


    cats = {
        "Hotel": {
            "pages": hotel_pages
        },
        "DogSitter": {
            "pages": sitter_pages
        }
    }


    for cat, cat_data in cats.items():
        for p in cat_data["pages"]:
            if cat=="Hotel":
                add_hotel_page( p["hotel_name"],p["address"], p["city"], p["picture"], p["phone_number"],
			p["email"], p["available_rooms"], p["description"], p["price_pounds"])
            else:
                add_sitter_page( p["name"], p["age"], p["picture"], p["bio"], p["dog_preference"], p["availability"],
			p["phone_number"], p["price_pounds"], p["city"])



def add_sitter_page( name, age, picture, bio, dog_preference, availability, phone_number, price_pounds, city):
    p = DogSitter.objects.get_or_create(first_name=name.split(" ")[0], last_name=name.split(" ")[1], age=age, picture=picture, bio=bio,
	dog_preference=dog_preference, availability=availability, phone_number=phone_number, price_per_night=price_pounds, city=city)[0]

    p.save()
    return p

def add_hotel_page(hotel_name, address, city, picture, phone_number, email, available_rooms, description, price):
    p = Hotel.objects.get_or_create(hotel_name=hotel_name,address=address,city=city,picture=picture,
	phone_number=phone_number,email=email, available_rooms=available_rooms,description=description,price=price)[0]
    p.save()
    return p


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    print("population successfull.")
