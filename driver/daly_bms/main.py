# simple inquiry example
import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
print("Found {} devices.".format(len(nearby_devices)))

for addr, name, klass in nearby_devices:
    print("  {} - {} - {}".format(addr, name, klass))

    target = addr
    if target == "all":
        target = None

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
        print("Found {} services.".format(len(services)))
    else:
        print("No services found.")

    for svc in services:
        print("\nService Name:", svc["name"])
        print("    Host:       ", svc["host"])
        print("    Description:", svc["description"])
        print("    Provided By:", svc["provider"])
        print("    Protocol:   ", svc["protocol"])
        print("    channel/PSM:", svc["port"])
        print("    svc classes:", svc["service-classes"])
        print("    profiles:   ", svc["profiles"])
        print("    service id: ", svc["service-id"])