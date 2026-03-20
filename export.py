import os
import shutil
import argparse
import nbformat
from nbconvert import MarkdownExporter


def convert_notebook(notebook_path):
    # 1. Path Setup
    abs_path = os.path.abspath(notebook_path)
    base_dir = os.path.dirname(abs_path)
    notebook_name = os.path.splitext(os.path.basename(abs_path))[0]
    markdown_dir = os.path.join(base_dir, "markdowns")
    rel_assets_path = os.path.join("assets", f"{notebook_name}_files")
    full_assets_path = os.path.join(markdown_dir, rel_assets_path)
    os.makedirs(markdown_dir, exist_ok=True)
    # Clear assets folder if it exists to prevent accumulation of old figures
    if os.path.exists(full_assets_path):
        shutil.rmtree(full_assets_path)
    os.makedirs(full_assets_path, exist_ok=True)

    # 2. Load Notebook
    with open(abs_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # 3. Pre-process cells for Collapsible Sections
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue

        # Check metadata-based collapsing (existing)
        is_collapsed = cell.metadata.get("jupyter", {}).get(
            "source_hidden", False
        ) or cell.metadata.get("collapsed", False)
        collapse_title = "Click to expand code"  # default title

        # Check for marker-based collapsing (new)
        lines = cell.source.splitlines()
        marker_title = None
        marker_line_idx = None

        for idx, line in enumerate(lines):
            if line.strip().startswith("## COLLAPSE:"):
                marker_title = line.split("## COLLAPSE:", 1)[1].strip()
                marker_line_idx = idx
                is_collapsed = True
                collapse_title = marker_title
                break

        # Remove the marker line from the cell if found
        if marker_line_idx is not None:
            lines.pop(marker_line_idx)
            cell.source = "\n".join(lines)

        # Wrap in collapsible section if marked
        if is_collapsed:
            header = f'???+ info "{collapse_title}"\n'
            indented_source = "\n".join(
                ["    " + line for line in cell.source.splitlines()]
            )
            cell.source = header + indented_source

    # 4. Export to Markdown
    md_exporter = MarkdownExporter()
    (body, resources) = md_exporter.from_notebook_node(nb)

    # 5. Fix Image Links & Save Figures
    images = resources.get("outputs", {})
    for img_name, img_data in images.items():
        img_full_path = os.path.join(full_assets_path, img_name)
        with open(img_full_path, "wb") as f:
            f.write(img_data)

        # String replacement for image links
        body = body.replace(f"({img_name})", f"({rel_assets_path}/{img_name})")

    # 6. Write Final MD
    md_filename = os.path.join(markdown_dir, f"{notebook_name}.md")
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    args = parser.parse_args()
    convert_notebook(args.notebook)
