# ValuePlayerWidget

ValuePlayerWidget is a tool to save and display the different steps of a visualisation. It allows the Player to watch all the steps leading to a final step backward and forward. It is also possible to set an UI : you may either display buttons or a delpy interface (which is a Blockly interface for jupyter).

ValuePlayerWidget takes four parameters for its initialization :
 * 'visualisation' : this parameter is obligatory, it has to be or inheritate from a traitlets object. This will be the visualisation, le Player interacts with.
 * 'UI' : This parameter is optional and set which user interface will be displayed. It is set to None by default. Possible values :
     * None : No user interface
     * 'btn' : display action buttons
     * 'delpy' : display a Delpy interface
 * 'actions' : this parameter is optionnal. It has to be a dictionary of lists. Each key of the dictionnary defines either a column for the buttons UI or a category for the Delpy UI.  This is an example to understand its structure :
     * actions={'category1':[('f1_name',f1,p1,p2), ('f2_name',f2)],'category2':[('f1_name',f1,p3,p4),('f3_name',f3,p5),('f3_name',f3)]}
     
     Each list contains tupples and each tupple defines either a button or a deply method. In this example, we have two categories/columns.
     For each action, we give a tupple t in which we may find at least 2 elements :
         * "fX_name" : the name of the action, it will be displayed on the buttons or become the name of the Delpy method
         * "f1" : the function we wihs to execute
         * args : it is optional, they are arguments to give to the function before it is executed
 * 'language' : this parameter is optionnal and set to 'en_EN' by default. A french version is also available with language='fr_FR'

There are several possibles modes to watch the steps :
* With the sliders : The player may choose which step to display with the "Time" slider and choose the speed with the "Speed" slider
* With the buttons, each butons changes the way to display the step (from the left to the right):
    * Display the first step and pause
    * Display the steps backward or/and increase the speed
    * Display the steps backward with a normal speed
    * Display the previous step and pause
    * Play/Pause
    * Display the next step and pause
    * Display the steps wiath a normal speed
    * Display the steps or/and increase the speed
    * Display the last step and pause
    

Link to the [Demo](https://gitlab.u-psud.fr/edwige.gros/ValuePlayerWidget/blob/master/Demo.ipynb)

Binder : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.u-psud.fr%2Fedwige.gros%2FValuePlayerWidget.git/master?filepath=Demo.ipynb)


Dependencies:
- traitlets
- time
- ipywidgets
- git+https://github.com/Edwauline/DelpyWidget.git@master
 

Install :
```
pip install valueplayerwidget
```

