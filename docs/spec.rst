======
Caspy 
======

Functional Spec
================

User Experience
----------------
Caspy is a web-based application.  It will be fully AJAX/HTML5 for most
responsive user experience.  Page content will be linked with specific urls
for bookmarking/quick access.  As page content changes, the url will be
updated using HTML5 location API.

Caspy will not implement bookmarking/favorites or back/forward buttons.
This functionality already exists on every modern browser.  By keeping the
location and page content in sync, we allow the browser to do it's job in
this regard.  See `Home Page`_ below for the sole, minor exception to this
rule.

The goal for the Caspy UX is to provide a simple, uncluttered interface
with clear affordances for the functionality available.  Icons may be used
to help convey functionality, but not as a substitute for text.  Caspy's
interface will be language specific, with i18n allowing for translation.
Labels and system messages will be precise but concise.

List Pages
"""""""""""
There are a number of different list pages, which will be presented with a
consistent overall interface and behavior.

Lists will not be paged.  List items will not be editable in place.
Clicking on a list item will navigate to the page for the item or open the
item in an edit pane at the bottom of the window.  A separate edit pane is
particularly important for editing transactions in the register, since it's
extremely useful to be able to scroll the register and view other
transactions while making changes to one transaction.  It should even be
possible to switch the register view between different account while
editing a transaction.

In addition to 'opening' a list item for edit by clicking on it, it will be
possible to *select* list items by clicking in a checkbox to the side of
the the item, (a la Google Mail, django admin, etc.).  Shift-click and
Ctrl-click should behave as expected for selecting a range. (It would be
nice if there were some other ui element which would facilitate selecting
multiple items that could also provide visible and obvious affordance, but
it isn't critical) Action buttons in a pane above the list provide
operations on the selected items: delete, mark as reconciled.

Keyboard Navigation
"""""""""""""""""""""
It will be possible to operate Caspy completely from the keyboard, without
touching the mouse.  Keyboard operation should be reasonably intuitive for
VIM users.  When using keyboard navigation, a highlight along the side of
a list item will indicate the location of the 'cursor.'  When not editing
an entry (insert mode), the interface will be in normal mode, select mode
(equivalent of vim's visual mode), command mode, or search mode.

Possibly allow configurable key-bindings, switch between vim keybindings
and standard windows keybindings (namely CTRL-Z,Y,X,C,V,P,W,N,O), and
perhaps (the horror!) emacs.

Mobile
"""""""
An interface which is simultaneously mobile-friendly would be nice to have.

Undo
""""
Caspy will provide single-stack unlimited undo/redo functionality.

Security
---------
Caspy will provide optional security features.  By default, we assume
it is running on trusted local-area network and does not require user
authentication.  With security setting configured, it will require 
user login.  In this scenario, only books owned (created) by the user or 
to which user is granted permissions will be accessible.  Permission is
boolean--either read/write access or nothing.

Home Page
---------
The home page lists all accessible books in the database and provides the ability
to create a new book or to 'open' an existing book by clicking on it or via
keyboard navigation.

Disconnected Mode
------------------
Would be useful for mobile
