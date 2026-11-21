# webcam-riser

3D-printable webcam riser that sits on the monitor top edge, modelled with build123d in `riser.py`. `uv run python riser.py` exports `out/riser.stl` (print pose), `out/riser.step`, `out/riser.design.stl` (mounted pose). `uv run python render.py` renders `out/riser.png`. Tests: `uv run pytest`.

## Orientation

The design frame built by `riser()` IS the mounted pose:

- Z up. X runs along the 40 mm width (parallel to the monitor top edge). Y is depth, from the front lip (Y = 0) toward the back of the monitor.
- Top plate (Z = RISE - WALL .. RISE, i.e. 8.8 .. 10) is the top of the mount. Anything that holds the camera goes on or above it (Z > 10).
- Bottom plate (Z = 0 .. WALL) rests on the monitor top edge. The monitor occupies Y >= FRONT_T, Z <= 0.
- Front lip (Y = 0 .. FRONT_T) hangs down to Z = -FRONT_DROP over the monitor front face.
- Hollow channel between top and bottom plate, open at the back (Y = TOP_DEPTH).
- Camera holder (`holder()`) above the top plate: roof (Z = RISE + GAP .. RISE + GAP + HOLDER_T) spanning X = 0 .. WIDTH + LIP_T, leaving a GAP = 5.3 mm slot for a 5 mm element. The end wall closes the slot at X = 0. At the other end the roof overhangs the top plate by LIP_T, and a lip (LIP_T thick) hangs LIP_H = 2 mm down from it at X = WIDTH .. WIDTH + LIP_T, outside the top plate, so the element is held in X between end wall and lip. The slot is open at front and back. The roof top stays flat (no dent). Mirror X in the slicer for the opposite hand.

Print pose (`print_pose`): rotated +90 deg about X, front lip flat on the bed. Seen along X in the slicer: the left wall (rounded corner at the bed) is the top plate, the right wall is the bottom plate, the short foot to the right of it is the front drop, and the monitor sits to the right of the right wall.
