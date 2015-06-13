#!/usr/bin/env python

import os
import subprocess
import sys

from hgapi.hgapi import Repo

#TODO: Create new Repo object for creating new branch?
'''
File: new_branch.py
Author: Arjen Dijkstra
Description: Create new branches for all repos, and some other mercurial tasks

    ## sequence of commands this script tries to replace
    ## hg pull
    ## hg up
    ## hg branch
    ## ./testit


    ## hg up release
    ## hg merge -r r6s3
    ## ./testit
    ## hg commit -m "merged with r6s3"
    ## hg branch r6-rc1
    ## hg commit -m "added r6-rc1"
    ## hg push --new-branch


    ## hg up production
    ## hg merge -r release
    ## ./testit
    ## hg commit -m "merge release 4 into production"
    ## hg push --new-branch
'''

## To make some lines more readable
JOIN = os.path.join


def get_repos(parentdir='.'):
    """Get de repositories for the given directory"""
    parentdir = os.path.realpath(parentdir)
    paths = (JOIN(parentdir, x) for x in JOIN(os.listdir(parentdir)))
    repos = (x for x in paths
             if os.path.isdir(x) and os.path.exists(JOIN(x, '.hg')))
    return repos


def test_it(repo):
    """Run test of repo and if necessary start mongo"""
    dir_ = os.getcwd()
    os.chdir(repo)
    print(os.getcwd())
    retcode = 0
    if os.path.exists('testit'):
        retcode = subprocess.call('./testit')
    os.chdir(dir_)
    return retcode


def run_npm_install(directory='.'):
    d = os.getcwd()
    os.chdir(directory)
    if os.path.exists('buildit'):
        install = subprocess.call(['./buildit'])
    elif os.path.exists('package.json'):
        install = subprocess.call(['npm', 'install'])
    os.chdir(d)
    return install


class ManageRepo(Repo):
    """Create e Repo object and do cool things with it"""
    def __init__(self, repo, username='arjend'):
        self.repo = repo
        self.directory = os.path.split(repo)[-1]
        self.username = username
        super(ManageRepo, self).__init__(self.repo, self.username)

    def create_new_branch(self, newbranch):
        """
        Create a new branch.
        Provide the branch from which you want to branch
        """
        # self.update(self.branch)
        try:
            self.hg_branch(newbranch)
            return 'succes'
        except Exception, e:
            print(e)
            return 'failure'

    def update(self, branch):
        """Update the repo to a revision"""
        self.branch = branch
        self.hg_update(self.branch)
        return self.hg_branch()

    def pull(self):
        """pull the latest changes"""
        out = self.hg_command('pull')
        return out

    def merge(self, reference):
        """Merge reference into self.branch"""
        # merge from into....
        # TODO: Can the 'merged from' always be the truth??
        try:
            message = self.hg_command("merge", reference)
            return message
        except Exception, e:
            print("Aaaah a merge failed has occured", e)
            return 'Failure'

    def push_newbranch(self):
        """Push the new branch to server
        hg push --new-branch"""
        try:
            self.hg_command('push', '--new-branch')
        except Exception, e:
            print(e)
        return

    def get_username(self):
        return self.username


