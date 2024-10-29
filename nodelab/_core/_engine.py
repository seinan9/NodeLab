import importlib.util
import os


def get_file_to_import(workflow, node_file_map):
    files_to_import = {}

    for node_name in workflow:
        file_path = node_file_map[node_name]
        if file_path in files_to_import:
            files_to_import[file_path].extend(node_name)
        else:
            files_to_import[file_path] = [node_name]

    return files_to_import


def bulk_import_files(files_to_import):
    for file_path, node_names in files_to_import.items():
        module_name = os.path.splitext(os.path.basename(file_path))[0]

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for node_name in node_names:
            globals()[node_name] = getattr(module, node_name)


def execute_workflow(workflow):
    results = {}

    for node_name, args in workflow.items():
        if node_name in globals():
            node_class = globals()[node_name]
            node_instance = node_class(**args)
            result = node_instance.run()
            results[node_name] = result

    return results
