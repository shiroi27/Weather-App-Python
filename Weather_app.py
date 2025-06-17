from tkinter import *
import tkinter as tk
import pytz 
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
from timezonefinder import TimezoneFinder


root = Tk()
root.title("Weather App")
root.attributes("-fullscreen", True)# Make it fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False)) #Press Esc to exit fullscreen 
# root.geometry("1200x700+50+50")  # Width x Height + x_offset + y_offset
# root.resizable(False,False)
root.config(bg="#B3EFF5")


def getWeather():
    city = textfield.get()
    geolocator = Nominatim(user_agent="new")
    location = geolocator.geocode(city)
    if location is None:
        messagebox.showerror("Error", "City not found. Please enter a valid city name.")
        return
    obj=TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    
    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")
    
    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    
    api_key="your api key" #Get your api key from openweatherapi
    api =f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    json_data=requests.get(api).json()
    # print(json_data)
    
    
    # Current weather from first forecast
    current = json_data['list'][0]
    temp = current['main']['temp']
    humidity = current['main']['humidity']
    pressure = current['main']['pressure']
    wind_speed = current['wind']['speed']
    description = current['weather'][0]['description']
    
    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure} hPa")
    w.config(text=f"{wind_speed} m/s")
    d.config(text=f"{description}")
    
    # Daily Forecast - Pick 12:00 PM entries
    daily_data=[]
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)
            
            
    icons = []
    temps = []
    
    for i in range(5):
        if i>=len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        try:
            img = Image.open(f"icon/{icon_code}@2x.png").resize((250,250))
        except FileNotFoundError:
            img = Image.open("icon/default.png").resize((250,250))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'],daily_data[i]['main']['feels_like']))
        
    day_widget = [
        (firstimage,day1,day1temp),
        (secondimage,day2,day2temp),
        (thirdimage,day3,day3temp),
        (fourthimage,day4,day4temp),
        (fifthimage,day5,day5temp)
    ]
    
    for i,(img_label,day_label,temp_label)in enumerate(day_widget):
        if i >= len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image = icons[i]
        temp_label.config(text=f"Day => \n{temps[i][0]}\nNight => \n{temps[i][1]}")
        future_data = datetime.now() + timedelta(days=i)
        day_label.config(text=future_data.strftime("%A"))


#icon
image_icon=PhotoImage(file="Images/logo.png")
root.iconphoto(False,image_icon)

# Designs

image = Image.open("Images/curved logo.png")
resized_image = image.resize((800, 820), Image.LANCZOS)

Round_box = ImageTk.PhotoImage(resized_image)

Label(root,image=Round_box,bg="#B3EFF5").place(x=0,y=0)

# Label

label1=Label(root,text="TEMPERATURE : ",font=('Times New Roman', 40, 'bold'),fg="#000000",bg="#3981BF")
label1.place(x=118,y=170)

label2=Label(root,text="HUMIDITY : ",font=('Times New Roman', 40, 'bold'),fg="#000000",bg="#3981BF")
label2.place(x=126,y=320)

label3=Label(root,text="PRESSURE : ",font=('Times New Roman', 40, 'bold'),fg="#000000",bg="#3981BF")
label3.place(x=154,y=445)

label4=Label(root,text="WIND SPEED : ",font=('Times New Roman', 40, 'bold'),fg="#000000",bg="#3981BF")
label4.place(x=156,y=565)

label5=Label(root,text="DESCRIPTION : ",font=('Times New Roman', 38, 'bold'),fg="#000000",bg="#3981BF")
label5.place(x=160,y=680)

# Search Bar

search_img = Image.open("Images/search bar.png")
search_img = search_img.resize((750, 120), Image.LANCZOS)  # width, height

Search_image = ImageTk.PhotoImage(search_img)

myimage = Label(root, image=Search_image,bg="#B3EFF5")
myimage.place(x=880,y=250)
    
# Search Bar text area
textfield= tk.Entry(root , justify="left", width=13,font=('Times New Roman', 60, 'bold'),bg="#4794BF",borderwidth=0, highlightthickness=0,fg="#000000")
textfield.place(x=1032,y=275)

# Search Button
original_icon = Image.open("Images/Search icon.png")
resized_icon = original_icon.resize((70, 70))

Search_icon = ImageTk.PhotoImage(resized_icon)

myimage_icon = Button(root, image=Search_icon, borderwidth=0, cursor="heart", highlightthickness=0,command=getWeather)
myimage_icon.place(x=915, y=273)


# Bottom Square 1 left
frame = Frame(root, width=880, height=640, bg="#7b9edb")
frame.place(x=770, y=400)  # You can change x and y values as needed

#Boxeswhite
whte_box = Image.open("Images/white box.png")
whte_box = whte_box.resize((200, 620), Image.LANCZOS)

whitebox = ImageTk.PhotoImage(whte_box)

# Place 4 boxes side by side with horizontal spacing
x_start = 777
y_pos = 410
gap = 220  # adjust gap if needed

for i in range(4):
    mybox = Label(root, image=whitebox, bg="#7b9edb")
    mybox.place(x=x_start + i * gap, y=y_pos)

