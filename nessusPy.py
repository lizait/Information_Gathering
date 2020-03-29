import sys
import requests
from nessrest import ness6rest


def doScanByNessus(login, password, targets, customPolicy,
                   policy="", customScanName="", url="https://127.0.0.1:8834", plugins="", insecure=True):
    """
    Scan by nessus API given results

    :param login: (string)
    :param password: (string)
    :param targets: (string) targets separate by ','
    :param customPolicy: (string) name of policies to use, if don't exist, will be created with this name
    :param policy: (string) if customPolicy don't exist, it will create using this template (discovery, basic or advanced)
    :param customScanName: (string) you can specify a custom scan name, else it will be same that customPolicy
    :param url: (string)
    :param plugins: (string) plugins to use in "advanced" scans
    :param insecure: (boolean) true to disable ssl
    :return: None
    """
    scan = ness6rest.Scanner(url=url, login=login, password=password, insecure=insecure)

    scan.action(action="policies/110", method="GET")

    if not customPolicy or not scan.policy_exists(customPolicy):
        print("Custom policy don't found, try to create new one")

        if policy == "discovery" or policy == "basic" or (policy == "advanced" and plugins):
            try:
                scan.action(action="editor/policy/templates", method="GET")
                template_uuid = ""
                for template in scan.res["templates"]:
                    if template["name"] == policy:
                        template_uuid = template["uuid"]
                        break
                if not template_uuid:
                    print("Policy template {} not found".format(policy))
                    return

                configuration = {"settings": {}}
                configuration.update({"uuid": template_uuid})
                configuration["settings"].update({"name": customPolicy})
                configuration["settings"].update({"safe_checks": "yes"})
                configuration["settings"].update({"scan_webapps": "no"})
                configuration["settings"].update({"report_paranoia": "Normal"})
                configuration["settings"].update({"provided_creds_only": "no"})
                configuration["settings"].update({"thorough_tests": "no"})
                configuration["settings"].update({"report_verbosity": "Normal"})
                configuration["settings"].update({"silent_dependencies": "yes"})
                configuration["settings"].update({"cisco_offline_configs": ""})
                configuration["settings"].update({"network_receive_timeout": "5"})
                configuration["settings"].update({"max_checks_per_host": "5"})

                if policy == "discovery":
                    configuration["settings"].update({"discovery_mode": "Host enumeration"})

                if policy == "basic":
                    configuration["settings"].update({"discovery_mode": "Port scan (all ports)"})

                scan.action(action="policies", method="POST", extra=configuration)

                scan.policy_id = scan.res["policy_id"]

                if policy == "advanced":
                    scan.plugins_info(plugins)
                    scan._enable_plugins()

            except KeyError:
                print("policy id was not returned")
            except requests.exceptions.ConnectionError:
                raise Exception("Problem during connection with Nessus: {}".format(url))
            except:
                print("Unexpected error: {}".format(sys.exc_info()[1]))
        else:
            print("Policy template not available, please choose between discovery, basic and advanced")
            print("If you choose advanced, please specify plugins to use")

    else:
        scan.policy_set(customPolicy)

    scan.scan_add(targets, name=customScanName)

    scan.scan_run()
    scan.scan_results()
    kbs = scan.download_kbs()

    for hostname in kbs.keys():
        f = open(hostname, "w")
        f.write(kbs[hostname])
        f.close()
########################################################################################################################


if __name__ == '__main__':

    try:
        doScanByNessus("id", "mdp", "192.168.0.1", "policiesName", plugins="20811,12128", policy="discovery")
    except:
        t = sys.exc_info()
        print("Unexpected error:", sys.exc_info()[1])
    print("end")




