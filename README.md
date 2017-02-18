Vise
======

A keyboard driven browser with tabs in a tree. Uses an embedded chromium
instance (via QtWebEngine) for the actual rendering. I got tired of
depending on fragile, cobbled together, poorly integrated solutions based on
mainstream browsers and extensions. Mainstream browsers are designed for lowest
common denominator usage, that is no longer good enough.


Features
----------

Here is a list of features that I intend this browser to have

 * Easy navigation through history by substring matching using the keyboard

 * A tabbed tree browser with drag and drop to group as well as quick access
   via keystrokes to individual tabs

 * The UI is modal, like vim, which means all major UI functions can be quickly
   and easily accessed via single key strokes.

 * Integrated password management with a simple (encrypted) filesystem based storage for
   passwords. That makes it easy to sync between computers using standard file
   syncing tools.

 * Text based configuration files for easy reproducability and syncing of
   settings


Status
--------

vise is fully functional, and I use it as my daily browser. While the code in
vise is fully cross-platform, currently it is only tested on linux, as I don't
have the time/interest to test on other platforms. If you want to install vise
for yourself on linux, you will need the dependencies listed in the
dependencies.txt file and then checkout this repository (I assume below that it
is checked out into the folder `~/work/vise`). Run:

```
rapydscript --js-version 6 --cache-dir ~/work/vise/.build-cache ~/work/vise/client/main.pyj > ~/work/vise/resources/vise-client.js
```

to build the client side JS vise uses. Once that is done, you can run vise
straight out of the source code folder, like this:

```
python3 ~/work/vise
```



Ad blocking
------------

While it was originally my plan to add integrated ad-blocking to vise, I
decided against it, since a better solution is to use either a system-wide (or
better network-wide) hosts blacklist, for example:
https://github.com/StevenBlack/hosts or use a system-wide privacy enabled
proxy, such a privoxy. These solutions have the advantage of working across all
applications, not just the browser.
