
from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.clearcolor = (0.025, 0.025, 0.055, 1)

PURPLE = (0.48, 0.20, 0.95, 1)
DARK = (0.09, 0.09, 0.16, 1)
WHITE = (1, 1, 1, 1)
GREY = (0.65, 0.65, 0.75, 1)


class VideoDownloader(App):

    def build(self):
        self.title = "Music Video Player"
        self.current_mode = "VIDEO"
        self.current_song = "कोणतेही गाणे निवडलेले नाही"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(55)
        )

        menu = Button(
            text="☰",
            size_hint_x=None,
            width=dp(50),
            font_size=sp(25),
            background_normal="",
            background_color=DARK
        )
        menu.bind(on_press=self.open_menu)

        title = Label(
            text="[b]MUSIC HUB[/b]",
            markup=True,
            font_size=sp(23),
            color=WHITE
        )

        header.add_widget(menu)
        header.add_widget(title)
        root.add_widget(header)

        # Search
        self.search = TextInput(
            hint_text="गाणे किंवा कलाकार शोधा...",
            size_hint_y=None,
            height=dp(48),
            multiline=False,
            background_color=DARK,
            foreground_color=WHITE,
            cursor_color=PURPLE,
            padding=dp(12)
        )
        root.add_widget(self.search)

        search_btn = self.make_button("🔍 SEARCH")
        search_btn.bind(on_press=self.search_song)
        root.add_widget(search_btn)

        # Categories
        root.add_widget(self.heading("Explore Music"))

        categories = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(105)
        )

        for name in [
            "🔥 Latest Hindi",
            "🎵 Old Hindi",
            "🎬 Music Videos",
            "🎧 Audio Songs"
        ]:
            btn = self.make_button(name, DARK)
            btn.bind(
                on_press=lambda b, n=name: self.category(n)
            )
            categories.add_widget(btn)

        root.add_widget(categories)

        # Scrollable songs
        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(9),
            size_hint_y=None
        )
        content.bind(
            minimum_height=content.setter("height")
        )

        content.add_widget(
            self.heading("Popular Hindi Music")
        )

        songs = [
            "Latest Bollywood Music",
            "Romantic Hindi Songs",
            "90s Hindi Songs",
            "Old Bollywood Classics",
            "Hindi Movie Songs",
            "New Music Videos",
            "Instrumental Music",
            "Devotional Music"
        ]

        for song in songs:
            row = BoxLayout(
                size_hint_y=None,
                height=dp(65),
                spacing=dp(8)
            )

            info = Label(
                text="🎵  " + song,
                color=WHITE,
                font_size=sp(14),
                halign="left",
                valign="middle"
            )
            info.bind(
                size=lambda obj, val: setattr(
                    obj, "text_size", val
                )
            )

            play = Button(
                text="▶",
                size_hint_x=None,
                width=dp(55),
                background_normal="",
                background_color=PURPLE
            )

            play.bind(
                on_press=lambda b, s=song: self.select_song(s)
            )

            row.add_widget(info)
            row.add_widget(play)
            content.add_widget(row)

        scroll.add_widget(content)
        root.add_widget(scroll)

        # Player
        player = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(125),
            padding=dp(8),
            spacing=dp(6)
        )

        player.add_widget(
            Label(
                text="[b]NOW PLAYING[/b]",
                markup=True,
                color=PURPLE,
                size_hint_y=None,
                height=dp(25)
            )
        )

        self.song_label = Label(
            text=self.current_song,
            color=WHITE
        )
        player.add_widget(self.song_label)

        controls = BoxLayout(spacing=dp(8))

        video_btn = self.make_button("🎬 VIDEO")
        audio_btn = self.make_button("🎧 AUDIO")

        video_btn.bind(
            on_press=lambda b: self.set_mode("VIDEO")
        )
        audio_btn.bind(
            on_press=lambda b: self.set_mode("AUDIO")
        )

        controls.add_widget(video_btn)
        controls.add_widget(audio_btn)

        player.add_widget(controls)
        root.add_widget(player)

        # Bottom navigation
        nav = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(5)
        )

        for name in ["Home", "Music", "Downloads", "Settings"]:
            btn = self.make_button(name, DARK)
            btn.bind(
                on_press=lambda b, n=name: self.navigation(n)
            )
            nav.add_widget(btn)

        root.add_widget(nav)

        return root

    def heading(self, text):
        return Label(
            text=f"[b]{text}[/b]",
            markup=True,
            color=WHITE,
            font_size=sp(18),
            size_hint_y=None,
            height=dp(38),
            halign="left"
        )

    def make_button(self, text, color=PURPLE):
        return Button(
            text=text,
            color=WHITE,
            font_size=sp(13),
            background_normal="",
            background_color=color
        )

    def message(self, title, msg):
        box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        box.add_widget(
            Label(text=msg, color=WHITE)
        )

        close = self.make_button("OK")
        box.add_widget(close)

        popup = Popup(
            title=title,
            content=box,
            size_hint=(0.88, 0.4)
        )

        close.bind(on_press=popup.dismiss)
        popup.open()

    def select_song(self, song):
        self.current_song = song
        self.song_label.text = song

        self.message(
            "Music Player",
            song + "\n\nगाणे निवडले आहे. अधिकृत Audio/Video स्रोत जोडणे बाकी आहे."
        )

    def set_mode(self, mode):
        self.current_mode = mode

        if mode == "VIDEO":
            self.message(
                "Video Mode",
                "Video Mode निवडला आहे."
            )
        else:
            self.message(
                "Audio Mode",
                "Audio Mode निवडला आहे. अधिकृत Audio Stream जोडणे बाकी आहे."
            )

    def search_song(self, instance):
        query = self.search.text.strip()

        if not query:
            self.message(
                "Search",
                "गाण्याचे नाव लिहा."
            )
            return

        self.message(
            "Music Search",
            "तुमचा शोध: " + query +
            "\n\nअधिकृत Music Search API जोडणे बाकी आहे."
        )

    def category(self, name):
        self.message(
            name,
            "ही Music Category निवडली आहे."
        )

    def navigation(self, name):
        self.message(
            name,
            name + " विभाग निवडला आहे."
        )

    def open_menu(self, instance):
        self.message(
            "Music Hub",
            "Home • Music • Video • Audio • Downloads • Settings"
        )


if __name__ == "__main__":
    VideoDownloader().run()
