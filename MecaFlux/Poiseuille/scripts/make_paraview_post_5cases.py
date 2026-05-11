#!/usr/bin/env python3
"""Build a ParaView state and batch screenshots for Poiseuille case0..case4."""

import os
from paraview.simple import *
from paraview import simple as pvs


ROOT = "/home/chrisvhk/Work_OpenFoam/WorkSpace/MecaFlux/Poiseuille"
OUT_STATE = os.path.join(ROOT, "paraview_cases_foam.pvsm")
OUT_IMG_DIR = os.path.join(ROOT, "Results", "paraview_images")
OUT_OVERVIEW_IMG = os.path.join(OUT_IMG_DIR, "U_cases_overview.png")


def save_case_screenshots(render_view, reader, case_name):
    """Export U, p and slice screenshots for one case."""
    HideAll(render_view)

    surface_display = Show(reader, render_view, "UnstructuredGridRepresentation")
    surface_display.Representation = "Surface"
    render_view.ResetCamera(False)

    ColorBy(surface_display, ("CELLS", "U", "Magnitude"))
    surface_display.SetScalarBarVisibility(render_view, True)
    SaveScreenshot(
        os.path.join(OUT_IMG_DIR, f"U_{case_name}_surface.png"),
        render_view,
        ImageResolution=[1920, 1080],
    )

    ColorBy(surface_display, ("CELLS", "p"))
    surface_display.SetScalarBarVisibility(render_view, True)
    SaveScreenshot(
        os.path.join(OUT_IMG_DIR, f"p_{case_name}_surface.png"),
        render_view,
        ImageResolution=[1920, 1080],
    )

    slice_filter = Slice(registrationName=f"slice_{case_name}", Input=reader)
    slice_filter.SliceType = "Plane"
    slice_filter.HyperTreeGridSlicer = "Plane"
    slice_filter.SliceOffsetValues = [0.0]
    slice_filter.SliceType.Normal = [0.0, 0.0, 1.0]

    UpdatePipeline(proxy=reader)
    bounds = reader.GetDataInformation().GetBounds()
    if bounds is not None and len(bounds) == 6:
        cx = 0.5 * (bounds[0] + bounds[1])
        cy = 0.5 * (bounds[2] + bounds[3])
        cz = 0.5 * (bounds[4] + bounds[5])
        slice_filter.SliceType.Origin = [cx, cy, cz]

    Hide(reader, render_view)
    slice_display = Show(slice_filter, render_view, "GeometryRepresentation")
    slice_display.Representation = "Surface"
    ColorBy(slice_display, ("CELLS", "U", "Magnitude"))
    slice_display.SetScalarBarVisibility(render_view, True)
    render_view.ResetCamera(False)
    SaveScreenshot(
        os.path.join(OUT_IMG_DIR, f"U_{case_name}_slice.png"),
        render_view,
        ImageResolution=[1920, 1080],
    )

    Hide(slice_filter, render_view)


def main() -> None:
    os.makedirs(OUT_IMG_DIR, exist_ok=True)

    if hasattr(pvs, "_DisableFirstRenderCameraReset"):
        pvs._DisableFirstRenderCameraReset()

    render_view = GetActiveViewOrCreate("RenderView")
    render_view.ViewSize = [1920, 1080]
    render_view.Background = [1.0, 1.0, 1.0]

    readers = []

    for i in range(5):
        case = f"case{i}"
        foam_path = os.path.join(ROOT, case, f"{case}.foam")
        if not os.path.exists(foam_path):
            raise FileNotFoundError(f"Missing file: {foam_path}")

        reader = OpenFOAMReader(registrationName=case, FileName=foam_path)
        reader.MeshRegions = ["internalMesh"]
        reader.CellArrays = ["U", "p"]
        readers.append(reader)

        # Shift each case so all 5 are visible in one render view.
        shifted = Transform(registrationName=f"{case}_shift", Input=reader)
        shifted.Transform.Translate = [0.0, i * 1.5, 0.0]

        display = Show(shifted, render_view, "UnstructuredGridRepresentation")
        ColorBy(display, ("CELLS", "U", "Magnitude"))
        display.SetScalarBarVisibility(render_view, i == 0)

    animation = GetAnimationScene()
    animation.UpdateAnimationUsingDataTimeSteps()
    try:
        animation.GoToLast()
    except Exception:
        pass

    render_view.ResetCamera(False)

    # Keep one common color scale; user can tune this later in GUI.
    u_lut = GetColorTransferFunction("U")
    u_lut.RescaleTransferFunction(0.0, 1.0)

    SaveScreenshot(OUT_OVERVIEW_IMG, render_view, ImageResolution=[1920, 1080])

    # Export case-by-case screenshots from the original (non-shifted) readers.
    for i, reader in enumerate(readers):
        save_case_screenshots(render_view, reader, f"case{i}")

    # Restore overview before saving state.
    HideAll(render_view)
    for i in range(5):
        Show(FindSource(f"case{i}_shift"), render_view, "UnstructuredGridRepresentation")

    SaveState(OUT_STATE)
    SaveScreenshot(OUT_OVERVIEW_IMG, render_view, ImageResolution=[1920, 1080])

    print(f"State generated: {OUT_STATE}")
    print(f"Overview image:  {OUT_OVERVIEW_IMG}")
    print(f"Batch images:    {OUT_IMG_DIR}")


if __name__ == "__main__":
    main()
