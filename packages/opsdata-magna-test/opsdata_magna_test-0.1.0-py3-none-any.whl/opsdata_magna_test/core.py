"""
ObsPlus instructions for downloading dataset.
"""
from functools import lru_cache
from pathlib import Path

import obsplus
import obspy
from opsdata_magna_test import __version__

starttime = obspy.UTCDateTime("2020-03-18T13:09:30")
endtime = starttime + 600

channel_list = [
    ("UU", "NOQ", "*", "HH?",),
    ("UU", "SAIU", "*", "EN?",),
    ("UU", "FTT", "*", "EN?",),
    ("UU", "ICF", "*", "EN?",),
    ("UU", "LKC", "*", "EN?",),
]

bulk = [list(x) + [starttime, endtime] for x in channel_list]


class SLC2020Small(obsplus.DataSet):
    """
    ObsPlus dataset of the 2020 Salt Lake City earthquake including only a
    few stations and small amounts of continuous data. This dataset may not
    be research quality and is only intended for testing.

    """

    name = "magna_test"
    base_path = Path(__file__).parent
    version = __version__

    @property
    @lru_cache()
    def client(self):
        """Init an IRIS FDSN client."""
        from obspy.clients.fdsn import Client

        return Client("IRIS")

    # --- functions used to specify how data are downloaded

    def download_events(self):
        """ download event data and store them in self.event_path """
        Path(self.event_path).mkdir(exist_ok=True, parents=True)

    def download_waveforms(self):
        """ download waveform data and store them in self.waveform_path """
        bank = obsplus.WaveBank(self.waveform_path)
        st = self.client.get_waveforms_bulk(bulk)
        bank.put_waveforms(st)

    def download_stations(self):
        """ download station data and store them in self.station_path """
        inv = self.client.get_stations_bulk(bulk=bulk, level="response")
        path = Path(self.station_path) / "inventory.xml"
        path.parent.mkdir(exist_ok=True, parents=True)
        inv.write(str(path), "stationxml")

    # --- properties to specify when data need to be downloaded

    # @property
    # def waveforms_need_downloading(self):
    #     """ Return True if the waveforms should be downloaded """

    # @property
    # def stations_need_downloading(self):
    #     """ Return True if the stations should be downloaded """
    # @property
    # def events_need_downloading(self):
    #     """ Return True if the events should be downloaded """

    # --- functions to return clients

    # @property
    # @lru_cache()
    # def waveform_client(self) -> Optional[WaveBank]:
    #     """ A cached property for a waveform client """

    # @property
    # @lru_cache()
    # def event_client(self) -> Optional[EventBank]:
    #     """ A cached property for an event client """

    # @property
    # @lru_cache()
    # def station_client(self) -> Optional[obspy.Inventory]:
    #     """ A cached property for a station client """

    # --- post download hook

    # def pre_download_hook(self):
    #     """ This code gets run before downloading any data. """

    def post_download(self):
        """ This code get run after downloading all data types. """
        # by default create a file with hash values for each. This will issue
        # a warning if any of the downloaded files change in the future.
        self.create_sha256_hash()
