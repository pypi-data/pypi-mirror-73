Working with Front-end Code
===========================

Front-end Grains
~~~~~~~~~~~~~~~~

Cob recognizes grains dedicated to front-end components, and offers
tailored handling for them. The exact behavior depends on the type of
framework you are looking to use.

Ember
-----
Cob supports front-ends written in Ember (through ember-cli). It even
lets you easily generate a new project::

  $ cob generate grain --type frontend-ember ./webapp

This will create the new grain and even, if ember-cli is detected in
your environment, run ``ember init`` and ``npm install`` for you.

.. note:: After generating the grain, you can use all regular ``ember-cli`` commands. You only have
          to make sure that you run them from within the grain directory -- otherwise they will not
          work as expected.


The Mount Point
+++++++++++++++

Ember front-end grains, much like many other types of grains, can
declare their **mount point**, through the ``.cob.yml`` file::

  type: frontend-ember
  mountpoint: /app

This will make Cob serve your front-end code from the ``/app`` path of
your webapp.

.. note:: for ember, the value of the ``mountpoint`` configuration
          option must be set in accordance with the ``rootURL`` of
          your Ember app's configuration (usually ``config/environment.js``)

Handling ``locationType``
+++++++++++++++++++++++++

Ember can utilize the web browser's *history API* to simulate browsing
URLs directing to the same dynamic single-page app. This capability
works great when navigating from the index through internal links, but
requires additional support when linking to specific routes externally
(as the web server needs to serve the same page even for other path segments).

Cob automatically detects the use of ``locationType`` in your
``config/environment.js`` and adjusts its behavior accordingly. Once
your app uses ``locationType: 'auto'`` instead of ``'hash'``, Cob will
serve all pages under the mountpoint the same way, leading to the
frontend code.


Developing with Front-end Compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Developing back-end and front-end code in tandem requires some additional ergonomics. Cob supports the ``tmux`` command for running a complete development environment inside tmux.

After creating your grains, run ``cob develop`` to start your tmux development session.


Working with Custom Node Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cob installs Node 8.x by default on its docker images, but it can be instructed to use other versions as well. To override the node version being used, override it in your project's configuration::

  # .cob-project.yml
  ...
  frontend:
      node_version: 8
