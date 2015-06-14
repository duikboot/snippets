should_we = lambda: False # e.g. NO and
destroy_world = lambda: "Call forth Cthulhu, eater of worlds" # then if
if all(f() for f in (should_we, destroy_world)):
    print("are we still here?")
if any(f() for f in (should_we, destroy_world)):
    print("Yes we should")
