#!/usr/bin/python3
"""TO-DO: Write a description of what this XBlock is."""
 
import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope
import psycopg2

class MyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/myxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/myxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/myxblock.js"))
        frag.initialize_js('MyXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def listardatos(self, data, suffix=''):
        conn = psycopg2.connect(dbname='db_usuarios',user='postgres',password='1234',host='localhost')
        cur = conn.cursor()
        #Se inserta los nuevos usuarios extraidos del formulario
        cur.execute("INSERT INTO tabla_usuarios (name, lastname, email) VALUES(%s, %s, %s)", (data['name'], data['lastname'],data['email']))
        conn.commit()
        cur.close()
        #Se coonsulta los usuarios ingresados para cargarlos a la tabla dinámica
        cur2 = conn.cursor()
        cur2.execute("SELECT * FROM tabla_usuarios")
        rows=cur2.fetchall()
        conn.close()
        tabladinamica = "<table border='1'> <tr><td>Nombre</td><td>Apellido</td><td>Correo</td></tr>"
        for i in range(len(rows)):
            tabladinamica+= "<tr><td>"+rows[i][0]+"</td><td>"+rows[i][1]+"</td><td>"+rows[i][2]+"</td></tr>"
        tabladinamica+="</table>"
        return{"resultado":tabladinamica}

    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]
