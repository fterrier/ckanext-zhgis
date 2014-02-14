import ckan.lib.cli
import sys
from pprint import pprint

from ckanext.zhgis.helpers import s3
from ckanext.zhgis.helpers import ckan_csw


class ZhGisCommand(ckan.lib.cli.CkanCommand):
    '''Command to handle zhgis data

    Usage:

        # General usage
        paster --plugin=ckanext-zhgis <command> -c <path to config file>

        # Show this help
        paster zhgis help

        # Import datasets
        paster zhgis import

        # List all files in the S3 bucket
        paster zhgis list

        # Show output from CSW, 'query' is typically
        # the name of a dataset like 'swissboundaries3D'
        paster zhgis csw <query>

        # Show output from CSW, 'query' is must be the id
        # of a dataset like '38d5c3c9-ff3f-447a-b11d-aa80472246b6'
        paster zhgis cswid <query>

    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        # load pylons config
        self._load_config()
        options = {
            'import': self.importCmd,
            'list': self.listCmd,
            'csw': self.cswCmd,
            'cswid': self.cswIdCmd,
            'help': self.helpCmd,
        }

        try:
            cmd = self.args[0]
            options[cmd](*self.args[1:])
        except KeyError:
            self.helpCmd()
            sys.exit(1)

    def helpCmd(self):
        print self.__doc__

    def listCmd(self):
        s3_helper = s3.S3()
        for file in s3_helper.list():
            print file

    def cswCmd(self, query=None, lang='de'):
        if (query is None):
            print "Argument 'query' must be set"
            self.helpCmd()
            sys.exit(1)
        csw = ckan_csw.ZhGisCkanMetadata()
        metadata = csw.get_ckan_metadata(query, lang)
        del metadata['metadata_raw']
        pprint(metadata)

    def cswIdCmd(self, query=None, lang='de'):
        if (query is None):
            print "Argument 'query' must be set"
            self.helpCmd()
            sys.exit(1)
        csw = ckan_csw.ZhGisCkanMetadata()
        metadata = csw.get_ckan_metadata_by_id(query, lang)
        del metadata['metadata_raw']
        pprint(metadata)

    def importCmd(self):
        raise NotImplementedError

    def showCmd(self):
        raise NotImplementedError
