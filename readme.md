## Purpose

This is a rewrite of PySimpleGUI v4.

The aim of this rewrite is to clean up the code, fix some bugs and add some new feature.

# State

This project is very much work in progress and in no way finished.

## Changes

Even though the rewrite won't change the overall functionality, there still will be changes to how to manage the GUI.
Unless impossible (like fixing bugs that previously were intentionally kept not to break existing code) I try to keep the package working seemlessly for now.
This meens that any functionality that is deprecated (see below), will work as before but will also print error-messages to stdout with more information on how to move forward.
If you ever encounter a crash, i.e. to a NameError within the package, please let me know.

The part of the rewrite that is probably most noticable to users is moving to pep8 naming conventions and removing (almost) all abbreviations/aliases.
