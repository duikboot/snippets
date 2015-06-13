import os
from os.path import pathsep
from subprocess import Popen, PIPE
import logging
from datetime import datetime
from datetime import timedelta
import mailer


def change_dir(directory, createwhenmissing=True, makeparents=True):
    """
    Change to directory, if directory doesn't exist,
    create it first
    """
    #import pdb;pdb.set_trace()
    #global logger
    try:
        os.chdir(directory)
        return True
    except OSError, e:
        logging.error("Cannot change into directory: %s" % e)
        if e.errno == 2:  # errno 2 == directory does not exist
            if not createwhenmissing:
                logging.error("Directory is not created: %s" % e)
                return False
            if not os.path.exists(directory):
                #if makeparents == True:
                if create_dir(directory, makeparents):
                    os.chdir(directory)
                    return True
                else:
                    return False
        elif e.errno == 13:  # errno 13 == permission denied
            logging.critical("Permission denied: %s" % e)
    return False


def create_dir(directory, makeparents=True):
    """
    Create directory and maybe its parents
    """

    if not os.path.exists(directory):
        if makeparents:
            try:
                logging.info("Create directory tree: %s" % directory)
                os.makedirs(directory)
                logging.info("Directory tree %s created" % directory)
                return True
            except OSError, e:
                logging.critical('%s' % e)
                return False
        else:
            logging.info("Create directory: %s" % directory)
            try:
                os.mkdir(directory)
                logging.info("Directory %s created" % directory)
                return True
            except OSError, e:
                directory = directory.rstrip(pathsep)
                parent = os.path.split(directory)[0]
                if e.errno == 2:
                    logging.critical("%s parent directory doesn't exist: %s" %\
                                        (directory, parent))
                    return False
                elif e.errno == 13:
                    logging.critical("Permission denied %s" % parent)
                    return False
            except:
                return False
    return True


def build_command(command_list):
    """
    Very simple, given a command list, flattens the lists, so you end
    up with a one level list
    """
    command = []
    for i in command_list:
        if hasattr(i, 'extend'):
            command.extend(i)
        else:
            command.append(i)
    return command


def sys_command(command, sendmail=None):
    try:
        proc = Popen(command, shell=False, stdout=PIPE, stderr=PIPE,
                     close_fds=True)
    except OSError, e:
        logging.warn("FAILED: system command: %s, for this reason: %s" %
                     (command or "", e or ""))
        return (1, '', e or "")
    output = proc.stdout.read()
    error = proc.stderr.read()
    proc.wait()
    debugmess = ("Output: %s %s" %
                 (output or "", error and "\nError: %s" % error))
    logging.debug(debugmess)
    if proc.returncode:
        log_andor_mail("FAILED Command: %s: out: %s  err: %s" %
                       (" ".join(command), output, error),
                       "FAILED Command",
                       level='error',
                       flag=sendmail)
    return (proc.returncode, output, error)


def log_andor_mail(message, subject="ANNOUNCEMENT", flag=None,
                   level='warn', delta=None, logger=None, debug=False):
    """
    Relatively simple, log the message, and if an email is
    appropriate send one to interested parties using subject as
    the subject.

    Flag can be None (mail never sent), True or False (mails sent
    always), or a datetime in which case if it is older than delta
    (defaults to one day) a mail is sent.  If the mail is sent, the
    new value that the flag should be set to is returned, of desired.
    """
    delta = delta or timedelta(days=1)
    if debug:
        print(message)
    logger = logger or globals().get('logging', False)
    logfunc = logger and getattr(logger, level, False)
    if logfunc:
        logfunc(message)
    else:
        return False
    if flag is None or flag is False:
        return True  # If flag is None, we never mail
    # Otherwise we should check whether we should be sending a mail.
    send_mail = flag is True or \
        (isinstance(flag, datetime) and flag < (datetime.now() - delta))
    if send_mail:
        # send the mail only if it has not been sent, or was sent
        # more than a day ago
        logfunc and logfunc("SENDING EMAIL ALERT")
        try:
            mailer.alert(message, subject=subject)
        except:  # fail silently, we have the log entry
            logfunc and logfunc("SENDING email FAILED")
        return datetime.now()

if __name__ == "__main__":
    #import logging
    #global logger
    logging.basicConfig(filename='/tmp/change_dir.log', level=logging.DEBUG)
    logging.debug("debug")
    change_dir("/tmp/a/b/c/d/", createwhenmissing=False, makeparents=False)
    change_dir("/tmp/a/b/c/d/", createwhenmissing=True, makeparents=False)
    change_dir("/tmp/a/b/c/d/", createwhenmissing=True, makeparents=True)
    change_dir("/tmp/d", createwhenmissing=True, makeparents=True)
    change_dir("/var/log/sssd/", createwhenmissing=True, makeparents=True)
    change_dir("/tmp/a/b/c/d/", createwhenmissing=False, makeparents=False)

    logging.info(os.getcwd())

    create_dir('/tmp/1/2/3/4/6')
    logging.info(os.getcwd())


