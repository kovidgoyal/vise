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

 * Integrated ad-blocking
