import requests
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import geocoder

class UploadButton(Widget):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    distance = ObjectProperty(None)

    pass
    def update(self,dt):
        self.x += 2
        self.distance.text = str(self.x)
        g = geocoder.ip('me')
        print(g.latlng)
    def start(self):
        Clock.schedule_interval(self.update,2)



    def SendData(self):
        source = requests.get('http://localhost:8000/login/').text
        stat = 'strength'
        steps = '100'
        r0 = requests.get('http://localhost:8000/login/')
        #article = soup.find('div', class_='gel-layout__item gel-1/1')
        #articleLink = article.find('a').text


        client = requests.session()
        client.get('http://localhost:8000/login/')
        csrftoken = client.cookies['csrftoken']
        login_data = {'username':self.username.text,'password':self.password.text, 'csrfmiddlewaretoken':csrftoken}
        r1=client.post('http://localhost:8000/login/',data=login_data)
        print(self.name.text)
        print(r1)
        uploadurl = 'http://localhost:8000/upload/'
        uploadurl += stat
        uploadurl += '/'
        uploadurl += steps
        csrftoken = client.cookies['csrftoken']
        payload={'csrfmiddlewaretoken':csrftoken}
        r2=client.post(uploadurl,data=payload)

        print(r2)

class uploading(App):
    def build(self):
        return UploadButton()
if __name__ == "__main__":
    uploading().run()