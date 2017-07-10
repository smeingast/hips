# Licensed under a 3-clause BSD style license - see LICENSE.rst
from collections import OrderedDict
from io import StringIO
from csv import DictWriter
import urllib.request
from typing import List
from astropy.table import Table

__all__ = [
    'HipsSurveyProperties',
    'HipsSurveyPropertiesList',
]

__doctest_skip__ = [
    'HipsSurveyProperties',
    'HipsSurveyPropertiesList',
]


class HipsSurveyProperties:
    """HiPS properties container.

    Parameters
    ----------
    data : `~collections.OrderedDict`
        HiPS survey properties

    Examples
    --------
    >>> from hips import HipsSurveyProperties
    >>> url = 'http://alasky.unistra.fr/DSS/DSS2Merged/properties'
    >>> hips_survey_property = HipsSurveyProperties.fetch(url)
    >>> hips_survey_property.base_url
    'http://alasky.u-strasbg.fr/DSS/DSS2Merged'
    """
    hips_to_astropy_frame_mapping = OrderedDict([
        ('equatorial', 'icrs'),
        ('galactic', 'galactic'),
        ('ecliptic', 'ecliptic'),
    ])
    """HIPS to Astropy SkyCoord frame string mapping."""

    def __init__(self, data: OrderedDict) -> None:
        self.data = data

    @classmethod
    def read(cls, filename: str) -> 'HipsSurveyProperties':
        """Read from HiPS survey description file (`HipsSurveyProperties`).

        Parameters
        ----------
        filename : str
            HiPS properties filename
        """
        with open(filename) as fh:
            text = fh.read()

        return cls.parse(text)

    @classmethod
    def fetch(cls, url: str) -> 'HipsSurveyProperties':
        """Read from HiPS survey description file from remote URL (`HipsSurveyProperties`).

        Parameters
        ----------
        url : str
            URL containing HiPS properties
        """

        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
        return cls.parse(text)

    @classmethod
    def parse(cls, text: str) -> 'HipsSurveyProperties':
        """Parse HiPS survey description text (`HipsSurveyProperties`).

        Parameters
        ----------
        text : str
            Text containing HiPS survey properties
        """
        data = OrderedDict()
        for line in text.split('\n'):
            # Skip empty or comment lines
            if line == '' or line.startswith('#'):
                continue
            try:
                key, value = [_.strip() for _ in line.split('=')]
                data[key] = value
            except ValueError:
                # Skip bad lines (silently, might not be a good idea to do this)
                continue

        return cls(data)

    @property
    def title(self) -> str:
        """HiPS title (`str`)."""
        return self.data['obs_title']

    @property
    def hips_version(self) -> str:
        """HiPS version (`str`)."""
        return self.data['hips_version']

    @property
    def hips_frame(self) -> str:
        """HiPS coordinate frame (`str`)."""
        return self.data['hips_frame']

    @property
    def astropy_frame(self) -> str:
        """Astropy coordinate frame (`str`)."""
        return self.hips_to_astropy_frame_mapping[self.hips_frame]

    @property
    def hips_order(self) -> int:
        """HiPS order (`int`)."""
        return int(self.data['hips_order'])

    @property
    def tile_format(self) -> str:
        """HiPS tile format (`str`)."""
        return self.data['hips_tile_format']

    @property
    def base_url(self) -> str:
        """HiPS access url"""
        return self.data['moc_access_url'].rsplit('/', 1)[0]

    @property
    def tile_width(self) -> int:
        """HiPS tile width"""
        return int(self.data['hips_tile_width']) or 512

    def directory(self, ipix: int) -> int:
        """Directory index containing HiPS tile(s)"""
        return (ipix // 10000) * 10000

    def tile_access_url(self, order: int, ipix: int) -> str:
        """Tile access URL

        Parameters
        ----------
        order : int
            HiPS order
        ipix : int
            Index of the HiPS tile
        """
        return self.base_url + '/Norder' + str(order) + '/Dir' + str(self.directory(ipix)) + '/'

    @property
    def hips_service_url(self) -> str:
        """HiPS service base URL (`str`)."""
        return self.data['hips_service_url']


class HipsSurveyPropertiesList:
    """HiPS survey properties list.

    Parameters
    ----------
    data : List[HipsSurveyProperties]
        HiPS survey properties

    Examples
    --------
    Fetch the list of available HiPS surveys from CDS:

    >>> from hips import HipsSurveyPropertiesList
    >>> surveys = HipsSurveyPropertiesList.fetch()

    Look at the results:

    >>> len(surveys.data)
    335
    >>> survey = surveys.data[0]
    >>> survey.title
    '2MASS H (1.66 microns)'
    >>> survey.hips_order
    9

    You can make a `astropy.table.Table` of available HiPS surveys:

    >>> table = surveys.table

    and then do all the operations that Astropy table supports, e.g.

    >>> table[['ID', 'hips_order', 'hips_service_url']][[1, 30, 42]]
    >>> table.show_in_browser(jsviewer=True)
    >>> table.show_in_notebook()
    >>> table.to_pandas()

    """
    DEFAULT_URL = ('http://alasky.unistra.fr/MocServer/query?'
                   'hips_service_url=*&dataproduct_type=!catalog&dataproduct_type=!cube&get=record')
    """Default URL to fetch HiPS survey list from CDS."""

    def __init__(self, data: List[HipsSurveyProperties]) -> None:
        self.data = data

    @classmethod
    def read(cls, filename: str) -> 'HipsSurveyPropertiesList':
        """Read HiPS list from file (`HipsSurveyPropertiesList`).

        Parameters
        ----------
        filename : str
            HiPS list filename
        """
        with open(filename, encoding='utf-8', errors='ignore') as fh:
            text = fh.read()

        return cls.parse(text)

    @classmethod
    def fetch(cls, url: str = None) -> 'HipsSurveyPropertiesList':
        """Fetch HiPS list text from remote location (`HipsSurveyPropertiesList`).

        Parameters
        ----------
        url : str
            HiPS list URL
        """
        url = url or cls.DEFAULT_URL
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8', errors='ignore')
        return cls.parse(text)

    @classmethod
    def parse(cls, text: str) -> 'HipsSurveyPropertiesList':
        """Parse HiPS list text (`HipsSurveyPropertiesList`).

        Parameters
        ----------
        text : str
            HiPS list text
        """
        data = []
        for properties_text in text.split('\n\n'):
            properties = HipsSurveyProperties.parse(properties_text)
            data.append(properties)

        return cls(data)

    @property
    def table(self) -> Table:
        """Table with HiPS survey infos (`~astropy.table.Table`)."""
        # There are two aspects that make creating a `Table` from the data difficult:
        # 1. Not all fields are present for the different surveys
        # 2. All data is stored as strings, numbers haven't been converted yet
        #
        # It might not be the best solution, but the following code does the conversion
        # by going via an intermediate CVS string, which Table can parse directly
        rows = [properties.data for properties in self.data]
        fieldnames = sorted({key for row in rows for key in row})
        buffer = StringIO()
        writer = DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        return Table.read(buffer.getvalue(), format='ascii.csv', guess=False)
