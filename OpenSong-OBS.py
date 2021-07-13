import obspython as obs
import math, time
from OSPoller import OSPoller

# Description displayed in the Scripts dialog window
def script_description():
  return """OpenSong-OBS plugin.
This plugin communicates with OpenSong (on the same PC or over the network), and can change the scene depending on the type of slide being shown.
you can select the desired scene for every type of slide being presented."""


# Global variables holding the values of data settings / properties
g = OSPoller('192.168.0.191:8082')
activated     = False
switch_active = False;


# Called to set default values of data settings
def script_defaults(settings):
  obs.obs_data_set_default_string(settings, "scene_song", "")
  obs.obs_data_set_default_string(settings, "scene_bible", "")
  obs.obs_data_set_default_string(settings, "scene_extern", "")
  obs.obs_data_set_default_string(settings, "scene_custom", "")
  obs.obs_data_set_default_string(settings, "source_ip", "127.0.0.1:8082")
  obs.obs_data_set_default_bool(settings, "switch_active", False)


# Fills the given list property object with the names of all sources plus an empty one
def populate_list_property_with_source_names(list_property):
  sources = obs.obs_frontend_get_scenes()
  for i in list_property:
    obs.obs_property_list_clear(i)
  for i in list_property:
    obs.obs_property_list_add_string(i, "", "")
  for i in sources:
    name = obs.obs_source_get_name(i)
    for i in list_property:
      obs.obs_property_list_add_string(i, name, name)
  obs.source_list_release(sources)

# Called to display the properties GUI
def script_properties():
  props = obs.obs_properties_create()

  # enable/disable the script
  p= obs.obs_properties_add_bool(props,"switch_active","Activate automatic switching")

  # Drop-down list of scenes for each slide type
  list_blank = obs.obs_properties_add_list(props, "scene_blank", "Blank slide",  obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  list_song = obs.obs_properties_add_list(props, "scene_song", "Song slide",  obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  list_bible = obs.obs_properties_add_list(props, "scene_bible", "Bible verse", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  list_external = obs.obs_properties_add_list(props, "scene_extern", "Video / External", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  list_custom = obs.obs_properties_add_list(props, "scene_custom", "Custom slide", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)

  #fill the dropdown with actual scene list
  populate_list_property_with_source_names([list_blank,list_song,list_bible,list_external,list_custom])

  #communication settings
  obs.obs_properties_add_text(props, "source_ip", "Opensong IP:Port", obs.OBS_TEXT_DEFAULT)

  return props

def getSceneObject(scene_name):
    scenes = obs.obs_frontend_get_scenes()
    for scene in scenes:
        name = obs.obs_source_get_name(scene)
        if name == scene_name:
            return scene
    obs.source_list_release(scenes) #Necessary?

# Called after change of settings including once after script load
def script_update(settings):
  global switch_active,scene_blank,scene_song,scene_bible,scene_extern,scene_custom
  switch_active = obs.obs_data_get_bool(settings, "switch_active")

  scene_blank = obs.obs_data_get_string(settings, "scene_blank")
  scene_song = obs.obs_data_get_string(settings, "scene_song")
  scene_bible = obs.obs_data_get_string(settings, "scene_bible")
  scene_extern = obs.obs_data_get_string(settings, "scene_extern")
  scene_custom = obs.obs_data_get_string(settings, "scene_custom")

  activate(switch_active)



# Called at script load
def script_load(settings):
  activate(switch_active)

# Called before data settings are saved
def script_save(settings):
  obs.obs_save_sources()

# Called at script unload
def script_unload():
    activate(False)


#poll OpenSong and change scene
def timer_callback():
    slide = g.poll()
    if slide == g.BLANK:
        obs.obs_frontend_set_current_scene(getSceneObject(scene_blank))
    elif slide == g.SONG:
        obs.obs_frontend_set_current_scene(getSceneObject(scene_song))
    elif slide == g.SCRIPTURE:
        obs.obs_frontend_set_current_scene(getSceneObject(scene_bible))
    elif slide == g.EXTERNAL:
        obs.obs_frontend_set_current_scene(getSceneObject(scene_extern))
    elif slide == g.CUSTOM:
        obs.obs_frontend_set_current_scene(getSceneObject(scene_custom))

#start/stop timer
def activate(activating):
    global activated

    if activated != activating:
        activated = activating
        if activating:
          obs.timer_add(timer_callback, 500)
        else:
          obs.timer_remove(timer_callback)
