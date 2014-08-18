import os, subprocess

from itty import get, post, run_itty


@get('/env/(?P<name>\w+)')
def lookup_environment_variable(request, name):
    return os.environ[name]


@get("/freespace")
def compute_free_diskspace(request):
    return subprocess.check_output("df")


@get("/tail_form")
def tail_form(request):
    return open("tail.html").read()


@post("/tail")
def tail(request):
    file_ = request.POST.get("file", "/var/log/messages")
    return subprocess.check_output(["tail", file_])


run_itty()
