import cherrypy
import os.path
import urllib2
import json
import re
from htmllaundry import strip_markup

current_dir = os.path.dirname(os.path.abspath(__file__))

class Page:
    # Store the page title in a class attribute
    title = 'GetHub Repo Lister'

    def header(self):
        return '''
            <html>
            <head>
                <title>%s</title>
                <link rel="stylesheet" type="text/css" href="style.css">
            <head>
            <body>
            <div id="container">
            <h1>The amazing github lister, awww yeaaa!</h1>
        ''' % (self.title)

    def footer(self):
        return '''
            </div>
            </body>
            </html>
        '''

class WelcomePage(Page):
    def index(self):
        # Every yield line adds one part to the total resulting body.
        yield self.header()

        # Ask for the username
        yield '''<p>
            <form action="getRepos" method="POST">
            What username would you like to lookup?
            <input type="text" name="name" />
            <input type="submit" />
            </form></p>'''
        yield self.footer()

    index.exposed = True

    def getRepos(self, name = None):

        yield self.header()

        if not name:
            yield '<p>Please actually enter a username.</p>'
        else:
            name = strip_markup(name)
            try:
                url = "https://api.github.com/users/%s/repos" % name
                req = urllib2.Request(url)
                opener = urllib2.build_opener()
                f = opener.open(req)
                data = json.load(f)
                gotten = True
            except urllib2.URLError, e:
                if '404' in str(e): yield "<p>Something went wrong, you likely didn't type in the username correctly.</p>"
                elif '403' in str(e): yield "<p>Something went wrong, you've likely gone beyond the GitHub API request limits.</p>"
                else: yield "<p>Something went wrong: " + str(e) + "</p>"
                gotten = False

            if(gotten):
                if(len(data) != 0):
                    final_data = "<p> The user %s has these public repos: <br /> <ul>" % name
                    for i in data:
                        final_data += "<li>" + i['name'] + "</li>"
                    final_data += "</ul></p>"
                    yield final_data
                else:
                    yield "<p>This user doesn't currently have any repos.</p>"

        ###############################################################################################################
        #                                                                                                             #
        #                                                                                                             #
        #          Adding the SendGrid API calls would be done here, will do once my account is provisioned.          #
        #                                                                                                             #
        #                                                                                                             #
        ###############################################################################################################

        yield "<p><a href='./'>Try again</a>.</p>"
        yield self.footer()

    getRepos.exposed = True

projconf = os.path.join(os.path.dirname(__file__), 'project.conf')

if __name__ == '__main__':
    cherrypy.quickstart(WelcomePage(), config=projconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(WelcomePage(), config=projconf)
