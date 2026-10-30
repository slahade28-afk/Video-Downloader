from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.035, 0.035, 0.075, 1)

PURPLE = (0.48, 0.20, 0.95, 1)
DARK = (0.075, 0.075, 0.14, 1)
WHITE = (1, 1, 1, 1)
GREY = (0.65, 0.65, 0.75, 1)


class VideoDownloader(App):

    def build(self):
        self.title = "Video Downloader"

        self.root_box = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(55)
        )

        menu = Button(
            text="☰",
            font_size=sp(27),
            size_hint_x=None,
            width=dp(55),
            background_normal="",
            background_color=DARK
        )
        menu.bind(on_press=self.open_menu)

        title = Label(
            text="[b]VIDEO DOWNLOADER[/b]",
            markup=True,
            font_size=sp(20),
            color=WHITE
        )

        header.add_widget(menu)
        header.add_widget(title)
        self.root_box.add_widget(header)

        # Subtitle
        self.root_box.add_widget(Label(
            text="Download • Convert • Enjoy",
            color=GREY,
            size_hint_y=None,
            height=dp(25)
        ))

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(14),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # URL input
        content.add_widget(self.heading("Paste Video Link"))

        self.url_input = TextInput(
            hint_text="Paste your video URL here...",
            size_hint_y=None,
            height=dp(52),
            multiline=False,
            background_color=DARK,
            foreground_color=WHITE,
            cursor_color=PURPLE,
            padding=dp(12)
        )
        content.add_widget(self.url_input)

        # Quality
        content.add_widget(self.heading("Video Quality"))

        self.quality = Spinner(
            text="Auto Quality",
            values=(
                "Auto Quality",
                "144p", "240p", "360p", "480p",
                "720p HD", "1080p Full HD",
                "2K", "4K", "8K", "16K"
            ),
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=PURPLE,
            color=WHITE
        )
        content.add_widget(self.quality)

        # Audio quality
        content.add_widget(self.heading("Audio Quality"))

        self.audio = Spinner(
            text="320 kbps",
            values=(
                "64 kbps", "128 kbps", "192 kbps",
                "256 kbps", "320 kbps", "FLAC"
            ),
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=DARK,
            color=WHITE
        )
        content.add_widget(self.audio)

        # Download button
        download = Button(
            text="⬇  DOWNLOAD NOW",
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=PURPLE,
            font_size=sp(17),
            bold=True
        )
        download.bind(on_press=self.start_download)
        content.add_widget(download)

        # Feature cards
        content.add_widget(self.heading("Explore Features"))

        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            row_default_height=dp(100),
            row_force_default=True
        )
        grid.bind(minimum_height=grid.setter("height"))

        features = [
            ("🎬", "Video Downloader"),
            ("🎵", "MP3 Downloader"),
            ("🔄", "Video to MP3"),
            ("▶", "YouTube"),
            ("📥", "Download Manager"),
            ("🎧", "Music Player"),
            ("📂", "Download History"),
            ("⚙", "Settings")
        ]

        for icon, name in features:
            btn = Button(
                text=f"{icon}\n{name}",
                font_size=sp(15),
                background_normal="",
                background_color=DARK,
                color=WHITE
            )
            btn.bind(
                on_press=lambda instance, n=name: self.feature(n)
            )
            grid.add_widget(btn)

        content.add_widget(grid)

        # Bottom information
        content.add_widget(Label(
            text="Fast • Simple • Powerful",
            color=PURPLE,
            size_hint_y=None,
            height=dp(45)
        ))

        scroll.add_widget(content)
        self.root_box.add_widget(scroll)

        # Bottom navigation
        nav = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(5)
        )

        for name in ["Home", "Downloads", "Convert", "Settings"]:
            btn = Button(
                text=name,
                font_size=sp(12),
                background_normal="",
                background_color=DARK
            )
            btn.bind(
                on_press=lambda instance, n=name: self.feature(n)
            )
            nav.add_widget(btn)

        self.root_box.add_widget(nav)

        return self.root_box

    def heading(self, text):
        return Label(
            text=f"[b]{text}[/b]",
            markup=True,
            color=WHITE,
            font_size=sp(17),
            size_hint_y=None,
            height=dp(38),
            halign="left"
        )

    def message(self, title, msg):
        popup = Popup(
            title=title,
            content=Label(
                text=msg,
                color=WHITE
            ),
            size_hint=(0.85, 0.35)
        )
        popup.open()

    def start_download(self, instance):
        url = self.url_input.text.strip()

        if not url:
            self.message(
                "Video Downloader",
                "Please paste a video link first."
            )
            return

        if not url.startswith(("https://", "http://")):
            self.message(
                "Invalid Link",
                "Please enter a valid URL."
            )
            return

        self.message(
            "Download Setup",
            "Link received. Actual downloading will be added in the next development step."
        )

    def feature(self, name):
        self.message(
            name,
            name + " feature selected."
        )

    def open_menu(self, instance):
        options = [
            "Home",
            "Video Downloader",
            "MP3 Downloader",
            "Video to MP3",
            "YouTube",
            "Download Manager",
            "Download History",
            "Settings",
            "About"
        ]

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            padding=dp(10)
        )

        for option in options:
            btn = Button(
                text=option,
                background_normal="",
                background_color=DARK,
                color=WHITE
            )
            btn.bind(
                on_press=lambda b, n=option: (
                    self.feature(n),
                    popup.dismiss()
                )
            )
            layout.add_widget(btn)

        popup = Popup(
            title="VIDEO DOWNLOADER MENU",
            content=layout,
            size_hint=(0.85, 0.8)
        )
        popup.open()


if __name__ == "__main__":
    VideoDownloader().run()
