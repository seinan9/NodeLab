import ast
import logging
import time

logger = logging.getLogger(__name__)


class Scanner:

    def __init__(self, cache, project_dir):
        self.cache = cache
        self.project_dir = project_dir

    def scan_project_directory(self):
        logger.info("Scanning project directory for nodes")
        start_time = time.time()

        # Get up to date mtimes
        file_mtimes = {
            str(file_path): file_path.stat().st_mtime
            for file_path in self.project_dir.rglob("*.py")
            if file_path.is_file()
        }

        # Identify nodes from the cache that are valid
        valid_node_files = {
            node_name: file_path
            for node_name, file_path in self.cache.node_files.items()
            if file_path in file_mtimes
            and file_mtimes[file_path] == self.cache.file_mtimes.get(file_path)
        }

        # Identify files that require parsing
        files_to_parse = {
            file_path
            for file_path, mtime in file_mtimes.items()
            if self.cache.file_mtimes.get(file_path) is None
            or mtime != self.cache.file_mtimes[file_path]
        }

        # Extract new nodes from files
        new_node_files = {}
        for file_path in files_to_parse:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        if any(
                            isinstance(decorator, ast.Name) and decorator.id == "node"
                            for decorator in node.decorator_list
                        ):
                            new_node_files[node.name] = file_path

        # Merge old valid nodes with new ones
        valid_node_files.update(new_node_files)

        duration = time.time() - start_time

        logger.info(
            "Scanned %i file(s), %i updated, %i new node(s) found, in %.3f seconds",
            len(file_mtimes),
            len(files_to_parse),
            len(new_node_files),
            duration,
        )

        # Update cache
        self.cache.update(valid_node_files, file_mtimes)
