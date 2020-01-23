import cv2
import numpy as np
from PIL import Image
import pytesseract
import mysql.connector
from twilio.rest import Client
import os
from mysql.connector import Error
from mysql.connector import errorcode

# try:
#     os.remove("output.jpg")
# except: pass
numberplate = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

previous_text = 'abc'
def detect(gray, original):
    plate = numberplate.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in plate:
        cv2.rectangle(original, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi = gray[y+5:y+h, x+30:x+w-20]
        cv2.imwrite("output.jpg", roi)
    return original

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    original = detect(gray, frame)
    cv2.imshow("Number Plate", original)
    new_text = pytesseract.image_to_string(Image.open("output.jpg"))
    if(new_text != previous_text):
        print("no. plate: " + new_text)
        previous_text = new_text
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="speed_limit"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM riders WHERE Bike_number = %s"
        bike_num = (new_text, )
        mycursor.execute(sql, bike_num)
        myresult = mycursor.fetchall()
        if(myresult):
            for x in myresult:
                Bike_number = x[1]
                Name = x[2]
                Number = x[3]
                Address = x[4]
            try:
                connection = mysql.connector.connect(host="localhost",
                                                     database="speed_limit",
                                                     user="root",
                                                     password="")
                mySql_insert_query = ("""INSERT INTO penalty(Bike_Number, Name, Number, Address) VALUES(%s, %s, %s, %s)""", (Bike_number, Name, Number, Address))

                cursor = connection.cursor()
                cursor.execute(*mySql_insert_query)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into Penalty")
            # cursor.close()

            except mysql.connector.Error as error:
                print("Failed to insert record into Location {}".format(error))

            finally:
                if (connection.is_connected()):
                    connection.close()

            account_sid = ''
            auth_token = ''
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                body="You have crossed the speed limit. You have been fined Rs.500",
                from_='+13073174108',
                to=Number
            )

            print(message.sid)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()