# OpenSong-OBS

## What is it:
This is a script for OBS to select a scene based on the slide that is projected in OpenSong.

## Requirements:
The API function must be activated in OpenSong.
Python must be installed (on Windows) to use the script

## Configuration
Configure the IP of the PC that OpenSong runs on (if the PC is the same as OBS, "127.0.0.1" will work)
For each slide type (lyrics, text, bible, blank) a scene can be selected.
when the presenter selects a slide, the scene is changed based on the setting for this type of slide.
the scene is only changed once, so you can manually change.


## Example:
Create in OBS the following scenes with an appropriate name:
* Blank slides: a scene with camera input
* Song slides: a scene with window capture of OBS
* Text slide: camera input with overlay
* Bible: side by side window capture + camera

Configure the above scene in the script and OBS will follow the presentation.