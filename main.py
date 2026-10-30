
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

Window.clearcolor = (0.035, 0.035, 0.035, 1)

WHITE = (1, 1, 1, 1)
GREY = (0.68, 0.68, 0.68, 1)
DARK = (0.10, 0.10, 0.10, 1)
RED = (0.95, 0.08, 0.08, 1)
PURPLE = (0.48, 0.25, 0.95, 1)


class VideoDownloader(App):

    def build(self):
        self.title = "Video Downloader"
        self.category_name = "All"

        self.videos = [
            ("Heeriye", "Jasleen Royal ft. Arijit Singh",
             "4:37", "Music", (0.20, 0.35, 0.40, 1)),
            ("Kesariya", "Arijit Singh",
             "3:36", "Hindi", (0.55, 0.25, 0.08, 1)),
            ("Raanjhan", "Do Patti",
             "3:50", "Trending", (0.35, 0.20, 0.15, 1)),
            ("Tum Se", "Darshan Raval",
             "4:06", "Music", (0.18, 0.30, 0.45, 1)),
            ("Sajni", "Arijit Singh",
             "4:57", "Hindi", (0.50, 0.32, 0.15, 1)),
            ("Aaj Ki Raat", "Sachin-Jigar",
             "3:10", "Trending", (0.30, 0.12, 0.20, 1)),
            ("Marathi Hits", "Marathi Music",
             "5:20", "Marathi", (0.35, 0.20, 0.10, 1)),
            ("Old Is Gold", "90s Classic Songs",
             "4:30", "Marathi", (0.20, 0.25, 0.30, 1)),
        ]

        self.root_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            padding=(dp(10), dp(5), dp(10), dp(5))
        )

        self.show_home()
        return self.root_layout

    def make_button(self, text, color=DARK, height=42):
        return Button(
            text=text,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_color=color,
            color=WHITE,
            font_size=sp(14)
        )

    def make_label(self, text, size=14, color=WHITE):
        return Label(
            text=text,
            font_size=sp(size),
            color=color,
            halign="left",
            valign="middle"
        )

    def show_home(self):
        self.root_layout.clear_widgets()

        # TOP HEADER
        header = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8)
        )

        logo = self.make_button("▶", RED, 42)
        logo.size_hint_x = None
        logo.width = dp(48)

        heading = Label(
            text="[b]Video Downloader[/b]",
            markup=True,
            font_size=sp(20),
            color=WHITE,
            halign="left"
        )

        search_icon = self.make_button("⌕", DARK, 42)
        search_icon.size_hint_x = None
        search_icon.width = dp(42)
        search_icon.bind(on_press=self.focus_search)

        header.add_widget(logo)
        header.add_widget(heading)
        header.add_widget(search_icon)

        self.root_layout.add_widget(header)

        # SEARCH BAR
        self.search = TextInput(
            hint_text="Search videos, songs or artists...",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            background_color=(0.13, 0.13, 0.13, 1),
            foreground_color=WHITE,
            hint_text_color=GREY,
            cursor_color=RED,
            padding=dp(12)
        )

        self.search.bind(text=self.search_changed)
        self.root_layout.add_widget(self.search)

        # CATEGORY BAR
        category_scroll = ScrollView(
            size_hint_y=None,
            height=dp(44),
            do_scroll_y=False,
            do_scroll_x=True
        )

        categories = GridLayout(
            rows=1,
            spacing=dp(7),
            size_hint=(None, 1),
            width=dp(650)
        )

        category_names = [
            "All", "Music", "Marathi",
            "Hindi", "English", "Trending"
        ]

        for name in category_names:
            color = RED if name == self.category_name else DARK

            btn = self.make_button(name, color, 40)
            btn.size_hint_x = None
            btn.width = dp(95)

            btn.bind(
                on_press=lambda b, n=name: self.change_category(n)
            )
            categories.add_widget(btn)

        category_scroll.add_widget(categories)
        self.root_layout.add_widget(category_scroll)

        # VIDEO FEED
        self.scroll = ScrollView(
            do_scroll_x=False
        )

        self.feed = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )

        self.feed.bind(
            minimum_height=self.feed.setter("height")
        )

        self.scroll.add_widget(self.feed)
        self.root_layout.add_widget(self.scroll)

        self.refresh_feed()

        # BOTTOM NAVIGATION
        nav = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            spacing=dp(4)
        )

        items = [
            ("⌂\nHome", "Home"),
            ("▷\nShorts", "Shorts"),
            ("⊕\nCreate", "Create"),
            ("▣\nSubscriptions", "Subscriptions"),
            ("▤\nLibrary", "Library")
        ]

        for text, name in items:
            btn = Button(
                text=text,
                background_normal="",
                background_color=DARK,
                color=WHITE,
                font_size=sp(11)
            )
            btn.bind(
                on_press=lambda b, n=name: self.navigation(n)
            )
            nav.add_widget(btn)

        self.root_layout.add_widget(nav)

    def refresh_feed(self):
        self.feed.clear_widgets()

        query = self.search.text.strip().lower()

        for video in self.videos:
            title, artist, duration, category, color = video

            if self.category_name != "All":
                if category != self.category_name:
                    continue

            if query:
                if query not in title.lower() and query not in artist.lower():
                    continue

            self.add_video_card(video)

        if len(self.feed.children) == 0:
            self.feed.add_widget(
                Label(
                    text="No videos found.\nTry another search.",
                    color=GREY,
                    size_hint_y=None,
                    height=dp(100)
                )
            )

    def add_video_card(self, video):
        title, artist, duration, category, color = video

        card = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(125),
            spacing=dp(8)
        )

        # VIDEO THUMBNAIL
        thumbnail = BoxLayout(
            orientation="vertical",
            size_hint_x=0.46,
            padding=dp(5)
        )

        thumb_button = Button(
            text="[b]▶[/b]\n" + title,
            markup=True,
            background_normal="",
            background_color=color,
            color=WHITE,
            font_size=sp(16)
        )

        thumb_button.bind(
            on_press=lambda b, v=video: self.open_player(v)
        )

        thumbnail.add_widget(thumb_button)

        # VIDEO INFORMATION
        info = BoxLayout(
            orientation="vertical",
            spacing=dp(3)
        )

        name = Label(
            text="[b]" + title + "[/b]",
            markup=True,
            color=WHITE,
            font_size=sp(15),
            halign="left",
            valign="middle",
            size_hint_y=0.36
        )

        channel = Label(
            text=artist,
            color=GREY,
            font_size=sp(11),
            halign="left",
            valign="middle",
            size_hint_y=0.25
        )

        details = Label(
            text="Video • " + category,
            color=GREY,
            font_size=sp(11),
            halign="left",
            valign="middle",
            size_hint_y=0.20
        )

        duration_label = Label(
            text=duration,
            color=WHITE,
            font_size=sp(11),
            size_hint_y=0.19
        )

        info.add_widget(name)
        info.add_widget(channel)
        info.add_widget(details)
        info.add_widget(duration_label)

        card.add_widget(thumbnail)
        card.add_widget(info)

        self.feed.add_widget(card)

    def change_category(self, name):
        self.category_name = name
        self.show_home()

    def search_changed(self, instance, value):
        self.refresh_feed()

    def focus_search(self, instance):
        self.search.focus = True

    def open_player(self, video):
        title, artist, duration, category, color = video

        self.root_layout.clear_widgets()

        # PLAYER HEADER
        header = BoxLayout(
            size_hint_y=None,
            height=dp(48)
        )

        back = self.make_button("← Back", DARK)
        back.size_hint_x = None
        back.width = dp(85)
        back.bind(on_press=lambda b: self.show_home())

        header.add_widget(back)
        header.add_widget(
            self.make_label("Video Player", 18)
        )

        self.root_layout.add_widget(header)

        # VIDEO SCREEN
        screen = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(230),
            padding=dp(10),
            spacing=dp(8)
        )

        screen.add_widget(
            Label(
                text="▶",
                font_size=sp(65),
                color=WHITE
            )
        )

        screen.add_widget(
            Label(
                text="Video stream जोडणे बाकी आहे",
                color=GREY,
                font_size=sp(14)
            )
        )

        screen.add_widget(
            Label(
                text="Official video source आवश्यक आहे",
                color=GREY,
                font_size=sp(11)
            )
        )

        self.root_layout.add_widget(screen)

        self.root_layout.add_widget(
            Label(
                text="[b]" + title + "[/b]",
                markup=True,
                color=WHITE,
                font_size=sp(20),
                size_hint_y=None,
                height=dp(45)
            )
        )

        self.root_layout.add_widget(
            Label(
                text=artist + "\n" + category,
                color=GREY,
                font_size=sp(14),
                size_hint_y=None,
                height=dp(55)
            )
        )

        # PLAYER CONTROLS
        controls = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(8)
        )

        for text in ["⏮", "▶", "⏭", "⛶"]:
            controls.add_widget(
                self.make_button(text, DARK)
            )

        self.root_layout.add_widget(controls)

        note = Label(
            text="अधिकृत Video Streaming API जोडल्यावरच\nखरे व्हिडिओ येथे प्ले होतील.",
            color=GREY,
            font_size=sp(12)
        )

        self.root_layout.add_widget(note)

        home = self.make_button("HOME", RED)
        home.bind(on_press=lambda b: self.show_home())
        self.root_layout.add_widget(home)

    def navigation(self, name):
        if name == "Home":
            self.category_name = "All"
            self.show_home()
        else:
            self.message(
                name,
                name + " विभाग पुढील टप्प्यात तयार करू."
            )

    def message(self, title, text):
        popup = Popup(
            title=title,
            content=Label(
                text=text,
                color=WHITE
            ),
            size_hint=(0.85, 0.35)
        )
        popup.open()


if __name__ == "__main__":
    VideoDownloader().run()

