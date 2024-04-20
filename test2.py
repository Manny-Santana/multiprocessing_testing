

for t in enumerate():
    if not t.daemon and t.is_alive():
        print(t)
    