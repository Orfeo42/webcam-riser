from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    BuildSketch,
    Part,
    Plane,
    Polygon,
    Pos,
    Sketch,
    export_step,
    export_stl,
    extrude,
    fillet,
)

WIDTH = 40.0
RISE = 10.0
TOP_DEPTH = 11.0
FRONT_DROP = 6.0
FRONT_T = 1.0
CORNER_R = 1.0
WALL = 1.2
GAP = 5.3
HOLDER_T = 2.0
LIP_H = 2.0
LIP_T = 2.0


def holder() -> Part:
    roof = Pos(0.0, 0.0, RISE + GAP) * Box(
        WIDTH + LIP_T,
        TOP_DEPTH,
        HOLDER_T,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    end_wall = Pos(0.0, 0.0, RISE) * Box(
        HOLDER_T,
        TOP_DEPTH,
        GAP + HOLDER_T,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    lip = Pos(WIDTH, 0.0, RISE + GAP - LIP_H) * Box(
        LIP_T,
        TOP_DEPTH,
        LIP_H + HOLDER_T,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    result = roof + end_wall + lip
    if not isinstance(result, Part):
        raise TypeError("holder union did not return a part")
    return result


def riser() -> Part:
    pts = [
        (0.0, RISE),
        (TOP_DEPTH, RISE),
        (TOP_DEPTH, 0.0),
        (FRONT_T, 0.0),
        (FRONT_T, -FRONT_DROP),
        (0.0, -FRONT_DROP),
    ]
    with BuildSketch(Plane.YZ) as sk:
        Polygon(*pts, align=None)
    profile = sk.sketch
    if not isinstance(profile, Sketch):
        raise TypeError("L profile did not build a sketch")
    body = extrude(profile, amount=WIDTH)
    front_top_edges = (
        body.edges()
        .filter_by(Axis.X)
        .filter_by_position(Axis.Z, RISE - 0.01, RISE + 0.01)
        .filter_by_position(Axis.Y, -0.01, 0.01)
    )
    rounded = fillet(front_top_edges, radius=CORNER_R)
    if not isinstance(rounded, Part):
        raise TypeError("fillet did not return a part")
    channel = Pos(-1.0, WALL, WALL) * Box(
        WIDTH + 2.0,
        TOP_DEPTH - WALL + 1.0,
        RISE - 2 * WALL,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    hollow = rounded - channel
    if not isinstance(hollow, Part):
        raise TypeError("channel cut did not return a part")
    combined = hollow + holder()
    if not isinstance(combined, Part):
        raise TypeError("holder union did not return a part")
    return combined


def print_pose(part: Part) -> Part:
    rotated = part.rotate(Axis.X, 90)
    bb = rotated.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * rotated


if __name__ == "__main__":
    out = Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    part = riser()
    posed = print_pose(part)
    bb = posed.bounding_box()
    print(
        f"print pose bbox {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}"
        f"  valid={posed.is_valid}  solids={len(posed.solids())}"
    )
    export_stl(posed, str(out / "riser.stl"))
    export_step(posed, str(out / "riser.step"))
    export_stl(part, str(out / "riser.design.stl"))
