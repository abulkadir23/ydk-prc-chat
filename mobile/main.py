from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.core.window import Window
from services import APIService
import json

# Ekran boyutunu ayarla
Window.size = (360, 640)

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.api = APIService()
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Logo veya başlık
        title = MDLabel(
            text="Yedek Parça Sistemi",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        
        # Giriş formu
        self.username = MDTextField(
            hint_text="Kullanıcı Adı",
            mode="rectangle",
            size_hint_x=0.8
        )
        
        self.password = MDTextField(
            hint_text="Şifre",
            mode="rectangle",
            password=True,
            size_hint_x=0.8
        )
        
        # Butonlar
        login_btn = MDRaisedButton(
            text="Giriş Yap",
            size_hint_x=0.8,
            on_release=self.login
        )
        
        register_btn = MDRaisedButton(
            text="Kayıt Ol",
            size_hint_x=0.8,
            on_release=self.register
        )
        
        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def login(self, *args):
        def on_success(result):
            self.manager.current = 'home'
        
        def on_error(error):
            dialog = MDDialog(
                title="Hata",
                text=error,
                buttons=[
                    MDRaisedButton(
                        text="Tamam",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        
        self.api.login(
            self.username.text,
            self.password.text,
            on_success,
            on_error
        )
    
    def register(self, *args):
        self.manager.current = 'register'

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.api = APIService()
        
        layout = MDBoxLayout(orientation='vertical')
        
        # Üst menü
        top_bar = MDBoxLayout(size_hint_y=0.1)
        menu_btn = MDRaisedButton(text="Menü")
        logout_btn = MDRaisedButton(text="Çıkış Yap", on_release=self.logout)
        top_bar.add_widget(menu_btn)
        top_bar.add_widget(logout_btn)
        
        # Parça listesi
        self.parts_list = MDList()
        layout.add_widget(top_bar)
        layout.add_widget(self.parts_list)
        
        self.add_widget(layout)
        
        # Parçaları yükle
        self.load_parts()
    
    def load_parts(self):
        def on_success(result):
            self.parts_list.clear_widgets()
            for part in result:
                self.parts_list.add_widget(
                    OneLineListItem(
                        text=part['name'],
                        on_release=lambda x, p=part: self.show_part_details(p)
                    )
                )
        
        def on_error(error):
            dialog = MDDialog(
                title="Hata",
                text=error,
                buttons=[
                    MDRaisedButton(
                        text="Tamam",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        
        self.api.get_parts(on_success, on_error)
    
    def show_part_details(self, part):
        self.manager.get_screen('part_details').set_part(part)
        self.manager.current = 'part_details'
    
    def logout(self, *args):
        self.api.logout()
        self.manager.current = 'login'

class PartDetailsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'part_details'
        self.api = APIService()
        self.current_part = None
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Parça detayları
        self.card = MDCard(
            orientation="vertical",
            padding=20,
            spacing=20,
            size_hint=(1, None),
            height=400
        )
        
        self.name_label = MDLabel(font_style="H5")
        self.price_label = MDLabel()
        self.stock_label = MDLabel()
        
        self.card.add_widget(self.name_label)
        self.card.add_widget(self.price_label)
        self.card.add_widget(self.stock_label)
        
        # Sipariş butonu
        order_btn = MDRaisedButton(
            text="Sipariş Ver",
            on_release=self.order_part
        )
        
        layout.add_widget(self.card)
        layout.add_widget(order_btn)
        
        self.add_widget(layout)
    
    def set_part(self, part):
        self.current_part = part
        self.name_label.text = part['name']
        self.price_label.text = f"Fiyat: {part['price']} TL"
        self.stock_label.text = f"Stok Durumu: {'Mevcut' if part['stock'] > 0 else 'Tükendi'}"
    
    def order_part(self, *args):
        if self.current_part:
            self.manager.get_screen('order').set_part(self.current_part)
            self.manager.current = 'order'

class OrderScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'order'
        self.api = APIService()
        self.current_part = None
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Sipariş formu
        self.quantity = MDTextField(
            hint_text="Miktar",
            mode="rectangle"
        )
        
        self.address = MDTextField(
            hint_text="Teslimat Adresi",
            mode="rectangle",
            multiline=True
        )
        
        order_btn = MDRaisedButton(
            text="Siparişi Tamamla",
            on_release=self.complete_order
        )
        
        layout.add_widget(self.quantity)
        layout.add_widget(self.address)
        layout.add_widget(order_btn)
        
        self.add_widget(layout)
    
    def set_part(self, part):
        self.current_part = part
    
    def complete_order(self, *args):
        if not self.current_part:
            return
            
        def on_success(result):
            dialog = MDDialog(
                title="Başarılı",
                text="Siparişiniz başarıyla oluşturuldu.",
                buttons=[
                    MDRaisedButton(
                        text="Tamam",
                        on_release=lambda x: (dialog.dismiss(), self.manager.current == 'home')
                    )
                ]
            )
            dialog.open()
        
        def on_error(error):
            dialog = MDDialog(
                title="Hata",
                text=error,
                buttons=[
                    MDRaisedButton(
                        text="Tamam",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        
        self.api.create_order(
            self.current_part['id'],
            int(self.quantity.text),
            self.address.text,
            on_success,
            on_error
        )

class ChatbotScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'chatbot'
        self.api = APIService()
        
        layout = MDBoxLayout(orientation='vertical')
        
        # Sohbet alanı
        self.chat_area = MDBoxLayout(orientation='vertical', size_hint_y=0.9)
        
        # Mesaj girişi
        input_area = MDBoxLayout(size_hint_y=0.1, padding=10)
        self.message_input = MDTextField(
            hint_text="Mesajınızı yazın...",
            mode="rectangle"
        )
        send_btn = MDRaisedButton(
            text="Gönder",
            on_release=self.send_message
        )
        
        input_area.add_widget(self.message_input)
        input_area.add_widget(send_btn)
        
        layout.add_widget(self.chat_area)
        layout.add_widget(input_area)
        
        self.add_widget(layout)
    
    def send_message(self, *args):
        message = self.message_input.text
        if not message:
            return
            
        def on_success(result):
            # Kullanıcı mesajını ekle
            self.add_message(message, is_user=True)
            # Chatbot yanıtını ekle
            self.add_message(result['response'], is_user=False)
            self.message_input.text = ""
        
        def on_error(error):
            dialog = MDDialog(
                title="Hata",
                text=error,
                buttons=[
                    MDRaisedButton(
                        text="Tamam",
                        on_release=lambda x: dialog.dismiss()
                    )
                ]
            )
            dialog.open()
        
        self.api.send_chat_message(message, on_success, on_error)
    
    def add_message(self, text, is_user):
        message = MDLabel(
            text=text,
            halign="right" if is_user else "left",
            padding=(10, 10)
        )
        self.chat_area.add_widget(message)

class YedekParcaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        screen_manager = MDScreenManager()
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(HomeScreen())
        screen_manager.add_widget(PartDetailsScreen())
        screen_manager.add_widget(OrderScreen())
        screen_manager.add_widget(ChatbotScreen())
        
        return screen_manager

if __name__ == '__main__':
    YedekParcaApp().run() 