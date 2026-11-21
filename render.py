from pathlib import Path

import pyvista as pv

pv.OFF_SCREEN = True


def render(stl: Path, out: Path) -> None:
    mesh = pv.read(str(stl))
    b = mesh.bounds
    sx, sy, sz = b[1] - b[0], b[3] - b[2], b[5] - b[4]
    bed = pv.Plane(center=(0, 0, -0.3), i_size=80, j_size=80)
    cams: dict[str, list[tuple[float, float, float]]] = {
        "iso": [(60, -70, 60), (0, 0, sz / 2), (0, 0, 1)],
        "top": [(0, 0, 150), (0, 0, 0), (0, 1, 0)],
        "side": [(0, -140, sz / 2), (0, 0, sz / 2), (0, 0, 1)],
        "front": [(140, 0, sz / 2), (0, 0, sz / 2), (0, 0, 1)],
    }
    pl = pv.Plotter(shape=(2, 2), window_size=[1400, 1200], off_screen=True)
    for i, (name, cam) in enumerate(cams.items()):
        pl.subplot(i // 2, i % 2)
        pl.add_text(name, font_size=11)
        pl.add_mesh(bed, color="#2f3540")
        pl.add_mesh(mesh, color="lightgrey", smooth_shading=False)
        pl.camera_position = cam
        pl.camera.parallel_projection = name != "iso"
        pl.camera.parallel_scale = 28.0
    pl.subplot(0, 0)
    pl.add_text(
        f"bbox {sx:.1f} x {sy:.1f} x {sz:.1f} mm - no brim",
        position="lower_left",
        font_size=11,
    )
    pl.screenshot(str(out))
    pl.close()


if __name__ == "__main__":
    out_dir = Path(__file__).parent / "out"
    render(out_dir / "riser.stl", out_dir / "riser.png")
