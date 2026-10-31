
[app]

title = Music Hub
package.name = musichub
package.domain = org.musichub

source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json

version = 2.0

requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_MEDIA_AUDIO,READ_MEDIA_VIDEO

android.api = 35
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
