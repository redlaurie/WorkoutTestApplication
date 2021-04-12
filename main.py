import requests
from math import sin, cos, sqrt, atan2, radians
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.utils import platform
import plyer
import json
from plyer import gps
class UploadButton(Widget):
    f = 0.0
    g = 0.0
    value = 0.0
    R = 6373.0
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    distance = ObjectProperty(None)

    #gps.start(500, 0)

    pass
    def request_android_permissions(self):

        try:
            from android.permissions import request_permissions, Permission
            try:
                request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION])
            except:
                self.password.text = "permission denied"
        except:
            self.password.text = "permission denied"
    def update(self,dt):
        try:
            gps.configure(on_location=self.on_gps_location,on_status=self.on_status)
        except:
            print("fail")
            self.password.text = "fail"

        if platform == "android":
            self.request_android_permissions()
        else:
            self.password.text = "not android device"
    def on_gps_location(self,**kwargs):
        try:
            lat = kwargs.get("lat")
            lon = kwargs.get("lon")
            print(lat,lon)

            try:
                if self.g == 0.0:
                    self.g = float(lat)
                    self.f = float(lon)

                else:

                    dlon = float(lon) - self.f
                    dlat = float(lat) - self.g
                    a = sin(dlat / 2)**2 + cos(self.g) * cos(lat) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    self.value = self.value + self.R*c
                    self.f = float(lan)
                    self.g = float(lat)

                    self.distance.text = str(self.value)
            except:
                print("something went wrong")
        except:
            print("failed")

    def on_status(self,stype,status):
        print(status)




    def start(self):
        Clock.schedule_interval(self.update,2)
        try:
            gps.start(1000,0)

        except:
            print("failed")


    def SendData(self):
        source = requests.get('http://----/login/').text
        stat = 'dexterity'
        steps = '100'
        r0 = requests.get('http://----/login/')
        #article = soup.find('div', class_='gel-layout__item gel-1/1')
        #articleLink = article.find('a').text


        client = requests.session()
        client.get('http://----/login/')
        csrftoken = client.cookies['csrftoken']
        login_data = {'username':self.username.text,'password':self.password.text, 'csrfmiddlewaretoken':csrftoken}
        r1=client.post('http://---/login/',data=login_data)

        print(r1)
        uploadurl = 'http://----/upload/'
        uploadurl += stat
        uploadurl += '/'
        uploadurl += steps
        csrftoken = client.cookies['csrftoken']
        payload={'csrfmiddlewaretoken':csrftoken}
        r2=client.post(uploadurl,data=payload)
        data = r2.json()
        returning = data.get('dexterity')
        print(returning)
        print(r2.text)
        id = returning['dex'][0]
        print(r2)

        print(id)
class uploading(App):
    def build(self):
        return UploadButton()
if __name__ == "__main__":
    uploading().run()