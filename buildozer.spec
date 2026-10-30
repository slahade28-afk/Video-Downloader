[app]

title = Video Downloader
package.name = videodownloader
package.domain = org.mediatools

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 35
android.minapi = 23
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
