# BOTLIB - the bot library !
#
#

import datetime, json, os, random, time

from .utl import cdir, fntime, get_type, hooked

def __dir__():
    return ("Object", "ObjectEncoder", "ObjectDecoder", "names", "stamp", "workdir", "xdir")

workdir = None

class Object:

    __slots__ = ("__dict__", "_path")

    def __init__(self):
        self._path = os.path.join(get_type(self), str(datetime.datetime.now()).replace(" ", os.sep))

    def __delitem__(self, k):
        del self.__dict__[k]

    def __getitem__(self, k, d=None):
        return self.__dict__.get(k, d)

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __len__(self):
        return len(self.__dict__)

    def __lt__(self, o):
        return len(self) < len(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v
        return self.__dict__[k]

    def __str__(self):
        return json.dumps(self, skipkeys=True, cls=ObjectEncoder, indent=4, sort_keys=True)

    def load(self, path, force=False):
        """ load an object from json file at the provided path. """
        assert path
        assert workdir
        self._path = path
        lpath = os.path.join(workdir, "store", path)
        cdir(lpath)
        with open(lpath, "r") as ofile:
            val = json.load(ofile, cls=ObjectDecoder)
            if val:
                if isinstance(val, Object):
                    self.__dict__.update(vars(val))
                else:
                    self.__dict__.update(val)

    def save(self, stime=None):
        """ save this object to a json file, uses the hidden attribute _path. """
        assert workdir
        if stime:
            self._path = os.path.join(get_type(self), stime) + "." + str(random.randint(1, 100000))
        opath = os.path.join(workdir, "store", self._path)
        cdir(opath)
        with open(opath, "w") as ofile:
            json.dump(stamp(self), ofile, cls=ObjectEncoder, indent=4, skipkeys=True, sort_keys=True)
        return self._path

class ObjectEncoder(json.JSONEncoder):

    def default(self, o):
        """ return string for object. """
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, list):
            return iter(o)
        if isinstance(o, (type(str), type(True), type(False), type(int), type(float))):
            return o
        return repr(o)

class ObjectDecoder(json.JSONDecoder):

    def decode(self, o):
        """ return object from string. """
        return json.loads(o, object_hook=hooked)

def names(name, delta=None):
    """ return filenames in the working directory. """
    if not name:
        return []
    assert workdir
    p = os.path.join(workdir, "store", name) + os.sep
    res = []
    now = time.time()
    if delta:
        past = now + delta
    for rootdir, dirs, files in os.walk(p, topdown=False):
        for fn in files:
            fnn = os.path.join(rootdir, fn).split(os.path.join(workdir, "store"))[-1]
            if delta:
                if fntime(fnn) < past:
                    continue
            res.append(os.sep.join(fnn.split(os.sep)[1:]))
    return sorted(res, key=fntime)

def stamp(o):
    """ recursively add filename fields to a dict. """
    for k in xdir(o):
        oo = getattr(o, k, None)
        if isinstance(oo, Object):
            stamp(oo)
            oo.__dict__["stamp"] = oo._path
            o[k] = oo
        else:
            continue
    o.__dict__["stamp"] = o._path
    return o

def xdir(o, skip=None):
    """ return dir() but skipping unwanted keys. """
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
