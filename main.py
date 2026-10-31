from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.06, 0.06, 0.10, 1)

class MusicHub(App):

    def build(self):
        root = BoxLayout(orientation="vertical", padding=15, spacing=12)

        title = Label(
            text="MUSIC HUB",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=60
        )
        root.add_widget(title)

        search = TextInput(
            hint_text="Search videos and songs...",
            size_hint_y=None,
            height=50,
            multiline=False
        )
        root.add_widget(search)

        scroll = ScrollView()
        content = BoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        sections = [
            "All Videos",
            "All Songs",
            "Latest Videos",
            "Latest Songs",
            "MP3 Player"
        ]

        for section in sections:
            btn = Button(
                text=section,
                size_hint_y=None,
                height=65,
                font_size=18
            )
            content.add_widget(btn)

        scroll.add_widget(content)
        root.add_widget(scroll)

        footer = Label(
            text="Music Hub",
            size_hint_y=None,
            height=35
        )
        root.add_widget(footer)

        return root


if __name__ == "__main__":
    MusicHub().run()
