# code-snippets
Did you find yourself search for the same answer in stackotherflow?
Then this is for you!

code-snippets is python program for search instant coding answers and save it fot later use.

## Binary Install
windows users can install the program by running the [setup](https://github.com/matan-h/code-snippets/raw/master/setup/snippets-setup.exe) (made by [inno setup](https://jrsoftware.org/isinfo.php))

or by download [last snippets.exe](https://github.com/matan-h/code-snippets/releases/latest/download/snippets.exe) from [last Release](https://github.com/matan-h/code-snippets/releases/latest)

linux users can download last binary by download [last snippets](https://github.com/matan-h/code-snippets/releases/latest/download/snippets) from [last Release](https://github.com/matan-h/code-snippets/releases/latest)

## Install using pip
 you can install type in terminal:
 ```shell
(sudo) pip install https://github.com/matan-h/code-snippets/archive/master.zip
```
after that,you can open the gui with `python -m code_snippets`. (you can recplace "python" by the python you have (py,python3,py3,etc)) or (if python pip scipts is in your PATH) just run `snippets`



## Gui Usage
after open the software (by run the the the binary file or by run the python module)
you will see:

![Screenshot](https://github.com/matan-h/code-snippets/blob/master/images/Screenshot.png?raw=true)



## Access from python
you can import the `code_snippets` module:
```python
# import the Graphic class
from code_snippets.snippets import Graphic # import Graphic class
# init Graphic - it will init icon,create Graphic object and create hook for open the issue reporter when error occurred
graphic = Graphic()
graphic.main() # start the mainloop of the gui
```
you can also use only the github issue reporter
```python
# import Graphic class,for init the icon
from code_snippets.snippets import Graphic
Graphic.init_icon() # only init the icon,without init the gui
from code_snippets.reporter import open_github_issue
open_github_issue() # open the "Open A GitHub Issue" window
```



## Built With

* [howdoi](https://github.com/gleitz/howdoi) - for searching answers.
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) - for create the gui
## icon
the icon is the <a target="_blank" href="https://icons8.com/icon/awvOcnV6D9iF/code">Code</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

## Author
matan h

## License
This project is licensed under the MIT License.