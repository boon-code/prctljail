#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This Module is about using PR_SET_SECCOMP as a jail.

The prctl syscall implements a command to build a jail
like environment (PR_SET_SECCOMP command).
"""

from ctypes import CDLL
from select import select
from io import StringIO
import os
import sys
import json

__author__ = 'Manuel Huber'
__copyright__ = "Copyright (c) 2011 Manuel Huber."
__license__ = 'GPLv3'
__version__ = '0.0.1'
__docformat__ = "restructuredtext en"


class JailException(Exception):
    """Basic Exception of this Module
    
    All Exceptions of this module should be derived
    from this one.
    """
    pass


class LibraryNotFoundError(JailException):
    """A library couldn't be found.
    
    This Exception will be thrown, if the library
    with name *name* couldn't be load successfully.
    """
    
    def __init__(self, name, *args):
        """Initializes a new instance.
        
        :param name: Name of the library to load.
        :param args: Details on the error that will be
                     passed to the base class.
        """
        JailException.__init__(*args)
        self.name = name


class FuncNotFoundError(JailException):
    """A function of a library couldn't be found.
    
    This Exception will be thrown, if it's has
    been tried to access a function of a library
    that does not exist.
    """
    
    def __init__(self, libname, funcname, *args):
        """Initializes a new instance.
        
        :param libname:  Name of the library that has been
                         searched.
        :param funcname: Name of the function that couldn't
                         be found.
        :param args:     Details on the error that will be
                         passed to the base class.
        """
        JailException.__init__(*args)
        self.libname = libname
        self.funcname = funcname


class JailedProcess(object):
    """Represents the jailed process.
    
    This *JailedProcess* object can be used to 
    execute a python function in a *safe* context.
    
    This class is only as safe as the json module it uses
    and the kernel it's running on. Also, there can be 
    errors in the code, it has not been tested a lot.
    Note that all files that are currently open can be
    accessed by the "secure" process.
    
    *func* can have a return value (this can be any json
    compatible type). The value will be written to *ret*.
    Note that you always have to check the value returned by
    the *run* method. If the returned value is not 0, 
    there has been an error and *ret* should contain a
    string representation of the exceptions that occurred.
    """
    
    PR_SET_SECCOMP = 22
    SYS_exit = 1
    
    @classmethod
    def isAvailable(cls, raise_exception=False):
        """Classmethod that checks availability of this "Jail".
        
        This method just tries to load the libc and find
        all functions needed to create a jail.
        
        TODO:
        
        - I'm not finished yet... I should somehow test if
          the *PR_SET_SECCOMP* command really is supported.
        
        :param cls:             The class object.
        :param raise_exception: If this flag ist set to True,
                                an exception will be thrown if 
                                the method would return False.
                                (The Exception should include
                                detailed information about
                                what went wrong.)
        
        :returns: True if all necessary methods could be found
                  else False.
        """
        
        libc_name = "libc.so.6"
        func_name = ""
        try:
            if sys.platform.startswith('linux'):
                cls.libc = CDLL(libc_name)
                func_name = "prctl"
                cls.prctl = cls.libc.prctl
                func_name = "syscall"
                cls.syscall = cls.libc.syscall
                return True
            else:
                return False
        except OSError as e:
            if raise_exception:
                raise LibraryNotFoundError(libc_name, *e.args)
            return False
        except AttributeError as e:
            if raise_exception:
                raise FuncNotFoundError(libc_name, func_name, *e.args)
            return False
    
    def __init__(self, func, args=tuple(), kargs=dict()):
        """Initializes a new instance.
        
        :param func:  The function that will be executed.
        :param args:  Arguments for *func*
        :param kargs: Keyword arguments for *func*
        """
        self.func = func
        self.args = args
        self.kargs = kargs
        self.ret = None
    
    def _wait(self, pp, cp, pid, wait=0.0):
        """Waits until i/o and process are finished.
        
        :param pp:   Parent pipe.
        :param cp:   Child pipe.
        :param pid:  Process identifier.
        :param wait: Optional wait time (for select).
        """
        proc_run = True
        pipe_run = True
        stream = StringIO()
        ret = None
        while proc_run or pipe_run:
            if pipe_run:
                if pp in select([pp], [], [], wait)[0]:
                    ch = os.read(pp, 1).decode()
                    if ch == '':
                        pipe_run = False
                    else:
                        stream.write(ch)
            if proc_run:
                ret = os.waitpid(pid, os.WNOHANG)
                if ret[0] == pid:
                    os.close(cp)
                    proc_run = False
        
        value = stream.getvalue()
        stream.close()
        
        return (ret[1], value)
    
    def run(self):
        """Executes restricted function (blocking).
        
        This will create a new process (fork) and block the
        calling process until the new process finishes.
        
        TODO:
        
        - It should be possible to give a "maximum-wait-time".
          After that time, the new process will be killed and
          the calling process finally returns (maybe
          throw an exception).
        - Maybe I will change the return value to directly
          return *ret* member and automatically throw an
          Exception if some error happend (or a violation).
        
        :returns: Returns the exit code of the new process.
        """
        self.ret = None
        self.isAvailable(raise_exception=True)
        emode = 0
        pp, cp = os.pipe()
        pid = os.fork()
        if pid == 0:
            self.prctl(self.PR_SET_SECCOMP, 1)
            try:
                v = self.func(*self.args, **self.kargs)
                d = json.dumps(v)
                os.write(cp, d.encode())
            except Exception as e:
                emode = 2
                d = json.dumps(str(e))
                os.write(cp, d.encode())
                emode = 1
            finally:
                self.syscall(self.SYS_exit, emode)
        else:
            ret, text = self._wait(pp, cp, pid)
            self.ret = text
            return ret
