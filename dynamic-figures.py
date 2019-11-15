import time

class Line:
        def __init__(self, x1, y1, x2, y2, clr):
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2
                self.color = clr

lines = []
N = 50
vx1 = 9 * 2
vy1 = 21 * 2
vx2 = 11 * 2
vy2 = 19 * 2

c = 0
colors = [
        "#FF0000",
        "#FF4000",
        "#A0A000",
        "#40FF00",
        "#00FF00",
        "#00FF40",
        "#00A0A0",
        "#0040FF",
        "#0000FF",
        "#0040FF",
        "#00A0A0",
        "#00FF40",
        "#00FF00",
        "#40FF00",
        "#A0A000",
        "#FF4000",
        ]


def color():
        global c
        global colors
        c += 1
        return "%s" % colors[c % len(colors)]

def clampadd(x, dx, dt):
        x += dx * dt
        if x < 0:
                x = 0
                dx = -dx
        if x > 100:
                x = 100
                dx = -dx
        return (x, dx)

def tick():
        global lines
        global N
        global vx1
        global vy1
        global vx2
        global vy2

        dt = 0.05

        if len(lines) > 0:
                newline = Line(lines[-1].x1, lines[-1].y1, lines[-1].x2, lines[-1].y2, color())
        else:
                newline = Line(17, 1, 1, 13, color())

        newline.x1, vx1 = clampadd(newline.x1, vx1, dt)
        newline.y1, vy1 = clampadd(newline.y1, vy1, dt)
        newline.x2, vx2 = clampadd(newline.x2, vx2, dt)
        newline.y2, vy2 = clampadd(newline.y2, vy2, dt)

        if len(lines) > N:
                lines = lines[1:]
        lines.append(newline)

        draw = []
        for l in lines:
                draw.append("line %f %f %f %f %s" % (l.x1, l.y1, l.x2, l.y2, l.color))
                draw.append("line %f %f %f %f %s" % (100 - l.x1, l.y1, 100 - l.x2, l.y2, l.color))
                draw.append("line %f %f %f %f %s" % (l.x1, 100 - l.y1, l.x2, 100 - l.y2, l.color))
                draw.append("line %f %f %f %f %s" % (100 - l.x1, 100 - l.y1, 100 - l.x2, 100 - l.y2, l.color))
        figure_set("channel_guid_here", draw)
        timeout(50, tick)

timeout(500, tick)
