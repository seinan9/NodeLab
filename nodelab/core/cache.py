import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class Cache:
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        self.node_files = {}
        self.file_mtimes = {}

    def load(self):
        if self.cache_file.exists():
            try:
                with self.cache_file.open("r", encoding="utf-8") as f:
                    cache = yaml.safe_load(f)
                    self.node_files = cache.get("node_files", {})
                    self.file_mtimes = cache.get("file_mtimes", {})
                    logger.info("Loaded cache")
            except Exception as e:
                logger.warning("Unexpected error while loading cache: %s", e)
                self._reset_cache()
        else:
            logger.warning("Cache file %s not found", self.cache_file)
            self._reset_cache()

    def write(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            yaml.dump(
                {
                    "node_files": self.node_files,
                    "file_mtimes": self.file_mtimes,
                },
                f,
            )
            logger.info("Wrote cache")

    def update(self, node_files, file_mtimes):
        self.node_files = node_files
        self.file_mtimes = file_mtimes
        logger.info("Updated cache")

    def _reset_cache(self):
        self.node_files = {}
        self.file_mtimes = {}
        logger.warning("Cache reset due to errors or missing file")
