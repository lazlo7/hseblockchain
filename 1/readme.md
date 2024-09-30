# Requirements to run

In order to properly display tree graphs in networkx, `graphviz` library is used.  
You need to install it on your system (and include it in path, specifically the `dot` processor) if you want to run the notebook yourself, as it is not provided by pip.  

On Arch Linux, you can simply run: `sudo pacman -S graphviz`.  
On Ubuntu, it may be possible to run: `sudo apt-get install graphviz`.  
You can search the package name for your distribution if you are using a different one.  

Python dependencies are listed in the `requirements.txt` file. Use a virtual environment to install them.
