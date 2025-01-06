from xml.etree import ElementTree
import dbus


def list_paths(
    bus: dbus.Bus,
    service: str,
    search_path: str = "/",
    current_path: str = "",
    paths=None,
):
    """List the paths from a dbus service

    Args:
        bus (dbus.Bus): Bus
        service (str): the service to connect to (e.g., org.freedesktop.DBus)
        search_path (str, optional): The path to search in. Defaults to "/".
        current_path (str, optional): Used in iterations. Defaults to "".
        paths (list, optional): Current found paths. Defaults to None.

    Returns:
        list: Found paths
    """
    if paths is None:
        paths = []
    if not search_path.startswith("/"):
        search_path = "/" + search_path
    if current_path == "":
        current_path = search_path
    if search_path != current_path and current_path not in paths:
        paths.append(current_path)
    obj = bus.get_object(service, current_path)
    # adapted from https://unix.stackexchange.com/a/203678
    iface = dbus.Interface(obj, "org.freedesktop.DBus.Introspectable")
    xml_string = iface.Introspect()
    for child in ElementTree.fromstring(xml_string):
        if child.tag == "node":
            if current_path == "/":
                current_path = ""
            new_path = "/".join((current_path, child.attrib["name"]))
            list_paths(bus, service, search_path, new_path, paths)
    return paths


if __name__ == "__main__":

    session_bus = dbus.SessionBus()
    print(
        list_paths(
            session_bus, "org.kde.konsole-311544", "/Sessions", "", ["/Sessions/1"]
        )
    )
    print(list_paths(session_bus, "org.kde.plasmashell"))
