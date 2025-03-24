from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class SparePartsApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Yedek Parça Uygulaması')
        button = Button(text='Parçaları Listele')
        layout.add_widget(label)
        layout.add_widget(button)
        return layout

if __name__ == '__main__':
    SparePartsApp().run() 