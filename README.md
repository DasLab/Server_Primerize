<h2>Primerize PCR Assembly Design Server</h2>
#### primerize.stanford.edu / 54.69.129.47
================

This is the repository for **Primerize** PCR primer assembly design server. The release version of the server is freely accessible at [primerize.stanford.edu](http://primerize.stanford.edu).  
<p align="center">
  <img src="res/images/logo_primerize_2.png" alt="Primerize Logo" />
</p>
In brief, the Primerize server uses **CherryPy** framework based on **Python**. It calls **MATLAB** scripts in the [*NA_thermo*](https://github.com/DasLab/Primerize) package for calculation. The front-end uses [*jQuery*](http://jquery.com/) and [*Bootstrap*](http://getbootstrap.com/) javascript libraries.  

To run server, use:  
```python
python run_server.py release/dev
```

For comprehensive documentation, please visit the [`/admin`](http://primerize.stanford.edu/admin) page.

---
by *t47*, May 2015

