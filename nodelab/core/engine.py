import importlib.util
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class Engine:

    def __init__(self, workflow, cache):
        self.workflow = workflow
        self.cache = cache

    def run(self):
        total_nodes = len(self.workflow.nodes)
        workflow_start_time = time.time()
        logger.info("Executing workflow...")

        for index, node in enumerate(self.workflow.nodes, start=1):
            node_name = node["node"]
            node_id = node.get("id", node_name)
            params = node.get("params", {})

            # Import and preprare node
            node_class = self._import_node(node_name)
            resolved_params = self._resolve_params(params)

            # Log start
            logger.info("Executing node %s...", node_name)

            # Execute node and measure time
            start_time = time.time()
            results = node_class.run(**resolved_params)
            duration = time.time() - start_time

            # Handle results
            if not isinstance(results, tuple):
                results = (results,)
            output_keys = list(node_class.outputs.keys())
            self.workflow.results[node_id] = dict(zip(output_keys, results))

            # Log end with execution time
            logger.info(
                "Executed node %s in %.3f seconds",
                node_name,
                duration,
            )

            progress = (index / total_nodes) * 100
            logger.info("Progress: %d/%d (%.2f%%)", index, total_nodes, progress)

        workflow_duration = time.time() - workflow_start_time
        logger.info("Executed workflow in %.3f seconds", workflow_duration)

    def _import_node(self, node_name):
        filepath = self.cache.node_files[node_name]
        module_name = Path(filepath).stem

        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, node_name)

    def _resolve_params(self, params):
        if isinstance(params, str) and params.startswith("$"):
            ref_path = params[1:].split(".")
            return self.workflow.results[ref_path[0]][ref_path[1]]
        if isinstance(params, dict):
            return {k: self._resolve_params(v) for k, v in params.items()}
        if isinstance(params, list):
            return [self._resolve_params(v) for v in params]
        return params
