import glob
import datetime
import time
from tkinter import *
from os import *
from multiprocessing import Process
import sys
ptime = datetime.datetime.now()
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import datetime
global filename
import PIL
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
face_names=[]
actualno=1
anm=''
imageno=1
clasim=1
b=0
tim=time.strftime("%H:%M:%S")
from PIL import ImageTk, Image
def findfaces():

    now = datetime.datetime.now()
    currentDate = str(now.month) + "_" + str(now.day) + "_" + str(now.year) + "_" + str(now.timestamp())
    a = []

    def get_encoded_faces():
        """
        looks through the faces folder and encodes all
        the faces

        :return: dict of (name, image encoded)
        """
        encoded = {}

        for dirpath, dnames, fnames in os.walk("./faces"):
            for f in fnames:
                if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                    face = fr.load_image_file("faces/" + f)
                    # face.rotate(90)
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding

        return encoded

    def unknown_image_encoded(img):
        """
        encode a face given the file name
        """
        face = fr.load_image_file("faces/" + img)
        encoding = fr.face_encodings(face)[0]

        return encoding
    global face_names
    def classify_face(im):
        """
        will find all of the faces in a given image and label
        them if it knows what they are

        param im: str of file path
        return: list of face names
        """
        faces = get_encoded_faces()
        faces_encoded = list(faces.values())
        known_face_names = list(faces.keys())
        img = cv2.imread(im, 1)
        # img=imutils.rotate(img, -90)    '''for rotating image by 90 degrees clockwise'''

        face_locations = face_recognition.face_locations(img)
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
        global face_names
        face_names = []
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding, tolerance=0.5)
            name = "Unknown"
            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[
                best_match_index]:  # and a[best_match_index] < 1:   #the 2nd condition is to prevent multiple people from being labelled with the same name
                # Give the detected face the name of the employee that match
                name = known_face_names[best_match_index]
                # a[best_match_index]+=1
            face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if name == "Unknown":
                    # Draw a box around the face
                    cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (20, 100, 0), 2)
                    # Draw a label with a name below the face
                    cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (0, 100, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)
                else:
                    # Draw a box around the face
                    cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (0, 0, 255), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)

        # Display the resulting image

        while True:
            #cv2.imshow(str(face_names) + currentDate + '.jpg', img)
            s=tim+".jpg"
            # save a image using extension
            cv2.imwrite("Processed/"+s, img)
            return face_names
    global anm
    d = os.getcwd()
    global clasim
    anm= "Faces Identified - ", classify_face(str(clasim)+".jpg")
    print(anm, "\n Image saved at location: " + d)
    global b
    b=1




master = Tk()
master.configure(bg='white')
master.title("Main Menu")
frame = Frame(master)
frame.pack()


'''canvas=Canvas(master)
canvas.create_line(925,0,925,1500, dash=(5,2))
canvas.pack(fill=BOTH, expand=True)'''

