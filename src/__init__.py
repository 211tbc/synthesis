from conf import settings
from conf import inputConfiguration
from mainprocessor import MainProcessor
import os
import logging

import datetime
from lxml import etree
import urllib
from webob import Request
from webob import Response

if inputConfiguration.USE_ENCRYPTION:
    from Encryption import *
from selector import Selector
import base64

from pyramid_controllers import RestController, expose
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

#server_root = config['here']
server_root = 'here'
log = logging.getLogger(__name__)

class DocsController(RestController):
    @expose
    def get(self, request):
        print "docs/index called"
        return "you're at the docs index"

    @expose
    def put(self, request):
        return 'put'

    @expose
    def post(self, request):
        #import pdb; pdb.set_trace()
        req = Request(request.environ)
        log.debug('Received HTTP Request: %s', req)
        print 'these are the request.params: ', request.params
        print "request.environ is" , request.environ
        #print "request.environ['CONTENT_LENGTH'] is" , request.environ['CONTENT_LENGTH']
        print "FULL RAW POST Data:"
        #this CONTENT_LENGTH wasn't getting populated in the environment on remote installations using encryption
        #print request.environ['wsgi.input'].read(int(request.environ['CONTENT_LENGTH']))
        print request.environ['wsgi.input'].read(req.content_length)

        print "FULL request.POST Data:"
        print request.POST
        
        postdatakeys = request.POST.keys()
        print "keys are:", postdatakeys
        #accept only one posted file per request for now
        stream_fieldstorage = request.POST[postdatakeys[0]]
        print "size of post data in bytes", len(stream_fieldstorage.value)
        #print "CGI FileStorage uploaded is: ", myfile
        
        #Create a file in a permanent location, moving it out of CGI FieldStorage
        #make file
        file_prefix = 'received_data_' + str(datetime.datetime.now())
        file_prefix = file_prefix.replace(' ', '_')
        file_suffix_enc = '_encrypted.xml'
        file_suffix_unenc = '_unencrypted.xml'
        if inputConfiguration.USE_ENCRYPTION:
            print "using encryption"
            file_name = file_prefix + file_suffix_enc
        elif not inputConfiguration.USE_ENCRYPTION:
            print "not using encryption"
            file_name = file_prefix + file_suffix_unenc
        else: 
            print "not sure if using encrypted file or not"
        
        if not os.path.exists(inputConfiguration.WEB_SERVICE_INPUTFILES_PATH[0]):
                os.mkdir(inputConfiguration.WEB_SERVICE_INPUTFILES_PATH[0])
        file_full_path = os.path.join(inputConfiguration.WEB_SERVICE_INPUTFILES_PATH[0], file_name)
        print 'file_full_path: ', file_full_path
        
        #open file 
        if inputConfiguration.USE_ENCRYPTION:
            try:
                print "trying to open encrypted file"
                encrypted_file = open(file_full_path, 'w')
            except:
                print "Error opening encrypted instance file for writing"
        if not inputConfiguration.USE_ENCRYPTION:
            try:
                print "trying to open unencrypted file"
                unencrypted_file = open(file_full_path, 'w')
            except:
                print "Error opening unencrypted instance file for writing"
                
        #write to file
        if inputConfiguration.USE_ENCRYPTION:
            print 'writing', file_name, 'to', server_root, 'for decryption'
            print 'encrypted_file is', encrypted_file
            encrypted_file.write(stream_fieldstorage.value)
            encrypted_file.close()
            
        if not inputConfiguration.USE_ENCRYPTION:
            print 'writing', file_name, 'to', server_root, 'server root for parsing'
            print 'unencrypted_file is', unencrypted_file
            unencrypted_file.write(stream_fieldstorage.value)
            unencrypted_file.close()
        
        #check if a file was written, regardless of encryption    
        if not os.path.exists(file_full_path):
            print "A file wasn't written"
        else:
            print "A file was written at: ", file_full_path
        
        #decrypt file if using decryption
        #assume file is encrypted, since it can be difficult to tell if it is.  We could look for XML structures, but how do you easily tell bad/invalid  XML apart from encrypted?  If not encrypted, that's a problem.
        #decrypt file
        if inputConfiguration.USE_ENCRYPTION:
            try:
                encrypted_file = open(file_full_path, 'r') 
            except: 
                print "couldn't open encrypted file for reading/decryption"

            data_decrypted = False
            encoded_stream = encrypted_file.read()
            encrypted_file.close()
            cryptors = [DES3, GPG]
            for cryptor in cryptors:
                cobj = cryptor()
                try:
                    if cobj.__class__.__name__ == 'DES3':
                        keyiv = get_incoming_3des_key_iv()
                        # decode base64 stream
                        encrypted_stream = base64.b64decode(encoded_stream)
                        # decrypt stream
                        decrypted_stream = cobj.decrypt(str(encrypted_stream), keyiv['key'], iv=keyiv['iv'])
                        # test if the resulting decrypted_stream is XML
                        xml_test = etree.XML(decrypted_stream)
                        data_decrypted = True
                        xml_test = None
                        break
                    if cobj.__class__.__name__ == 'GPG':
                        # decode base64 stream
                        encrypted_stream = base64.b64decode(encoded_stream)
                        # decrypt stream
                        decrypted_stream = cobj.decrypt(str(encrypted_stream))
                        # test if the resulting decrypted_stream is XML
                        xml_test = etree.XML(decrypted_stream)
                        data_decrypted = True
                        xml_test = None
                        break
                except:
                    continue

            if data_decrypted:
                file_suffix_unenc = '_decrypted.xml'
                file_name = file_prefix + file_suffix_unenc
                file_full_path =  inputConfiguration.INPUTFILES_PATH[0] + '/' + file_name
                try:
                    decrypted_file = open(file_full_path, 'w')
                except:
                    print "Error opening decrypted instance file for writing"
                #write to file
                print 'writing', file_name, 'to', server_root, 'to validate'
                decrypted_file.write(decrypted_stream)
                decrypted_file.close()
                if not os.path.exists(file_full_path):
                    print "An decrypted file wasn't written"
                else:
                    print "A file was written at: ", file_full_path
            else:
                message = "Unable to decrypt %s or the decoded|decrypted data is not valid XML" % file_full_path
                print message
                return message
        
        #read in candidate XML file
