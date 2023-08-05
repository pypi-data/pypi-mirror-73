"""
Matrix class
"""
import numpy as np
import pandas as pd
import flowutils
from ..._utils import utils


class Matrix(object):
    """
    Represents a single compensation matrix from a CSV/TSV file, NumPy array or Pandas
    DataFrame.

    :param matrix_id: Text string used to identify the matrix (cannot be 'uncompensated' or 'fcs')
    :param spill_data_or_file: matrix data array, can be either:
            - a file path or file handle to a CSV/TSF file
            - a pathlib Path object to a CSV/TSF file
            - a NumPy array of spill data
            - a Pandas DataFrame (channel labels as headers)
    :param detectors: A list of strings or a list of tuples to use for the detector
        labels.
    :param fluorochromes: A list of strings or a list of tuples to use for the detector
        labels.
    :param null_channels: List of PnN labels for channels that were collected
        but do not contain useful data. Note, this should only be used if there were
        truly no fluorochromes used targeting those detectors and the channels
        do not contribute to compensation.
    """
    def __init__(
            self,
            matrix_id,
            spill_data_or_file,
            detectors,
            fluorochromes=None,
            null_channels=None
    ):
        if matrix_id == 'uncompensated' or matrix_id == 'fcs':
            raise ValueError(
                "Matrix IDs 'uncompensated' and 'fcs' are reserved compensation references " +
                "used in Dimension instances to specify that channel data should either be " +
                "uncompensated or compensated using the spill value from a Sample's metadata"
            )

        if isinstance(spill_data_or_file, np.ndarray):
            spill = spill_data_or_file
        else:
            spill = utils.parse_compensation_matrix(
                spill_data_or_file,
                detectors,
                null_channels=null_channels
            )
            spill = spill[1:, :]

        self.id = matrix_id
        self.matrix = spill
        # TODO: Should we use a different name other than 'fluorochromes'? They are typically antibodies or markers.
        self.detectors = detectors
        # Note: fluorochromes attribute is required for compatibility with GatingML exports,
        #       as the GatingML 2.0 requires both the set of detectors and fluorochromes.
        if fluorochromes is None:
            fluorochromes = ['' for _ in detectors]

        self.fluorochomes = fluorochromes

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.id}, dims: {len(self.detectors)})'
        )

    def apply(self, sample):
        """
        Apply compensation matrix to given Sample instance.
        :param sample: Sample instance with matching set of detectors
        :return: NumPy array of compensated events
        """
        indices = [
            sample.get_channel_index(d) for d in self.detectors
        ]
        events = sample.get_raw_events()
        events = events.copy()

        return flowutils.compensate.compensate(
            events,
            self.matrix,
            indices
        )

    def as_dataframe(self, fluoro_labels=False):
        """
        Returns the compensation matrix as a Pandas DataFrame.

        :param fluoro_labels: If True, the fluorochrome names are used as the column headers & row indices, else
            the detector names are used (default).
        :return: Pandas DataFrame
        """
        if fluoro_labels:
            labels = self.fluorochomes
        else:
            labels = self.detectors

        return pd.DataFrame(self.matrix, columns=labels, index=labels)
