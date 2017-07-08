import sys, os, bottle
sys.path = ['C:/Users/scshao5923/SkyDrive/python/project/dict/'] + sys.path

# Change working directory so relative paths (and template lookup) work again
print('__file__:'+os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

# ... build or import your bottle application here ...
import webdict # This loads your application

# Do NOT use bottle.run() with mod_wsgi
application = bottle.default_app()
