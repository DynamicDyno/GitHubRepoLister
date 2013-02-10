GitHub Repo Lister
==================

This is a simple web app, done as a project for [SendGrid](http://sendgrid.com/). Both [CherryPy](http://www.cherrypy.org/) and [HTML Laundry](http://pypi.python.org/pypi/htmllaundry/) need to be installed, setup.sh will take care of this for you. HTML Laundry uses the clang compiler, which most linux disros include by default and Mac OSX has if you install the Xcode command line tools. You will need to update project.conf. After you finish installing, just run `python GitHubRepoLister.py` and visit `localhost:8080`.
