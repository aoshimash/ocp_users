def create_new_idps(providers, secret, provider_name):
    provider_names = [ provider.get("name") for provider in providers ]
    
    if provider_name in provider_names:
        return providers

    new_provider = {
        "name": provider_name,
        "type": "HTPasswd",
        "mappingMethod": "claim",
        "htpasswd": {
            "fileData": {
                "name": secret
            }
        }
    }

    providers.append(new_provider)

    return providers


class FilterModule(object):
    def filters(self):
        return {
            'create_new_idps': create_new_idps
        }
