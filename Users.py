import ldap
import ldap.filter


class LdapException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Ldap(object):
    """
    >>> l = Ldap({'bind_pw': 'noaCces6',
    ...           'uid_attr': 'uid',
    ...           'base_dn': 'ou=somecompany,dc=somecompany,dc=com',
    ...           'uri': 'ldap://localhost:389',
    ...           'bind_dn': r'cn=administrator,dc=somecompany,dc=com'}) # raw_string!!!
    >>> l.connect()
    >>> l.get_attribute('mee', "mail")
    'arjen.dijkstra@somecompany.nl'
    >>> l.get_attribute('mee', "notanattribute")
    []
    >>> l.get_attribute('mee', 'l')  # weird attribute name in LDAP
    'Groningen'
    >>> l.get_attribute('mee', 'givenName')
    'Arjen'
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
            self.l.simple_bind_s(self.cred['bind_dn'], self.cred['bind_pw'])
        except Exception, e:
            raise LdapException(e)

    def get_attribute(self, user, attribute):
        """
        get attribute for a user
        """
        person = self.l.search_s(self.cred['base_dn'],
                          ldap.SCOPE_SUBTREE,
                          "%s=%s" % (self.cred['uid_attr'],
                              ldap.filter.escape_filter_chars(user)))
        if person:
            info = person[0][1]
        else:
            return []

        try:
            result = info[attribute][0]
        except KeyError:
            return []
        return result

    def unbind(self):
        self.l.unbind_s()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
