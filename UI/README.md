### This program still has a lot of bugs to work out



# Requirements

```console
sudo apt install python3-pyqt5 python3-pyqt5.qtwebkit python3-mysql.connector
```

# Presentation

This UI is using PyQt5. The file interface.ui was made using QtDesigner. It represents the UI.

Then the interface was converted to a python script using pyuic5: ```pyuic5 interface.ui > UI.py```


# Run it

You just have to install the requirements and the  execute the main.py file: ```python3 main.py```

Make sur that the xbee is connected to your computer.
**WARNING**: Don't forget to change your credential in the UI/main.py file lines 77 to 80.
