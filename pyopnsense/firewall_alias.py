from pyopnsense import client


class FirewallAliasClient(client.OPNClient):
    def search_item(self, searchPhrase=None, current=1, rowCount=100):
        """Search alias according given terms.

        :param string searchPhrase: search terms.
        :param int current: current page.
        :param int searchPhrase: number of alias per pages.
        """
        if searchPhrase is None:
            searchPhrase = str()

        body = dict(
            current=current, rowCount=rowCount, searchPhrase=searchPhrase
        )
        return self._post('firewall/alias/searchItem', body=body)

    def _save_item(
        self, endpoint, name, alias_type, content, proto=None,
        updatefreq=None, counters=None, description=None, enabled=None
        ):
        # Default value
        if proto is None:
            proto = str()
        if updatefreq is None:
            updatefreq = str()
        if counters is None:
            counters = str("0")
        if description is None:
            description = str()
        if enabled is None:
            enabled = str("1")

        alias = dict(
            enabled=enabled,
            name=name,
            type=alias_type,
            proto=proto,
            updatefreq=updatefreq,
            content="\n".join(content),
            counters=counters,
            description=description
        )
        network_content = ",".join(content)
        body = dict(
            alias=alias,
            network_content=network_content
        )

        return self._post(endpoint, json=body)

    def set_item(
        self, id, name, alias_type, content, proto=None, updatefreq=None,
        counters=None, description=None, enabled=None
        ):
        """Update an alias

        :param string id: alias identifier.
        :param string name: current page.
        :param string alias_type: type of alias: host, network, port, url,
        :                         urltable, geoip, networkgroup, external.
        :param list content: the network content in list format.
        :param string proto: the network content.
        :param string updatefreq: the network content.
        :param string counters: the network content.
        :param string description: The description.
        """

        endpoint = "{}/{}".format("firewall/alias/setItem", id)

        return self._save_item(
            endpoint,
            name,
            alias_type,
            content,
            proto,
            updatefreq,
            counters,
            description,
            enabled
        )

    def add_item(
        self,
        name, alias_type, content, proto=None, updatefreq=None, counters=None,
        description=None, enabled=None
        ):
        """Create an alias

        :param string id: alias identifier.
        :param string name: current page.
        :param string alias_type: type of alias: host, network, port, url,
        :                         urltable, geoip, networkgroup, external.
        :param list content: the network content in list format.
        :param string proto: the network content.
        :param string updatefreq: the network content.
        :param string counters: the network content.
        :param string description: The description.
        """

        endpoint = "firewall/alias/addItem/"

        return self._save_item(
            endpoint, name, alias_type, content, proto,
            updatefreq, counters, description, enabled
        )

    def delete_item(self, id):
        """Del item with given identifier.

        :param string id: alias identifier.
        """

        endpoint = "{}/{}".format("firewall/alias/delItem", id)

        return self._post(endpoint, json=dict())

    def get_item(self, id=None):
        """Get item with given identifier.

        :param string id: alias identifier.
        """
        if id is None:
            id = str()

        endpoint = "{}/{}".format("firewall/alias/getItem", id)

        return self._get(endpoint)

    def reconfigure(self):
        """Apply aliases.
        """

        return self._get("firewall/alias/reconfigure")
