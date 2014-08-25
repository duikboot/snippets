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
    ...   {'bind_pw': 'L8xMikxTw4x4DHx6gCKv',
    ...    'uid_attr': 'userPrincipalName',
    ...    'base_dn': 'dc=yourhosting,dc=local',
    ...    'uri': 'ldap://192.168.0.7',
    ...    'bind_dn': r'CN=ad access,OU=Gebruikers,DC=yourhosting,DC=local'}) # raw_string!!
    >>> l.connect()
    >>> l.get_attribute('arjen.dijkstra', "mail")
    'arjen.dijkstra@yourhosting.nl'
    >>> l.get_attribute('arjen.dijkstra', "notanattribute")
    []
    >>> l.get_attribute('arjen.dijkstra', 'givenName')
    'Arjen'
    >>> l.get_attribute('mick.vandermostvanspijk', 'givenName')
    'Mick'
    >>> l.get_attribute('mick.vandermostvanspijk','mail')
    'mick.vandermostvanspijk@yourhosting.nl'
    >>> l._person('ireallydontexist')
    ''
    >>> sorted(l.get_attributes('arjen.dijkstra')) # doctest: +ELLIPSIS
    ['accountExpires', 'badPasswordTime', 'badPwdCount', 'cn', 'codePage', ...]
    >>> l.unbind()
    >>> l = Ldap({'bind_pw': 'password',
    ...           'uid_attr': 'sAMAccountName',
    ...           'base_dn': 'ou=somecompany,dc=somecompany,dc=com',
    ...           'uri': 'ldap://0.0.0.0:389',
    ...           'bind_dn': r'somecompany\\administrator'}) # raw_string!!!
    >>> try:
    ...     l.connect()
    ... except LdapException, e:
    ...     print "Exception: %r" % e
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

    def get_attribute(self, user, attribute, attrsonly=0):
        """Return a ldap person."""
        # user = "%s@yourhosting.local" % user
        search_filter = "(&(objectClass=Person)(%s=%s))" % (self.cred['uid_attr'],
                                                            ldap.filter.escape_filter_chars(user))
        person_attibute = self.l.search_s(self.cred['base_dn'], ldap.SCOPE_SUBTREE,
                                 search_filter,
                                 attrlist=[attribute],
                                 attrsonly=attrsonly)
        return person_attibute

    def get_attributes(self, user):
        """Get all attributes of a user."""
        person = self.get_attribute(user, attrsonly=1)
        return person[0][1].keys()

    def unbind(self):
        self.l.unbind_s()


if __name__ == "__main__":

    import cProfile
    l = Ldap(
      {
          # 'bind_pw': 'L8xMikxTw4x4DHx6gCKv',
        'bind_pw': "plSRXrHRuN2b",
       'uid_attr': 'sAMAccountName',
       'base_dn': 'dc=yourhosting,dc=local',
       'uri': 'ldap://192.168.0.7',
       # 'bind_dn': r'CN=ad access,OU=Gebruikers,DC=yourhosting,DC=local'}) # raw_string!!
       'bind_dn': 'yourhosting\\arjen.dijkstra'}) # raw_string!!
    l.connect()
    
    cProfile.run("l.get_attribute('arjen.dijkstra', 'mail')")
    cProfile.run("l.get_attributes('arjen.dijkstra', 'mail')")
