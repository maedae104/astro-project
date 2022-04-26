"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
import crud
import model
import server

os.system("dropdb transits")
os.system('createdb transits')

model.connect_to_db(server.app)
model.db.create_all()


for n in range(10):
    email = f'user{n}@test.com' 
    password = 'test'
    phone_number = 707-484-9110

    user = crud.create_user(email, password, phone_number)
    model.db.session.add(user)


model.db.session.commit()