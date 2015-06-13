import ldap
import ldap.filter


class LdapException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Ldap(object):
    """
    >>> l = Ldap(
    ...   {'bind_pw': 'plSRXrHRuN2b',
    ...    'uid_attr': 'sAMAccountName',
    ...    'base_dn': 'dc=yourhosting,dc=local',
    ...    'uri': 'ldap://192.168.0.7',
    ...    'bind_dn': r'yourhosting\\arjen.dijkstra'}) # raw_string!!
    >>> l.connect()
    >>> l.get_attribute('arjen.dijkstra', "mail")
    ['arjen.dijkstra@yourhosting.nl']
    >>> l.get_attribute('arjen.dijkstra', "notanattribute")
    []
    >>> l.get_attribute('arjen.dijkstra', 'givenName')
    ['Arjen']
    >>> l.get_attribute('mick.vandermostvansp', 'givenName')
    ['Mick']
    >>> l.get_attribute('mick.vandermostvansp','mail')
    ['mick.vandermostvanspijk@yourhosting.nl']
    >>> l.unbind()
    >>> l = Ldap({'bind_pw': 'password',
    ...           'uid_attr': 'sAMAccountName',
    ...           'base_dn': 'ou=somecompany,dc=somecompany,dc=com',
    ...           'uri': 'ldap://0.0.0.0:389',
    ...           'bind_dn': r'somecompany\\administrator'}) # raw_string!!!
    >>> try:
    ...     l.connect()
    ... except LdapException, e:
    ...     print("Exception: %r" % e)
    Exception: LdapException()
    """

    def __init__(self, cred):
        self.cred = cred

    def connect(self):
        """
        connect to ldap
        """
        try:
            self.l = ldap.initialize(self.cred['uri'])
            # self.l.start_tls_s()
            self.l.simple_bind_s(self.cred['bind_dn'], self.cred['bind_pw'])
        except Exception, e:
            raise LdapException(e)

    def get_attribute(self, user, attribute="mail", attrsonly=0):
        """Return a ldap person."""
        # user = "%s@yourhosting.local" % user
        search_filter = "(&(objectClass=Person)(%s=%s))" % (self.cred['uid_attr'],
                                                            ldap.filter.escape_filter_chars(user))
        person_attibute = self.l.search_s(self.cred['base_dn'], ldap.SCOPE_SUBTREE,
                                 search_filter,
                                 attrlist=[attribute],
                                 attrsonly=attrsonly)
        try:
            return person_attibute[0][1][attribute]
        except:
            return []

    def unbind(self):
        self.l.unbind_s()


if __name__ == "__main__":

    import cProfile
    # l = Ldap(
    #   {
    #     'bind_pw': "plSRXrHRuN2b",
    #    'uid_attr': 'sAMAccountName',
    #    'base_dn': 'dc=yourhosting,dc=local',
    #    'uri': 'ldap://192.168.0.7',
    #    # 'bind_dn': r'CN=ad access,OU=Gebruikers,DC=yourhosting,DC=local'}) # raw_string!!
    #    'bind_dn': 'yourhosting\\arjen.dijkstra'}) # raw_string!!
    # l.connect()

    # cProfile.run("l.get_attribute('arjen.dijkstra', 'mail')")
    # print(l.get_attribute('arjen.dijkstra', 'mail'))
    import doctest
    doctest.testmod()
