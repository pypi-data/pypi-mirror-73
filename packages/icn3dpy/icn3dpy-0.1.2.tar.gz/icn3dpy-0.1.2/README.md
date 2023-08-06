icn3dpy
=======

A simple [IPython/Jupyter](http://jupyter.org/) widget to
embed an interactive [iCn3D](https://github.com/ncbi/icn3d) viewer in a notebook.

The widget is completely static, which means the viewer doesn't need a running
IPython kernel to be useful and web pages and presentations generated from
the notebook will work as expected.  However, this also means there is only
one-way communication between the notebook and the viewer.

If you experience problems, please file 
an [issue](https://github.com/ncbi/icn3d/issues).


Installation
------------

From PyPI:

    pip install icn3dpy


*Important:* In order to use with JupyterLab you must install the JupyterLab extension:

    jupyter labextension install jupyterlab_3dmol



Usage
-----

Open a notebook

    jupyter notebook

and issue

```Python
import icn3dpy
view = icn3dpy.view(q='mmdbid:1tup',command='color spectrum')
view
view = icn3dpy.view(q='mmdbid:6m0j',command='line+graph+interaction+pairs+%7C+!A+!E+%7C+hbonds,salt+bridge,interactions,halogen,pi-cation,pi-stacking+%7C+false+%7C+threshold+3.8+6+4+3.8+6+6;+show+selection;+add+residue+number+labels%7C%7C%7C%7B"factor":"1.4817","mouseChange":%7B"x":0,"y":0%7D,"quaternion":%7B"_x":"0.036185","_y":"0.49963","_z":"0.078595","_w":"0.86191"%7D%7D')
view
```

Command
---

All [iCn3D commands](https://www.ncbi.nlm.nih.gov/Structure/icn3d/icn3d.html#commands) work.


License
-------

United States Government Work
