import cherrypy
import os
import re
import subprocess

from scipy.stats import *



MEDIA_DIR = os.path.join(os.path.abspath("."))

def get_first_part_of_page():
    f = open(os.path.join(MEDIA_DIR, u'media/Test_Your_Model_Result.html')) 
    lines = f.readlines()
    f.close()

    string = "".join(lines)
    return string

def is_valid_sequence(sequence):
	res = "A,G,C,U,T".split(",")
	for e in sequence.upper():
		if e not in res:
			return 0
	return 1


class rest:
    def __init__(self):
        pass


    @cherrypy.expose
    def index(self):
        return open(os.path.join(MEDIA_DIR, u'media/index.html'))

    @cherrypy.expose
    def posted(self, sequence, structure):

        construct = Construct(sequence,structure,0)
        constructs = [construct]
        populate_features_for_constructs(constructs,feature_generators)
    
        #features = constructs[0].features.keys()
        #features.sort(reverse=True)

        real_scores = []
        all_data = []
        for c in constructs:
            data = []
            for f in features:
                data.append(c.features[f])
            real_scores.append(float(c.eterna_score))
            all_data.append(data)

        predicted_scores = predictor.predict(all_data)
        f = open(os.path.join(MEDIA_DIR, u'media/Score_Seq_SS_Result.html')) 
        lines = f.readlines()
        f.close()

        string = "".join(lines)
        string += """
        <br/>
        <hr>
        <p class=\"lead\">
        Sequence:  %s<br/>
        Structure: %s<br/>
        Score:     %s</p>
        </div>
        </div>
        </body>
        </html>""" % (sequence,structure,predicted_scores[0])
        return string

    @cherrypy.expose
    def design_primers(self, sequence):

        #TODO use matlab wrapper instead
        #TODO check for length

        if len(sequence) < 60:
        	string = get_first_part_of_page()
        	string += """
        	<br/>
        	<hr>
        	<p class=\"lead\">
        	You need a sequence of atleast 60 residues, try again. 
        	</p>
        	</div>
        	</div>
        	</body>
        	</html>"""

        	return string

        if not is_valid_sequence(sequence):
        	string = get_first_part_of_page()
        	string += """
        	<br/>
        	<hr>
        	<p class=\"lead\">
        	sequence must consist of A,G,C,U or T!
        	</p>
        	</div>
        	</div>
        	</body>
        	</html>"""

        	return string

        out = os.popen('matlab -nojvm -nodisplay -nosplash -r "design_primers(\'%s\'); exit()"' % sequence).read()
        out = out.replace('\n', '<br/>')

        f = open(os.path.join(MEDIA_DIR, u'media/Test_Your_Model_Result.html')) 
        lines = f.readlines()
        f.close()

        string = "".join(lines)
        string += """
        <br/>
        <hr>
        <p class=\"lead\">
        Output:          %s<br />
        </p>
        </div>
        </div>
        </body>
        </html>""" % out
        return string

if __name__ == "__main__":

    cherrypy.config.update( {
        #'server.socket_host':"171.64.65.150", 
        'server.socket_host':"127.0.0.1", 
        'server.socket_port':8080,
        'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
        #'tools.statiddir.root': "/Users/skullnite/Downloads"
    } )
    #print os.path.abspath(os.path.join(__file__, 'static'))
    #cherrypy.quickstart( rest(), '/', 'development.conf' )
    
    cherrypy.quickstart(rest(), '', config={
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
            },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'images'
            },
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'media'
            },
        '/data': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'data'
            }
        }
    )





