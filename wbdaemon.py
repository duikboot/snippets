import fcntl
from daemon import Daemon
from daemons.utils.locking import LockFile
import subprocess
import logging
import os
import time
import shutil
from lxml import etree
from daemons.utils import helperfunctions as hf

LOCKFILE = "/var/lock/wbdaemon.lock"

# process wide lock flag that also holds a reference to the LockFile
# class.
_lock = None

class WBDaemon(Daemon):
    """
    This is an attempt to stick all the daemony bits and pieces we need
    into one class, which can then be extended
    """

    def svn_command(self, command, lock_first=True, error_msg=None):
        """Many svn commands must aquire a lock first, which is a
        bunch of template code, so this can be better refactored
        to here."""
        if lock_first and not self.aquire_lock():
            logging.error("Could not aquire lock for command: %s", command)
            return False
        ret, output, error = hf.sys_command(command)
        lock_first and self.release_lock()
        if ret != 0:  # an error occurred
            if error_msg:
                logging.error(error_msg, command, error)
            else:
                logging.error("Svn command failed for %s:  %s", command, error)
            return False
        return (ret, output, error)

    def svn_up(self, path, lock_first=True):
        """This updates a path, making sure that it has locked the
        lock file first"""
        command = ['svn', 'update', path]
        ret, output, error = self.svn_command(command, lock_first,
                                              error_msg="SVN UP Failed %s: %s")
        return output

    def svn_commit(self, files, comment="Committing Files"):
        """Given a list of files, do an svn commit for the files"""
        # It might be a better idea to just stick this in a while loop
        # until it can actually aquire the lock, and the execute.
        if not self.aquire_lock():
            logging.error("Could not aquire lock for commit: %s", files)
            return False

        # update files before committing (if the file is not under
        # svn, svn gives not error, so this will not cause problems)
        up_results = [(path, self.svn_up(path, False)) for path in files]
        print up_results
        ## check if this must be added first
        ## To do this I need to check the status of the files
        adds = self.add_first(files)
        added = [(add, self.svn_add(add, False)) for add in adds]

        ## Now commit the lot
        command = ['svn', 'commit', '-m', comment]
        command.extend(files)
        ret, output, error = self.svn_command(command, lock_first=False,
                                              error_msg="Commit failed for %s: %s")
        self.release_lock()
        return error and False or True

    def add_first(self, files):
        """Checks a list of file paths to see if the file is under
        version control.  If not it is added to a list of files that
        must be added first, and returned"""
        adds = []
        # get the xml version of status for the file
        xmlouts = [(path, self.svn_status(path)) for path in files]
        for path, xml in xmlouts:  # parse the xml
            tree = etree.fromstring(xml)
            entries = tree.xpath('//entry')
            for entry in entries:
                path = entry.attrib['path']
                status = entry.getchildren()[0].attrib['item']
                if status == 'unversioned':  # needs to be added first
                    adds.append(path)
        return adds

    def svn_add(self, path, lock_first=True):
        command = ['svn', 'add', path]
        ret, output, error = self.svn_command(command, lock_first)
        return not error and True or False

    def svn_status(self, path):
        command = ['svn', 'status', '--ignore-externals', '--xml', path]
        ret, output, error = self.svn_command(command, lock_first=False,
                                              error_msg="status request failed for %s: %s")
        return ret != 0 and False or output

    def move_dir_files(self, from_dir, to_dir, nohidden=True):
        """Moves all the files from one directory to another"""
        files = (os.path.join(from_dir, f) for f in os.listdir(from_dir))
        files = (f for f in files if os.path.isfile(f))
        # if nohidden:
        #     files = (f for f in files if not os.path.basename(f).startswith('.'))
        for p in files:
            filep = os.path.basename(p)
            try:
                # if the file already exists, remove it
                if os.path.exists(os.path.join(to_dir, filep)):
                    os.remove(os.path.join(to_dir, filep))
                # if the file to be moved does not exist, continue
                if not os.path.exists(p):
                    continue
                shutil.move(os.path.join(p), to_dir)
            except IOError, e:
                logging.error("moving %s to %p failed with error: %s",
                             p, to_dir, e)
                raise e

    def aquire_lock(self):
        """Aquire a lock on the lock file"""
        global _lock
        logging.debug("Creating lockfile %s", self.lockfile)
        while True:
            _lock = LockFile(self.lockfile)
            if _lock.get():
                break
            else:
                logging.warn("Failed to acquire lock, Sleeping...")
                time.sleep(2)
        return True

    def release_lock(self):
        global _lock
        logging.debug("Removing lockfile %s", self.lockfile)
        hasattr(_lock, 'release') and _lock.release()

    def revisions(self, dir):
        """Check in a directory to see if there are any revision numbers."""
        files = os.listdir(dir)
        fdirs = {}
        for f in files:
            fdirs[f] = [line.strip() for line in open(os.path.join(dir,f)).readlines()]
        return fdirs

    def ensure_dirs(self, dirs):
        for d in dirs:
            if not os.path.exists(d):
                os.mkdir(d)

