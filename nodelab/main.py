import argparse
import logging
from pathlib import Path

from nodelab.core.cache import Cache
from nodelab.core.engine import Engine
from nodelab.core.scanner import Scanner
from nodelab.core.workflow import Workflow

logger = logging.getLogger(__name__)


def setup_logging(output_dir=None, level="INFO"):
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    handlers = [logging.StreamHandler()]

    if output_dir:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        log_file_path = output_dir / "workflow.log"
        file_handler = logging.FileHandler(log_file_path)
        handlers.append(file_handler)

    logging.basicConfig(
        level=level, format=log_format, datefmt=datefmt, handlers=handlers
    )


def main():
    # --- Setup ---

    # Set up argument parser
    parser = argparse.ArgumentParser(prog="NodeLab", description="Run a workflow.")

    # Add arguments
    parser.add_argument("workflow_file", help="Path to the workflow file to execute")
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Output directory where workflow, log and artifacts will be stored",
    )
    parser.add_argument(
        "-p",
        "--project_dir",
        help="Project directory (default: current working directory)",
        default=Path.cwd(),
    )
    parser.add_argument(
        "-c",
        "--cache_file",
        help="Cache file (default: cwd/.nodelab-cache.yaml)",
        default=Path.cwd() / ".nodelab-cache.yaml",
    )
    parser.add_argument(
        "-l",
        "--level",
        help="Set the logging level (default: INFO)",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the arguments
    workflow_file = Path(args.workflow_file).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    project_dir = Path(args.project_dir).resolve()
    cache_file = Path(args.cache_file).resolve()
    level = args.level

    # Set up logging
    setup_logging(output_dir=output_dir, level=level)

    logger.info("--- Arguments ---")
    logger.info("Workflow file: %s", workflow_file)
    logger.info("Output directory: %s", output_dir)
    logger.info("Project directory: %s", project_dir)
    logger.info("Cache file: %s", cache_file)
    logger.info("Log level: %s", level)

    # --- Preparation and Execution ---

    logger.info("--- Preparation ---")
    # Load workflow
    workflow = Workflow(workflow_file)
    workflow.load()

    # Copy workflow to output directory
    if output_dir:
        workflow.copy(output_dir)

    # Load cache
    cache = Cache(cache_file)
    cache.load()

    # Find nodes
    scanner = Scanner(cache, project_dir)
    scanner.scan_project_directory()
    cache.write()

    logger.info("--- Execution ---")

    # Run workflow
    engine = Engine(workflow, cache)
    engine.run()


if __name__ == "__main__":
    main()
