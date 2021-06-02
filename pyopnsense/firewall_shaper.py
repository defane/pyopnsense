from pyopnsense import client


class FirewallShaperClient(client.OPNClient):
    def search_rules(self, searchPhrase=None, current=1, rowCount=100):
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
        return self._post('trafficshaper/settings/searchRules', body=body)

    def _save_rule(
            self, endpoint, sequence, interface, source, destination, target, proto=None, enabled=None,
            interface2=None,iplen=None, src_port=None, dst_port=None, direction=None, dscp=None, description=None
        ):
        # Default value
        if enabled is None:
            enabled = str("1")
        if interface2 is None:
            interface2 = str("")
        if proto is None:
            proto = str("ip")
        if iplen is None:
            iplen = str("")
        if src_port is None:
            src_port = str("any")
        if dst_port is None:
            dst_port = str("any")
        if dscp is None:
            dscp = str("")
        if direction is None:
            direction = str("")
        if description is None:
            description = str("")

        
        if source["not"]:
            source_not=str("1")
        else:
            source_not=str("0")
        source_content = ",".join(source["content"])

        if destination["not"]:
            destination_not = str("1")
        else:
            destination_not = str("0")
        destination_content = ",".join(destination["content"])

        rule = dict(
            enabled=enabled,
            sequence=sequence,
            interface=interface,
            interface2=interface2,
            proto=proto,
            iplen=iplen,
            source=source_content,
            source_not=source_not,
            src_port=src_port,
            destination=destination_content,
            destination_not=destination_not,
            dst_port=dst_port,
            dscp=dscp,
            direction=direction,
            target=target,
            description=description
        )
        
        body = dict(rule=rule)

        return self._post(endpoint, json=body)

    def set_rule(
            self, uuid, sequence, interface, source, destination, target, proto=None, enabled=None,
            interface2=None,iplen=None, src_port=None, dst_port=None, direction=None, dscp=None, description=None
        ):
        """Update a Traffi Shaper rule
        """

        endpoint = "{}/{}".format("trafficshaper/settings/setRule", uuid)

        return self._save_rule(
            endpoint, sequence, interface, source, destination, target, proto, enabled,
            interface2, iplen, src_port, dst_port, direction, dscp, description
        )

    def add_rule(
            self, sequence, interface, source, destination, target, proto=None, enabled=None,
            interface2=None, iplen=None, src_port=None, dst_port=None, direction=None, dscp=None, description=None
        ):
        """Create a Traffic Shaper rule
        """

        endpoint = "trafficshaper/settings/addRule/"

        return self._save_rule(
            endpoint, sequence, interface, source, destination, target, proto, enabled,
            interface2, iplen, src_port, dst_port, direction, dscp, description
        )

    def delete_rule(self, uuid):
        """Delete rule with given identifier.

        :param string uuid: rule identifier.
        """

        endpoint = "{}/{}".format("trafficshaper/settings/delRule", uuid)

        return self._post(endpoint, json=dict())

    def get_rule(self, uuid=None):
        """Get rule with given identifier.

        :param string id: rule identifier.
        """
        if uuid is None:
            uuid = str()

        endpoint = "{}/{}".format("trafficshaper/settings/getRule", uuid)

        return self._get(endpoint)

    def reconfigure(self):
        """Apply Traffic Shaper rule.
        """

        endpoint = "trafficshaper/service/reconfigure"

        return self._post(endpoint, json=dict())
