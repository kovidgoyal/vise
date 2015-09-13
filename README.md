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

 * Easy navigation through history by sub-sequence matching using the keyboard
   (similar to how you can select files in vim using Command-T or Ctrl-P or
   completion entries using YouCompleteMe).

 * A tabbed tree browser with drag and drop to group as well as quick access
   via keystrokes to individual tabs

 * The UI is modal, like vim, which means all major UI functions can be quickly
   and easily accessed via single key strokes.

 * Integrated password management with simple pluggable backends for local
   storage/networked storage or login information

 * Integrated ad-blocking