# Keep a reference to the image to prevent garbage collection
root.whitebox = whitebox

# Bottom Square 2 right
frame = Frame(root, width=700, height=220, bg="#7b9edb")
frame.place(x=30, y=818)

#Box1 
frst_box = Image.open("Images/Box1.png")
frst_box = frst_box.resize((695, 185), Image.LANCZOS)

firstbox = ImageTk.PhotoImage(frst_box)

mybox1 = Label(root, image=firstbox, bg="#7b9edb")
mybox1.place(x=30, y=835)  # Slightly lower than frame.y (818) to center vertically


#Box2
scnd_box = Image.open("Images/Box2.png")
scnd_box = scnd_box.resize((880, 165), Image.LANCZOS)

secondbox = ImageTk.PhotoImage(scnd_box)

mybox1 = Label(root, image=secondbox, bg="#B3EFF5")
mybox1.place(x=800, y=50)


#clock
clock=Label(root,font=('Times New Roman', 50, 'bold'), fg="#000000" , bg="#69BACF")
clock.place(x=840,y=100)


#timezone
timezone=Label(root,font=('Times New Roman', 70, 'bold'), fg="#000000", bg="#69BACF")
timezone.place(x= 1100 , y = 70)


#Longitude-Latitude
long_lat=Label(root,font=('Times New Roman', 35, 'bold'), fg="#000000", bg="#69BACF")
long_lat.place(x=1100,y=150)


# Temperature 
t=Label(root,font=('Times New Roman', 40, 'bold'), fg="#000000", bg="#90CDff")
t.place(x=480,y=170)

# Humidity
h=Label(root,font=('Times New Roman', 40, 'bold'), fg="#000000", bg="#3981BF")
h.place(x=380,y=320)

# Pressure
p=Label(root,font=('Times New Roman', 40, 'bold'), fg="#000000", bg="#3981BF")
p.place(x=400,y=445)

# Wind Speed
w=Label(root,font=('Times New Roman', 40, 'bold'), fg="#000000", bg="#3981BF")
w.place(x=450,y=565)

# Description
d=Label(root,font=('Times New Roman', 40, 'bold'), fg="#000000", bg="#3981BF")
d.place(x=465,y=680)


#First Cell

firstframe=Frame(root,width=620, height=137,bg= "#AACCFA")
firstframe.place(x=70, y=860)

firstimage=Label(firstframe,bg="#AACCFA")
firstimage.place(x=-40,y=-55)

day1=Label(firstframe,font=('Times New Roman', 55, 'bold'),bg="#AACCFA",fg="#000000")
day1.place(x=180,y=25)

day1temp=Label(firstframe,font=('Times New Roman', 28, 'bold'),bg="#AACCFA",fg="#000000")
day1temp.place(x=450,y=0)

#Second Cell

secondframe=Frame(root,width=177, height=590,bg= "#ffffff")
secondframe.place(x=790, y=430)

secondimage=Label(secondframe,bg="#ffffff")
secondimage.place(x=-38,y=150)

day2=Label(secondframe,font=('Times New Roman', 33, 'bold'),bg="#ffffff",fg="#000000")
day2.place(x=4,y=70)

day2temp=Label(secondframe,font=('Times New Roman', 35, 'bold'),bg="#ffffff",fg="#000000")
day2temp.place(x=20,y=400)

#Third Cell

thirdframe=Frame(root,width=177, height=590,bg= "#ffffff")
thirdframe.place(x=1012, y=430)

thirdimage=Label(thirdframe,bg="#ffffff")
thirdimage.place(x=-38,y=150)

day3=Label(thirdframe,font=('Times New Roman', 33, 'bold'),bg="#ffffff",fg="#000000")
day3.place(x=4,y=70)

day3temp=Label(thirdframe,font=('Times New Roman', 35, 'bold'),bg="#ffffff",fg="#000000")
day3temp.place(x=20,y=400)

#Fourth Cell 

fourthframe=Frame(root,width=177, height=590,bg= "#ffffff")
fourthframe.place(x=1230, y=430)

fourthimage=Label(fourthframe,bg="#FFFFFF")
fourthimage.place(x=-38,y=150)

day4=Label(fourthframe,font=('Times New Roman', 33, 'bold'),bg="#FFFFFF",fg="#000000")
day4.place(x=4,y=70)

day4temp=Label(fourthframe,font=('Times New Roman', 35, 'bold'),bg="#FFFFFF",fg="#000000")
day4temp.place(x=20,y=400)

#Fifth Cell 

fifthframe=Frame(root,width=177, height=590,bg= "#ffffff")
fifthframe.place(x=1450, y=430)

fifthimage=Label(fifthframe,bg="#ffffff")
fifthimage.place(x=-38,y=150)

day5=Label(fifthframe,font=('Times New Roman', 33, 'bold'),bg="#ffffff",fg="#000000")
day5.place(x=4,y=70)

day5temp=Label(fifthframe,font=('Times New Roman', 35, 'bold'),bg="#ffffff",fg="#000000")
day5temp.place(x=20,y=400)

root.mainloop()
