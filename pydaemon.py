'''
    This module is used to fork the current process into a daemon.
    Almost none of this is necessary (or advisable) if your daemon 
    is being started by inetd. In that case, stdin, stdout and stderr are 
    all set up for you to refer to the network connection, and the fork()s 
    and session manipulation should not be done (to avoid confusing inetd). 
    Only the chdir() and umask() steps remain as useful.
    References:
        UNIX Programming FAQ
            1.7 How do I get my program to act like a daemon?
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        Advanced Programming in the Unix Environment
            W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

    History:
      2001/07/10 by Jrgen Hermann
      2002/08/28 by Noah Spurrier
      2003/02/24 by Clark Evans
      
      http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
'''
import sys, os, time
from signal import SIGTERM

class pydaemon:
    def __init__(self, name=sys.argv[0], stdout='/dev/null', stderr=None, stdin='/dev/null',
                  pidfile=None, user_function=None):
        self.name = name
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.pidfile = pidfile
        self.user_function = user_function

    def _daemonize(self):
        '''
            This forks the current process into a daemon.
            The stdin, stdout, and stderr arguments are file names that
            will be opened and be used to replace the standard file descriptors
            in sys.stdin, sys.stdout, and sys.stderr.
            These arguments are optional and default to /dev/null.
            Note that stderr is opened unbuffered, so
            if it shares a file with stdout then interleaved output
            may not appear in the order that you expect.
        '''
        # Do first fork.
        try: 
            pid = os.fork() 
            if pid > 0: sys.exit(0) # Exit first parent.
        except OSError, e: 
            sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment.
        os.chdir("/") 
        os.umask(0) 
        os.setsid() 

        # Do second fork.
        try: 
            pid = os.fork() 
            if pid > 0: sys.exit(0) # Exit second parent.
        except OSError, e: 
            sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Open file descriptors and print start message
        if not self.stderr: self.stderr = self.stdout
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        pid = str(os.getpid())
        startmsg = "%s started with pid %s\n"
        sys.stderr.write(startmsg % (self.name, pid))
        sys.stderr.flush()
        if self.pidfile: file(self.pidfile,'w+').write("%s\n" % pid)

        # Redirect standard file descriptors.
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def _get_pid(self):
        try:
            pf  = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        return pid

    def _kill_process(self, pid):
        if pid == None: return False
        try:
            while 1:
                os.kill(pid,SIGTERM)
                time.sleep(1)

        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                os.remove(self.pidfile)
                return True
            else:
                print str(err)
                return False

    def init(self, action):
        if "start" == action: 
            pid = self._get_pid()
            if pid:
                m = "Error: Aborted start since pid file '%s' exists.\n"
                sys.stderr.write(m % self.pidfile)
                return

            self._daemonize()
            self.user_function()

        elif "stop" == action:
            pid = self._get_pid()
            if not pid:
                m = "Error: Could not stop, pid file '%s' is missing.\n"
                sys.stderr.write(m % self.pidfile)
                return

            if self._kill_process(pid):
                sys.stderr.write("%s stopped.\n" % self.name)

        elif "restart" == action:
            if self._kill_process(self._get_pid()):
                sys.stderr.write("%s stopped.\n" % self.name)

            self._daemonize()
            self.user_function()

        elif "status" == action:
            if self._get_pid():
                sys.stderr.write("Status: %s is running.\n" % self.name)
            else:
                sys.stderr.write("Status: %s is stopped.\n" % self.name)

        else:
            print "usage: %s start|stop|restart|status" % self.name

def test():
    '''
        This is an example main function run by the daemon.
        This prints a count and timestamp once per second.
    '''
    sys.stdout.write ('Message to stdout...')
    sys.stderr.write ('Message to stderr...')
    c = 0
    while 1:
        sys.stdout.write ('%d: %s\n' % (c, time.ctime(time.time())) )
        sys.stdout.flush()
        c += 1
        time.sleep(1)

if __name__ == "__main__":

    action = "start"
    if len(sys.argv) > 1:
        action = sys.argv[1]

    d = pydaemon(stdout='/tmp/deamonize.log',
                 pidfile='/tmp/deamonize.pid',
                 user_function=test)
    d.init(action)
