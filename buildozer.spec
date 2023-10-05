[app]
title = ZuxPingPong
package.name = Zux
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = kivy,python3

orientation = landscape
fullscreen = 1

[buildozer]
android.api = 28
android.ndk_path = /path/to/your/ndk
android.sdk_path = /path/to/your/sdk

[android]
arch = armeabi-v7a