bottomframe = Frame(master)
bottomframe.pack(side=BOTTOM)
#findfaces()
def window():
    import glob
    import shutil
    from tkinter.filedialog import askopenfilename
    from PIL import ImageTk, Image
    if not path.exists("faces"):
        makedirs("faces")
        print("Directory ", "faces", " Created ")
    else:
        print("Directory ", "faces", " already exists")

    def destroy():
        root.destroy()
    #photo=PhotoImage(file="test.jpg")
    #label=Label(master, image=photo)
    #label.pack()
    def makewindow():
        global root
        root = Toplevel(master)
        root.title("Adding Faces")
        root.geometry("600x300")
        frame = Frame(root)
        frame.pack()
        bottomframe = Frame(root)
        bottomframe.pack(side=BOTTOM)
        from tkinter.filedialog import askopenfilename


        global button
        button = Button(root, text="Choose Image File", fg="white", bg="red", command=getfile)
        button.pack(side=BOTTOM)  # or apply the syntax .place(x=500, y=300) and remove the pack statement
        button1 = Button(root, text="Back", fg="black", bg="white", command=destroy)
        button1.pack(side=RIGHT)
        root.mainloop()

    def refresh():
        root.destroy()
        makewindow()

    def savefile():

        try:
            shutil.copy(filename, "faces", follow_symlinks=True)
        except shutil.SameFileError:
            # code when Exception occur
            pass
        except PIL.UnidentifiedImageError:
            button2.destroy()
            button3.destroy()
            w.destroy()
            m2=Message(root, text="Choose an Image of jpg or jpeg format only")
            m2.pack()
        else:
            # code if the exception does not occur
            pass
        finally:
            button2.destroy()
            button3.destroy()
            w.destroy()
            m = Message(root, text="Image Added Successfully!", )
            m.pack()

    def getfile():
        button.configure(state="disabled")
        global filename
        filename = askopenfilename()
        print(filename)
        labels = []

        for jpeg in glob.glob(filename)[:5]:
            im = Image.open(jpeg)
            im.thumbnail((100, 170), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(im)
            label = Label(root, image=photo)
            label.pack()
            label.img = photo  # *
            # * Each time thru the loop, the name 'photo' has a different
            # photoimage assigned to it.
            # This means that you need to create a separate, 'longer-lived'
            # reference to each photoimage in order to prevent it from
            # being garbage collected.
            # Note that simply passing a photoimage to a Tkinter widget
            # is not enough to keep that photoimage alive.
            labels.append(label)
            global w
            w = Message(root, text="Add this image?", )
            w.pack()
            global button2
            global button3
            button2 = Button(root, text="YES", fg="white", bg="green", command=savefile)
            button2.pack()
            button3 = Button(root, text="NO", fg="white", bg="maroon", command=refresh)
            button3.pack()

    makewindow()
add_faces_button=Button(master,text="Add Faces", fg="white",bg="red",command=window)
add_faces_button.pack(side=BOTTOM)


'''if __name__=='__main__':
    p1 = Process(target = findfaces)
    p1.start()
    time.sleep(15)
    p2 = Process(target = mainloop)
    p2.start()'''

filename="/home/anupam/PycharmProjects/trial/pic.jpg"
print(filename)
labels = []
for jpeg in glob.glob(filename)[:5]:
    im = Image.open(jpeg)
    im.thumbnail((750, 1450), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(im)
    global label
    label = Label(master, image=photo)
    label.pack(side=LEFT)
    label.img = photo  # *
        # * Each time thru the loop, the name 'photo' has a different
        # photoimage assigned to it.
        # This means that you need to create a separate, 'longer-lived'
        # reference to each photoimage in order to prevent it from
        # being garbage collected.
        # Note that simply passing a photoimage to a Tkinter widget
        # is not enough to keep that photoimage alive.
    labels.append(label)
T = Text(master, height=5, width=100)
#T.grid(row=1,column=0,padx=10,pady=10,ipadx=20,ipady=30)
T.pack( pady=70, side=RIGHT)
#time.sleep(3)
T.insert(END,time.strftime("%H:%M:%S -> "+str(anm)))
# Fetch the service account key JSON file contents
cred = credentials.Certificate("credentials.json")
# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'visualtracer-3302a.appspot.com/Profiler',
}, name='storage')
def downloadimage():
    global imageno
    global app
    global cred
    bucket = storage.bucket(app=app)
    blob = bucket.blob(str(imageno)+'.jpg')

    print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))

    # Downloading data from the firebase
    import json
    import urllib.error as error
    import urllib.request as request

    def download_file():
        my_url = str(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
        '''Will have to change this so as to to just be able to use the filename in firebase'''
        global imageno
        global actualno
        try:
            loader = request.urlretrieve(my_url, str(actualno)+".jpg")

        except error.URLError as e:
           ''' message = json.loads(e.read())
            print(message["error"]["message"])'''
           print("why?")
        else:
            print(loader)

            actualno += 1
    download_file()
    imageno+=1
def labelappend():

    global b
    global clasim
    if b==1:

        b=0
        T.insert(END,time.strftime("\n%H:%M:%S -> "+str(anm)))
        filename="/home/anupam/PycharmProjects/trial/Processed/"+tim+".jpg"
        global label
        label.destroy()
        for jpeg in glob.glob(filename)[:5]:
            im = Image.open(jpeg)
            im.thumbnail((750, 1450), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(im)
            label = Label(master, image=photo)
            label.pack(side=LEFT)
            label.img = photo  # *
            # * Each time thru the loop, the name 'photo' has a different
            # photoimage assigned to it.
            # This means that you need to create a separate, 'longer-lived'
            # reference to each photoimage in order to prevent it from
            # being garbage collected.
            # Note that simply passing a photoimage to a Tkinter widget
            # is not enough to keep that photoimage alive.
            labels.append(label)
            findfaces()
            clasim+=1
    downloadimage()

    master.after(3000, labelappend)
labelappend()
findfaces()
clasim+=1
mainloop()
