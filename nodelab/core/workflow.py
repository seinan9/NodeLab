import logging
import shutil
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class Workflow:

    def __init__(self, workflow_file: Path):
        self.workflow_file = workflow_file
        self.nodes = {}
        self.results = {}

    # Load the workflow
    def load(self):
        if not self.workflow_file.exists():
            logger.error("Workflow file not found: %s", self.workflow_file)
            raise FileNotFoundError(f"Workflow file not found: {self.workflow_file}")

        with open(self.workflow_file, "r", encoding="utf-8") as f:
            workflow_data = yaml.safe_load(f)

        if not isinstance(workflow_data, dict) or "nodes" not in workflow_data:
            logger.error("Invalid workflow structure")
            raise ValueError("Invalid workflow structure")

        self.nodes = workflow_data["nodes"]
        logger.info("Loaded workflow with %d nodes", len(self.nodes))

    # Write the workflow
    def write(self, output_file: Path):
        with output_file.open("w", encoding="utf-8") as f:
            yaml.dump({"nodes": self.nodes}, f)
        logger.info("Saved workflow: %s", output_file)

    def copy(self, output_dir: Path):
        destination = output_dir / "workflow.yaml"
        shutil.copy(self.workflow_file, destination)
        logger.info("Copied workflow to output directory")
