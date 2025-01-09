import os
import shutil
import re
import xml.etree.ElementTree as ET
import mido

name_regex = re.compile('.+ - (.+).mid')
input_folder = "input"
output_folder = "output"
white_key_intervals = [2, 2, 1, 2, 2, 2, 1]
  

def read_midi_file(source_path):
  # make sure this is a MIDI file
  name_match = name_regex.match(source_path)
  if not name_match:
    return

  # get chord names from file name
  chord_names = name_match.group(1).split()

  prog_dict = {}
  chord_count = 0
  trig_note = 60
  chord_notes = []

  midi_file = mido.MidiFile(source_path)
  for msg in midi_file:
    # collect groups of "note on" MIDI messages
    if msg.type == "note_on":
      chord_notes.append(msg.note)

    # when we hit a "note off" MIDI message
    # convert collected "note on" messages into a chord
    elif msg.type == "note_off" and len(chord_notes) > 0:
      # if we have more chords than chord names, something is wrong
      if chord_count > len(chord_names):
        print("!!! Something sus with: " + source_path)

      # create a new mapping: trigger + name + chord
      prog_dict[trig_note] = {}
      prog_dict[trig_note]["notes"] = chord_notes
      prog_dict[trig_note]["name"] = chord_names[chord_count]

      # reset
      # this just puts all the mappings on white keys
      trig_note += white_key_intervals[chord_count % len(white_key_intervals)]
      chord_count += 1
      chord_notes = []
  return prog_dict

# not very interesting, just converting a dict to XML
def write_ripchord_file(prog_dict, dest_path):
  root_tag = ET.Element('ripchord')
  preset_tag = ET.SubElement(root_tag, 'preset')
  for key in prog_dict:
    input_tag = ET.SubElement(preset_tag, 'input')
    input_tag.set('note', str(key))
    chord_tag = ET.SubElement(input_tag, 'chord')
    chord_tag.set('name', prog_dict[key]["name"])
    chord_tag.set('notes', ';'.join(str(x) for x in prog_dict[key]["notes"]))
  tree = ET.ElementTree(root_tag)
  ET.indent(tree)
  os.makedirs(os.path.dirname(dest_path), exist_ok=True)
  tree.write(dest_path, encoding='utf-8', xml_declaration=True)
  

def main():
  # clean output folder
  for filename in os.listdir(output_folder):
    path = os.path.join(output_folder, filename)
    if os.path.isdir(path):
      shutil.rmtree(path)
    elif filename != ".gitkeep":
      os.remove(path)

  # generate files
  for root, dirs, files in os.walk(input_folder):
    for file in files:
      source_path = os.path.join(root, file)

      # split root path
      path_parts = os.path.split(root)
      # filter empty strings
      path_parts = [part for part in path_parts if part]
      # remove input dir
      path_parts = path_parts[1:]
      # replace file extension
      new_name = os.path.splitext(file)[0]+'.rpc'
      # create new file path
      dest_path = os.path.join(output_folder, *path_parts, new_name)

      # Read the MIDI file
      prog_dict = read_midi_file(source_path)
      if prog_dict:
        # Create a new Ripchord preset
        write_ripchord_file(prog_dict, dest_path)

  print("Done")

main()