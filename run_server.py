import cherrypy
import os
import re
import subprocess

from scipy.stats import *



def iif(a,b,c):
    if a:
        return b 
    else:
        return c

def update_top_models_page(models):
    f = open("media/Navbar.html")
    navbar_lines = f.readlines()
    f.close()

    f = open("media/TopModels.html","w")
    for l in navbar_lines:
        f.write(l)

    f.write("""
     <div class="container theme-showcase" role="main">
          <div class="starter-template">
            <div class="panel panel-default">
              <div class="panel-heading">Top User Submited Models</div>
              <table class="table">
                <thead>
                  <tr>
                      <th>#</th>
                    <th>Model</th>
                    <th>R Correlation</th>
                  </tr>
                </thead>
                <tbody>""")

    count = 1
    for m in models:
        f.write("<tr><td>" + str(count) + "</td><td>" + m[0] + "</td><td>" + str(m[1]) + "</td></tr>\n")
        count += 1 

        if count > 20:
            break

    f.close()
 
MEDIA_DIR = os.path.join(os.path.abspath("."))




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
    def posted_2(self, model):
        compiled_model = compile_model_from_str(model,features)

        real_scores = []
        predicted_scores = []

        for c in all_constructs:
            #set the correct local variable name for the compiled code object
            construct = c
            exec compiled_model
            real_scores.append(float(c.eterna_score))
            #local variable score gets set by exec model, see parse_model_file
            predicted_scores.append(score)

        R = pearsonr(real_scores,predicted_scores)
        #R = [0,0]

        found = 0
        for m in self.models:
            if m[0] == model:
                found = 1
                break

        if not found:
            flag = 0
            pos = 20 
            if len(self.models) < pos:
                flag = 1
            else:
                if self.models[pos][1] < float(R[0]):
                    flag = 1


            self.models.append([model,float(R[0])])
            self.model_file.write(model + "\n" + str(R[0]) + "\n")
            self.model_file.flush()

            if flag:
                self.models = sorted(self.models, key=lambda x: x[1], reverse=True)
                update_top_models_page(self.models)

        f = open(os.path.join(MEDIA_DIR, u'media/Test_Your_Model_Result.html')) 
        lines = f.readlines()
        f.close()

        string = "".join(lines)
        string += """
        <br/>
        <hr>
        <p class=\"lead\">
        Model:          %s<br />
        R Correlation:  %s
        </p>
        </div>
        </div>
        </body>
        </html>""" % (model,R[0])
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





