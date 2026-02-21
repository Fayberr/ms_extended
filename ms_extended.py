import system.lib.minescript as m
import time, random, math
from java import JavaClass

def look(target_yaw, target_pitch, duration=0.22, steps=70):
    CONFIRM_YAW_PITCH = False  # If it should manuallly correct at the end (If you need exact Yaw and Pitch

    sy, sp = m.player_orientation()

    def angle_diff(a, b):
        return (b - a + 180) % 360 - 180

    dy = angle_diff(sy, target_yaw)
    dp = target_pitch - sp

    if abs(dy) < 1.0 and abs(dp) < 1.0:
        m.player_set_orientation(target_yaw, target_pitch)
        return

    step_time = duration / steps

    power = 5

    for i in range(1, steps + 1):
        t = i / steps

        if t < 0.5:
            s = 0.5 * (2 * t) ** power
        else:
            s = 1 - 0.5 * (2 * (1 - t)) ** power

        jy = (1 - abs(0.5 - t) * 2) * 0.2

        m.player_set_orientation(
            sy + dy * s + random.uniform(-jy, jy),
            sp + dp * s + random.uniform(-jy * 0.7, jy * 0.7)
        )

        time.sleep(step_time)

    if CONFIRM_YAW_PITCH:
        m.player_set_orientation(target_yaw, target_pitch)

def json_entities():
    entities = m.entities()

    if not entities:
        return []

    ref = entities[0].position

    def dist(e):
        x1, y1, z1 = ref
        x2, y2, z2 = e.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    entities_sorted = sorted(entities, key=dist)

    json_entities = []

    for entity in entities_sorted:
        entry = {
            "name": entity.name,
            "type": entity.type,
            "uuid": entity.uuid,
            "position": entity.position,
            "orientation": [entity.yaw, entity.pitch]
        }
        json_entities.append(entry)

    return json_entities

def target_yaw_pitch_entity(player_pos, entity_pos):
    px, py, pz = player_pos
    ex, ey, ez = entity_pos

    dx = ex - px
    dy = ey - py
    dz = ez - pz

    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = math.degrees(-math.atan2(dy, math.sqrt(dx * dx + dz * dz)))

    return yaw, pitch


def get_tablist():
    m.set_default_executor(m.script_loop)

    Minecraft = JavaClass("net.minecraft.client.Minecraft")
    mc = Minecraft.getInstance()

    connection = mc.getConnection()
    if not connection:
        return []

    players = connection.getOnlinePlayers()
    tablist = []

    for info in players:
        comp = info.getTabListDisplayName()
        if not comp:
            continue

        text = comp.getString()
        tablist.append(text)

    return tablist
