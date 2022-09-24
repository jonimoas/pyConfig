# pyConfig
 
Console based yml, xml and json file editor

# usage

pyconfig path/to/file.yml

navigate through the keys of the file until a leaf is reached.

The leaf can be edited or deleted.

You can also insert a new field with a value, or a value by itself if in an array.

![Navigate](/navigate.PNG)
![Edit](/edit.PNG)

The following libraries were used:

    asciimatics    - https://github.com/peterbrittain/asciimatics
    dict_deep      - https://github.com/mbello/dict-deep
    PyYAML         - https://github.com/yaml/pyyaml
    xmltodict      - https://github.com/martinblech/xmltodict
