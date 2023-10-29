objects = [[], []]


def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('존재하지 않는 오브젝트 제거')


def update_object():
    for layer in objects:
        for o in layer:
            o.update()


def render_object():
    for layer in objects:
        for o in layer:
            o.draw()
            