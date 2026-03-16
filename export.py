import os
import argparse
import nbformat
from nbconvert import MarkdownExporter


def convert_notebook(notebook_path):
    # 1. Path Setup
    abs_path = os.path.abspath(notebook_path)
    base_dir = os.path.dirname(abs_path)
    notebook_name = os.path.splitext(os.path.basename(abs_path))[0]
    rel_assets_path = os.path.join("assets", f"{notebook_name}_files")
    full_assets_path = os.path.join(base_dir, rel_assets_path)
    os.makedirs(full_assets_path, exist_ok=True)

    # 2. Load Notebook
    with open(abs_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # 3. Pre-process cells for Collapsible Sections
    for cell in nb.cells:
        # Check if cell is marked as collapsed in metadata
        is_collapsed = cell.metadata.get("jupyter", {}).get(
            "source_hidden", False
        ) or cell.metadata.get("collapsed", False)

        if is_collapsed and cell.cell_type == "code":
            # Wrap the code in MkDocs ??? toggle syntax
            # You can change 'Snippet' to a custom title if needed
            header = '???+ info "Click to expand code"\n'
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
    md_filename = os.path.join(base_dir, f"{notebook_name}.md")
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    args = parser.parse_args()
    convert_notebook(args.notebook)
