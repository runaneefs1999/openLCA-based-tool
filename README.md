# openLCA-based-tool
The openLCA-based tool is a Python script that enables the LCA study of a project captured in an IFC file by creating the necessary processes and products systems in openLCA.

This repository contains a script written in Python language of a possible method for incorporating LCA calculations into a BIM workflow. In particular, it examines a method for calculating the life cycle assessment of a project, captured in an IFC file, with the aid of the openLCA software. The objective of this investigation is to automatically generate the LCA results of a project starting from an IFC file without needing much user input.

However, it should be noted that the LCA study done with tese scripts only considers modules A1 to A3, as defined by EN 15978. Consequently, for a specific project, only the production of the elements is considered. Other modules, such as transport to site or construction and installation processes, require a great deal of specific additional information that is not present in most IFC files. However, the script present in this repository can accommodate the addition of other data sets that can provide this information and allow other modules to be taken into account in the life cycle assessment of the project.

To properly use this tool a connection should be made with the openLCA tool. More particularly the Environmental Footprint (EF) database should be opened in the tool and an IPC server should started.
