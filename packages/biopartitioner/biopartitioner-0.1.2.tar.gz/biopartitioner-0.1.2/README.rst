
Bio Partitioner 
.. image:: https://github.com/david30907d/bio-partitioner/workflows/Docker%20Image%20CI/badge.svg
   :target: https://github.com/david30907d/bio-partitioner/workflows/Docker%20Image%20CI/badge.svg
   :alt: Docker Image CI

===============================================================================================================================================================================================================================================

Install
-------

For User
^^^^^^^^

``pip install biopartitioner``

For Developer
^^^^^^^^^^^^^


#. Python dependencies:

   #. ``virtualenv venv; . venv/bin/activate``
   #. ``pip install poetry``
   #. ``poetry install``

#. Npm dependencies, for linter, formatter and commit linter (optional):

   #. ``brew install npm``
   #. ``npm ci``

Run
===


#. ``npm run test``
#. You'll see 10 vcf partition files at your folder

Test
----


#. test: ``npm run test``
#. Run all linter before commitment would save some effort: ``npm run check``
