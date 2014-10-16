import json
import inspect
#----------------------------------------------------------------------
def init_config_json(config_file):

    #Load the config file
    with open(config_file) as json_file:
        json_data = json.load(json_file)
        return unicode_convert( json_data)
#----------------------------------------------------------------------
def write_config_json(config_file, data):
    with open(config_file, 'w') as outfile:
        json.dump(data, outfile)  
      
#----------------------------------------------------------------------
def unicode_convert(obj):
    """ converts unicode to anscii """
    if isinstance(obj, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in obj.iteritems()}
    elif isinstance(obj, list):
        return [unicode_convert(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj
def find_replace(obj,find,replace):
    """ searchs an object and does a find and replace """
    if isinstance(obj, dict):
        return {find_replace(key,find,replace): find_replace(value,find,replace) for key, value in obj.iteritems()}
    elif isinstance(obj, list):
        return [find_replace(element,find,replace) for element in obj]
    elif obj == find:
        return replace
    else:
        return obj     
#----------------------------------------------------------------------
def init_log(log_file,):

    #Create the log file
    log = None
    try:
        log = open(log_file, 'a')

        #Change the output to both the windows and log file
        #original = sys.stdout
        sys.stdout = Tee(sys.stdout, log)
    except Exception:
        pass
    return log


#----------------------------------------------------------------------
def init_localization():
    '''prepare l10n'''
    locale.setlocale(locale.LC_ALL, '') # use user's preferred locale
    # take first two characters of country code
    filename = "res/messages_%s.mo" % locale.getlocale()[0][0:2]

    try:
        #print( "Opening message file %s for locale %s") % (filename, loc[0])
        trans = gettext.GNUTranslations(open( filename, "rb" ) )
    except IOError:
        #print( "Locale not found. Using default messages" )
        trans = gettext.NullTranslations()

    trans.install()

#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile( inspect.currentframe() )
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

