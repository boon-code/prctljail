===================================
prctljail module
===================================

This project is about a simple jail mechanism
on linux (kernel version >= 2.6.23).

.. note:: I'm not completly sure that 
  it's not possibe to easily break this jail.

Feel free to use this little piece of code
(of course, there is no warranty that the 
software works as expected).

If you find any bugs, or want to contribute
you can contact me via email (Manuel.h87@gmail.com)

Status
---------

This version isn't really stable yet. I'm thinking
about reorganizing the JailedProcess class. I will
maybe add a decorator, so that you only have to 
mark an unsafe method and it will automatically be 
wrapped and executed in a seperate process, whenever
it will be called.

Update
----------


.. _here : http://boon-code.github.com/prctljail/

I uploaded the documentation of this project using github pages
(Took me just some minutes until I figured out that I have an empty
file named *.nojekyll*). You can find the docu here_.
