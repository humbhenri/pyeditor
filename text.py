# Text manipulation tools
import md5

def md5sum(contents):
    return md5.md5(contents).digest()
