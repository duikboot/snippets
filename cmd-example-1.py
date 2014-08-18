# File: cmd-example-1.py
import cmd
import sys
import subprocess


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '

    def do_hello(self, arg):
        print "hello again", arg, "!"

    def help_hello(self):
        print "syntax: hello [message]",
        print "-- prints a hello message"

    def do_quit(self, arg):
        sys.exit(0)

    def do_shell(self, arg):
        args = arg.split()
        cmd = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        if not stderr:
            print stdout
        else:
            print stderr

    def help_shell(self):
        print "syntax: ! cmd"
        print "--- print cmd"

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"

    # shortcuts
    do_q = do_quit
    do_h = help


if __name__ == "__main__":
    cli = CLI()
    cli.cmdloop("""
                Welcome to the shell thingie.
                Use at your own risk
                """)
