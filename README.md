# webcam-riser

3D-printable riser that sits on the top edge of a monitor and holds a webcam 10 mm higher. Modelled in Python with [build123d](https://github.com/gumyr/build123d).

## Shape

- A hollow body rests on the monitor top edge. A front lip hangs 6 mm down the monitor front face to keep it in place.
- Above the body, a camera holder: a 5.3 mm slot under a flat roof, for a 5 mm thick element (the camera clip/foot).
- The slot is closed at one end by a wall and at the other by a 2 mm lip hanging from the roof, which overhangs the body by 2 mm. It is open at front and back.
- Body width 40 mm, roof 42 mm. Overall 42 x 11 x 23.3 mm.

Mirror on X in the slicer if you want the closed end on the other side.

## Build

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run python riser.py   # writes out/riser.stl, out/riser.step, out/riser.design.stl
uv run python render.py  # writes out/riser.png (preview)
uv run pytest            # geometry tests
```

- `out/riser.stl` / `out/riser.step`: print pose, ready to slice.
- `out/riser.design.stl`: mounted pose, for reference.

## Printing

The part is exported lying on its front lip: every wall is vertical, no supports and no brim needed.

## Customising

All dimensions are constants at the top of `riser.py` (width, rise, depth, wall thickness, slot gap, lip size). Change them, rerun `riser.py`, and update the expected values in `test_riser.py`.

## License

Public domain, under [The Unlicense](LICENSE).
