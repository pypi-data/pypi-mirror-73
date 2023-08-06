""" Test EVC name filters """


import unittest
from ...libs.models.evc import EthernetVirtualCircuit
from ...libs.core.evc_list import EvcsList
from ...libs.core.cli import CliOptions, create_parser

def create_cli():
    """ mock cli arguments """
    p = create_parser()
    a = p.parse_args(['-u', 'xpto', '-p', 'xpto', '-O', 'http://xpto', \
                       '-L', '-t', 'XPTO'])
    return CliOptions(parser=p, args=a)

class TestFilterUnis(unittest.TestCase):
    """  Test filters of EVC """

    def setUp(self):
        """ Set Up Testing environment. Creates three EVCs """
        self.evc_1 = EthernetVirtualCircuit()
        self.evc_1.name = "Vlan_4040_XPTO"

        self.evc_2 = EthernetVirtualCircuit()
        self.evc_2.name = "Vlan_4040_Foobar"

        self.evc_3 = EthernetVirtualCircuit()
        self.evc_3.name = "Vlan_4040"

        self.evc_4 = EthernetVirtualCircuit()
        self.evc_4.name = "Vlan_4040_XPTO"

        self.evcs = [self.evc_1, self.evc_2, self.evc_3, self.evc_4]

        self.evcs_list = EvcsList()

    def test_filter_evc_no_filter_provided_assert_true(self):
        """ If no filters are request by user, all UNIs are good.
         Expected number of EVCs: 4 """
        create_cli().has_evc_name = None
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 4)

    def test_filter_evc_exact_name(self):
        """ Search for evc_2's name """
        create_cli().has_evc_name = 'Vlan_4040_Foobar'
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Vlan_4040_Foobar")

    def test_filter_evc_same_name(self):
        """ Search for evc_1 and evc_4's name """
        create_cli().has_evc_name = 'Vlan_4040_XPTO'
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Vlan_4040_XPTO")
        self.assertEqual(result[1].name, "Vlan_4040_XPTO")

    def test_filter_evc_substring_name(self):
        """ Search for evc_3's name """
        create_cli().has_evc_name = 'Vlan_4040'
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Vlan_4040")

    def test_filter_evc_regex_name(self):
        """ Search for substring name, no EVC should be listed"""
        create_cli().has_evc_name = 'Vlan_4040_.*'
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 0)

    def test_filter_evc_unexisting_name(self):
        """ Search for unexisting name no EVC should be listed. """
        create_cli().has_evc_name = 'UnexistingName'
        result = self.evcs_list.filter(self.evcs)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
