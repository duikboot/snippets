#/usr/bin/python

import tidylib
import os
import cgi
import re


class Validator(object):
    """
    Validates a template according to configs
    """
    logger = None
    logger_mail = None

    def __init__(self, config={}, ignore={}, escape=True):
        """
        Validator. Takes a tidy-configfile and strings to ignore
        """
        self.config = config
        self.ignore = ignore
        self.flush()
        self.escape = escape

    def flush(self):
        self._errors = []
        self._warnings = []
        self._accessibility = []
        self.document = ''

    def _parse_line(self, line):
        """
        expected line format:
        '[line] X [column] Y - [type]: [message]'

        parse the output of tidylib
        'line 1 column 1 - Warning: missing <!DOCTYPE> declaration'

        >>> #from informaat.daemons.htmlvalidation.Validate import Validator
        >>> from Validate import Validator
        >>> v = Validator(escape=False)
        >>> v._parse_line('line 1 column 1 - Warning: missing <!DOCTYPE>')
        [1, 1, 'Warning', 'missing <!DOCTYPE>']
        >>> v = Validator(escape=True)
        >>> v._parse_line('line 1 column 1 - Warning: missing <!DOCTYPE>')
        [1, 1, 'Warning', 'missing &lt;!DOCTYPE&gt;']
        """

        if self.escape:
            line = cgi.escape(line)  # pfoei, remembered escape in cgi :-)
            line = line.replace('\n', '')
            line = line.replace('\t', '')

        if not line:
            return None
        index_of_dash = line.find('-')
        if index_of_dash < 0:
            return None
        if 'Accessibility Checks' in line:
            return None
        numberpart = line[:index_of_dash]
        messagepart = line[index_of_dash + 1:]

        numberpart = numberpart.replace('line', '')
        numberpart = numberpart.replace('column', '')
        if numberpart:
            try:
                lineno, column = numberpart.split()
                type_, message = messagepart.split(':', 1)
                l = [int(lineno), int(column), type_.strip(), message.strip()]
                return l
            except:
                return None

    def read_template(self, template, file_=False):
        """
        Read and validate the html template, explicitly specify if you want a
        file to be validated, because you can have to html as a string be
        validated too. Default file_ is set to false"""
        # self.template = template
        if self.logger:
            self.logger.info("template: %s" % template)
        # if os.path.isfile(template):
        #     self.template = open(self.template).read()
        if file_:
            if os.path.exists(template):
                template = open(template).read()
            else:
                return "error"

        self.output = ''

        parse = tidylib.tidy_document(template, self.config)
        self.document, output = parse[0], parse[1]
        if 'Warning:' in output or 'Error:' in output or 'Access:' in output:
            self.output = output.split('\n')
        if self.output:
            self._parse_output()

    def _parse_output(self):
        """
        parse the output from tidy and put it in
        lists(self._errors, self._warnings, self._accessibility)
        """

        def ignorestring(line, ignorelist):
            """Is the string in the list to ignore?"""
            for item in ignorelist:
                if item.startswith("re:"):
                    regex = item.replace('re:', '')
                    regex = re.findall(regex, line[3])
                    if regex:
                        return True
                if item in line[3]:
                    return True

        tempListTemplates = []
        if self.output:
            for l in self.output:
                line = self._parse_line(l)
                tempListTemplates.append(line)
        tempListTemplates.sort()

        if tempListTemplates:
            for line in tempListTemplates:
                if line:
                    if 'Error' in line:
                        if 'errors' in self.ignore:
                            if ignorestring(line, self.ignore['errors']):
                                continue
                        self._errors.append(line)

                    elif 'Warning' in line:
                        if 'warnings' in self.ignore:
                            if ignorestring(line, self.ignore['warnings']):
                                continue
                        self._warnings.append(line)

                    elif 'Access' in line:
                        if 'accessibility' in self.ignore:
                            if ignorestring(line,
                                            self.ignore['accessibility']):
                                continue
                        self._accessibility.append(line)

    @property
    def errors(self):
        return sorted(self._errors)

    @property
    def warnings(self):
        return sorted(self._warnings)

    @property
    def accessibility(self):
        return sorted(self._accessibility)

    def get_document(self):
        """return the tidied document"""
        return self.document


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    def parse_config_file(c_file):
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.readfp(open(c_file))
        d = {}
        for section in config.sections():
            d.update(dict(config.items(section)))
        return d

    try:
        config = parse_config_file('tidyconf.conf')
    except:
        config = dict(show_errors='999999', doctype="auto", force_output=1)
    print(config)
    template = "tests/testtemplates/DE-setEffectiveDate.html"
    ignore = {'accessibility':
                ['[2.1.1.4]',
                '[2.1.1.5]',
                '[6.2.2.2]',
                '[6.3.1.1]',
                '[7.1.1.1]',
                '[8.1.1.1]',
                'no-such-tag'],
               'warnings':
                [
                 're:attribute.*?#{'
                ]}
    validator = Validator(config, ignore)
    validator.read_template(template)
    errors = validator.errors
    warnings = validator.warnings
    accessibility = validator.accessibility
    #import mail_user
    #mail_user.mail_validation("arjen.dijkstra@informaat.nl",
            #errors + warnings + accessibility)
    print("Errors: %r" % errors)
    print("Warnings: %r" % warnings)
    print("Accessibility: %r" % accessibility)
    if not validator._errors and not validator._warnings:
        print("NO ERRORS")
        f = open('test.html', 'w').write(validator.get_document())
