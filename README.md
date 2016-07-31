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


Ad blocking
------------

While it was originally my plan to add integrated ad-blocking to vise, I
decided against it, since a better solution is to use either a system-wide (or
netter network-wide) hosts blacklist, for example:
https://github.com/StevenBlack/hosts or use a system-wide privacy enabled
proxy, such a privoxy. These solutions have the advantage of working across all
applications, not just the browser.
