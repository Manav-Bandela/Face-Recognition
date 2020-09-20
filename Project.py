# Importing necessary libraries
import face_recognition
import sqlite3
from PIL import Image, ImageDraw

# Asking user for an input
user_in = input("Enter the image with extension(.jpg/.jpeg/.png): ")
p_2 = face_recognition.load_image_file(user_in)
face_locations = face_recognition.face_locations(p_2)
e_2 = face_recognition.face_encodings(p_2)[0]
pill_image = Image.fromarray(p_2)
print("Searching...")
# Creating Database
conn = sqlite3.connect("Project.db")
cursor = conn.cursor()
# Creation of table
cursor.execute("""
     CREATE TABLE IF NOT EXISTS  people_db
     (name TEXT,image BLOB,status TEXT)""")
# Inserting values into the table
name = "Narendra Modi"
status = "Prime Minister of India"
with open("index.jpeg", "rb") as f:
    image = f.read()
cursor.execute(""" INSERT INTO people_db
     (name, image, status) VALUES (?,?,?)""", (name, image, status))
# Taking values from the database
database = cursor.execute("""
SELECT * FROM people_db
""")
counter = 1
for x in database:
    with open("{}.png".format(counter), "wb") as f:
        f.write(x[1])
        p_1 = face_recognition.load_image_file("{}.png".format(counter))
        e_1 = face_recognition.face_encodings(p_1)[0]
        result = face_recognition.compare_faces([e_1], e_2)
        face_encodings = [e_2]
        draw = ImageDraw.Draw(pill_image)
        if result[0]:
            for ((top, right, bottom, left), e_2) in zip(face_locations, face_encodings):
                draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 0))
                text_width, text_height = draw.textsize(x[0])
                draw.rectangle(((left, bottom - text_height), (right, bottom + 5)), fill=(0, 0, 0), outline=(0, 0, 0))
                draw.text((left + 6, bottom - text_height), x[0], fill=(255, 255, 255, 255))
            del draw
            print("There are {} people in the photo".format(len(face_locations)))
            print("The person found in the photo is {} , {}".format(x[0], x[2]))
            break
        counter = counter + 1

conn.commit()
cursor.close()
conn.close()
# Displaying and saving the result
pill_image.show()
pill_image.save("Result.jpg")
