from ast import Assign, Name, literal_eval, parse
from pathlib import Path

import mkdocs_gen_files

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "my_first_adventure_game"
PACKAGE_ROOT = PROJECT_ROOT / "src" / PACKAGE_NAME


def _has_public_exports(init_path: Path) -> bool:
    syntax_tree = parse(init_path.read_text(encoding="utf-8"))

    for node in syntax_tree.body:
        if not isinstance(node, Assign):
            continue

        defines_all = any(
            isinstance(target, Name) and target.id == "__all__"
            for target in node.targets
        )

        if defines_all:
            return bool(literal_eval(node.value))

    return False


for init_path in sorted(PACKAGE_ROOT.glob("*/*/__init__.py")):
    if not _has_public_exports(init_path):
        continue

    layer, domain, _ = init_path.relative_to(PACKAGE_ROOT).parts
    domain_name = domain.replace("_", " ")
    package_name = ".".join((PACKAGE_NAME, layer, domain))

    if layer == "game":
        filename = f"game-{domain}.md"
        page_title = f"Game {domain_name} API"
    else:
        filename = f"{domain}.md"
        page_title = f"{domain_name.capitalize()} API"

    doc_path = Path("api", filename)

    with mkdocs_gen_files.open(doc_path, "w") as page:
        page.write(
            f"# {page_title}\n\n"
            f"See the [{domain_name} architecture page]"
            f"(../architecture/{domain}.md) for responsibilities, relationships,\n"
            "invariants, extension points, and change risks.\n\n"
            f"::: {package_name}\n"
        )

    mkdocs_gen_files.set_edit_path(
        doc_path.as_posix(),
        init_path.relative_to(PROJECT_ROOT).as_posix(),
    )
