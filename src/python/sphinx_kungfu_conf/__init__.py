import inspect
import json
import semver
import os
from os import path


version_info = {
    "current_version": "latest",
    "versions": list(),
    "has_prerelease": os.environ.get("KUNGFU_DOC_HAS_PRERELEASE", "false") == "true",
}

download_info = {"current_version": "latest", "versions": list()}


def get_version(doc_root):
    parse = semver.VersionInfo.parse
    package_json_path = path.join(doc_root, "package.json")
    with open(package_json_path, "r") as package_json_file:
        package_json = json.load(package_json_file)
    if "kungfuVersion" in package_json:
        return parse(package_json["kungfuVersion"])
    return parse(package_json["dependencies"]["@kungfu-trader/kungfu-core"])


def get_version_label(doc_version):
    return f"v{doc_version.major}.{doc_version.minor}"


def setup(module):
    """
    Setup sphinx configuration. Example usage:
        __import__('sphinx_kungfu_conf').setup(globals())

        Parameters:
            module: expected value is `globals()`
    """
    if type(module) is not dict:
        return

    doc_root = path.realpath(path.join(path.dirname(module["__file__"]), ".."))
    docs_dir = path.realpath(path.join(doc_root, ".."))

    for doc_dir in [
        path.join(docs_dir, x) for x in sorted(os.listdir(docs_dir), reverse=True)
    ]:
        try:
            doc_version = get_version(doc_dir)
            doc_version_label = get_version_label(doc_version)
            doc_href = f"../{doc_version_label}/index.html"
            download_href = f"../{doc_version_label}/Kungfu-Doc-{doc_version_label}.pdf"
            if not doc_version.prerelease:
                version_info["versions"].append(
                    (doc_version_label, str(doc_version), doc_href)
                )
                download_info["versions"].append(
                    (doc_version_label, str(doc_version), download_href)
                )
        except:
            pass

    version_info["current_version"] = str(get_version(doc_root))
    download_info["current_version"] = str(get_version(doc_root))

    from . import conf

    exclued_private = lambda t: not (t[0].startswith("_"))
    exclued_modules = lambda v: not (inspect.ismodule(v))

    conf_dict = dict(filter(exclued_private, inspect.getmembers(conf, exclued_modules)))

    for key in conf_dict:
        value = conf_dict[key]
        if type(value) is dict:
            origin = module.get(key, {})
            origin = {} if type(origin) is not dict else origin
            value = {**origin, **value}
        module[key] = value

    doc_static_dir = path.join(doc_root, "src", "_static")
    if path.exists(doc_static_dir):
        module["html_static_path"].append(doc_static_dir)

    doc_templates_dir = path.join(doc_root, "src", "_templates")
    if path.exists(doc_templates_dir):
        module["templates_path"].append(doc_templates_dir)
