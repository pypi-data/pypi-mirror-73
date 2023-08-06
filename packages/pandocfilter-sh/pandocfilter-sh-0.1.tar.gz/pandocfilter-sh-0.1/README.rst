Pandocfilters.sh
================

Wrapper package to install `pandocfilters` with an executable.

This allows to install `pandocfilters` with `pipx`:

.. code:: bash

    pipx install pandocfilters-sh

To use with `pandoc`, simply adjust `PYTHONPATH`:

.. code:: bash

    export PYTHONPATH=$(pandocfilters --python)
