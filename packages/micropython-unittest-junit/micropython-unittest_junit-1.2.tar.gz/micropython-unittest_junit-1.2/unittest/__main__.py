from .unittest_xml import *

ret = unittest_all(True)

if ret < 0:
    sys.exit(2)
elif ret > 0:
    sys.exit(1)
