"""Compile a generated .tex into a PDF."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .context import ROOT
from .render import TEMPLATE_DIR

BUILD_DIR = ROOT / "build"


class BuildError(RuntimeError):
    pass


@dataclass
class BuildResult:
    pdf: Path
    pages: int


def compile_pdf(tex_path: Path, jobname: str) -> BuildResult:
    out_dir = tex_path.parent
    aux_dir = BUILD_DIR / out_dir.name
    aux_dir.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "TEXINPUTS": f"{TEMPLATE_DIR}{os.pathsep}"}
    cmd = [
        "latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        f"-jobname={jobname}", f"-outdir={out_dir}", f"-auxdir={aux_dir}", str(tex_path),
    ]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    pdf = out_dir / f"{jobname}.pdf"
    if proc.returncode != 0 or not pdf.exists():
        log = aux_dir / f"{jobname}.log"
        tail = log.read_text(errors="replace")[-3000:] if log.exists() else proc.stdout[-3000:]
        raise BuildError(f"latexmk failed for {tex_path}:\n{tail}")

    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", info, re.M)
    pages = int(m.group(1)) if m else -1
    return BuildResult(pdf=pdf, pages=pages)
