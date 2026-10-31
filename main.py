
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.04, 0.05, 0.10, 1)


class MusicHub(App):

    def build(self):
        self.songs = []
        self.filtered_songs = []
        self.current_index = -1
        self.sound = None

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="MUSIC HUB",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=65
        )
        root.add_widget(title)

        subtitle = Label(
            text="Your Music. Your World.",
            font_size=15,
            size_hint_y=None,
            height=30
        )
        root.add_widget(subtitle)

        self.search = TextInput(
            hint_text="Search your songs...",
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.search.bind(text=self.search_songs)
        root.add_widget(self.search)

        self.status = Label(
            text="Welcome to Music Hub",
            size_hint_y=None,
            height=45
        )
        root.add_widget(self.status)

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=8
        )

        scan_btn = Button(text="Scan Download")
        scan_btn.bind(on_press=self.scan_songs)
        buttons.add_widget(scan_btn)

        buttons.add_widget(
            Button(text="Refresh", on_press=self.scan_songs)
        )

        root.add_widget(buttons)

        scroll = ScrollView()

        self.song_list = BoxLayout(
            orientation="vertical",
            spacing=6,
            size_hint_y=None
        )
        self.song_list.bind(
            minimum_height=self.song_list.setter("height")
        )

        scroll.add_widget(self.song_list)
        root.add_widget(scroll)

        self.now_playing = Label(
            text="Now Playing: None",
            size_hint_y=None,
            height=45
        )
        root.add_widget(self.now_playing)

        controls = BoxLayout(
            size_hint_y=None,
            height=65,
            spacing=8
        )

        prev_btn = Button(text="Previous")
        prev_btn.bind(on_press=self.previous_song)
        controls.add_widget(prev_btn)

        self.play_btn = Button(text="Play")
        self.play_btn.bind(on_press=self.toggle_play)
        controls.add_widget(self.play_btn)

        next_btn = Button(text="Next")
        next_btn.bind(on_press=self.next_song)
        controls.add_widget(next_btn)

        root.add_widget(controls)

        footer = Label(
            text="Enjoy Your Music",
            size_hint_y=None,
            height=30
        )
        root.add_widget(footer)

        Clock.schedule_once(self.request_audio_permission, 1)

        return root

    def request_audio_permission(self, dt):
        try:
            from android.permissions import (
                request_permissions,
                Permission
            )

            request_permissions([
                Permission.READ_MEDIA_AUDIO,
                Permission.READ_EXTERNAL_STORAGE
            ])

        except ImportError:
            pass

    def scan_songs(self, instance=None):
        folder = "/storage/emulated/0/Download"

        self.songs = []

        try:
            for filename in os.listdir(folder):
                if filename.lower().endswith(
                    (".mp3", ".wav", ".ogg", ".m4a")
                ):
                    self.songs.append(
                        os.path.join(folder, filename)
                    )

            self.songs.sort()

            self.filtered_songs = list(self.songs)
            self.show_songs()

            self.status.text = (
                f"Found {len(self.songs)} songs"
            )

        except Exception as error:
            self.status.text = (
                "Cannot access Download folder. "
                "Check audio permission."
            )

    def show_songs(self):
        self.song_list.clear_widgets()

        if not self.filtered_songs:
            self.song_list.add_widget(
                Label(
                    text="No songs found",
                    size_hint_y=None,
                    height=60
                )
            )
            return

        for index, path in enumerate(self.filtered_songs):
            name = os.path.basename(path)

            btn = Button(
                text=name,
                size_hint_y=None,
                height=55
            )

            btn.bind(
                on_press=lambda instance, i=index:
                self.play_selected(i)
            )

            self.song_list.add_widget(btn)

    def search_songs(self, instance, value):
        self.filtered_songs = [
            song for song in self.songs
            if value.lower() in os.path.basename(song).lower()
        ]

        self.show_songs()

    def play_selected(self, index):
        path = self.filtered_songs[index]

        self.current_index = self.songs.index(path)
        self.play_song(path)

    def play_song(self, path):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

        self.sound = SoundLoader.load(path)

        if self.sound:
            self.sound.play()
            self.play_btn.text = "Pause"

            self.now_playing.text = (
                "Now Playing: " + os.path.basename(path)
            )

            self.status.text = "Playing Music"

        else:
            self.status.text = "Cannot play this audio format"

    def toggle_play(self, instance):
        if not self.sound:
            if self.songs:
                self.current_index = 0
                self.play_song(self.songs[0])
            else:
                self.status.text = "Scan Download first"
            return

        if self.sound.state == "play":
            self.sound.stop()
            self.play_btn.text = "Play"
        else:
            self.sound.play()
            self.play_btn.text = "Pause"

    def next_song(self, instance):
        if not self.songs:
            self.status.text = "No songs available"
            return

        self.current_index = (
            self.current_index + 1
        ) % len(self.songs)

        self.play_song(self.songs[self.current_index])

    def previous_song(self, instance):
        if not self.songs:
            self.status.text = "No songs available"
            return

        self.current_index = (
            self.current_index - 1
        ) % len(self.songs)

        self.play_song(self.songs[self.current_index])


if __name__ == "__main__":
    MusicHub().run()