#        if inputConfiguration.USE_ENCRYPTION:
#            try:
#                unencrypted_file = open(file_full_path, 'r') 
#            except: 
#                print "couldn't open decrypted file for reading"
#            
#        if inputConfiguration.USE_ENCRYPTION:
#            try:
#                unencrypted_file = open(file_full_path, 'r') 
#            except: 
#                print "couldn't open unencrypted file for reading"

        # remove multiple source tags
        incoming_doc = etree.parse(file_full_path)
        ns='{http://xsd.alexandriaconsulting.com/repos/trunk/HUD_HMIS_XML/TBC_Extend_HUD_HMIS.xsd}'
        for i, src in enumerate(incoming_doc.findall('{0}Source'.format(ns))):
            if i == 0:
                # we only care about the first one
                continue
            # remove the remaning source tags
            incoming_doc.getroot().remove(src)
        incoming_doc.write(file_full_path, pretty_print=True, encoding="UTF-8")

        #validate  XML instance
        select = Selector()
        result = select.validate(file_full_path, False)
        try:
            this_schema = result.index(True)
            schema_name = select.current_tests[this_schema].__name__
            if len(schema_name) > 4:
                schema_name = schema_name[:len(schema_name) - 4]
            message = '202: The posted xml (locally at %s) successfully validated against the %s schema.' % (file_name, schema_name)
            response = Response()
            response.status_int = 202
            print message
            #move valid file over to regular synthesis input_files directory for shredding
            print "moving valid file ", file_name, "over to input_files for shredding"
            ###
            ### FBY: The following if-else code block is just plain weird!
            ###
            if not inputConfiguration.USE_ENCRYPTION:
                # FBY: Call fileutils.moveFile to move unencrypted files into the input_files folder
                import fileutils
                fileutils.moveFile(file_full_path, inputConfiguration.INPUTFILES_PATH[0])
            else:
                # FBY: For encrypted files, instead of a call to fileutils.moveFile, move
                #      the files using system calls (i.e. the "mv" command)
                try:
                    if not os.path.exists(inputConfiguration.INPUTFILES_PATH[0]):
                        os.mkdir(inputConfiguration.INPUTFILES_PATH[0])
                    import subprocess
                    mvp = subprocess.Popen('mv %s %s' % (file_full_path, fileutils.getUniqueFileNameForMove(file_full_path, inputConfiguration.INPUTFILES_PATH[0])))
                    # FBY: Wait for the "mv" call to finish
                    mvp.wait()
                except Exception, e:
                    print e
            return message            
        except:
            details = ''.join(list(set([str(issue) for issue in select.issues])))
            message = '400: Could not find a matching schema for the posted xml. Details: %s' % (details)
            return message
    
    @expose
    def delete(self, request):
        return 'delete'
        
def start_mainprocessor():
    MainProcessor()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_controllers')
    config.add_controller('docs', '/docs', DocsController())
    config.add_static_view('static', 'static', cache_max_age=3600)
    #config.add_route('home', '/')
    config.add_route('index', '/')
    config.scan()
    app = config.make_wsgi_app()
    # MainProcessor setup the database among other things
    from multiprocessing import Process
    p = Process(target=start_mainprocessor, args=())
    p.start()
    return app
