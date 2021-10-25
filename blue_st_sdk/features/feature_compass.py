
from blue_st_sdk.feature import Feature
from blue_st_sdk.feature import Sample
from blue_st_sdk.feature import ExtractedData
from blue_st_sdk.features.field import Field
from blue_st_sdk.features.field import FieldType
from blue_st_sdk.utils.number_conversion import LittleEndian
from blue_st_sdk.utils.blue_st_exceptions import BlueSTInvalidOperationException
from blue_st_sdk.utils.blue_st_exceptions import BlueSTInvalidDataException


# CLASSES

class FeatureCompass(Feature):
    """The feature handles the data coming from a compass.

    Data is one bytes long and has one decimal digit.
    """

    FEATURE_NAME = "Compass"
    FEATURE_UNIT = "°"
    FEATURE_DATA_NAME = "Angle"
    DATA_MAX = 360.0
    DATA_MIN = 0.0
    FEATURE_FIELDS = Field(
        FEATURE_DATA_NAME,
        FEATURE_UNIT,
        FieldType.Float,
        DATA_MAX,
        DATA_MIN)
    DATA_LENGTH_BYTES = 2
    SCALE_FACTOR = 100.0

    def __init__(self, node):
        """Constructor.

        Args:
            node (:class:`blue_st_sdk.node.Node`): Node that will send data to
                this feature.
        """
        super(FeatureCompass, self).__init__(
            self.FEATURE_NAME, node, [self.FEATURE_FIELDS])

    def extract_data(self, timestamp, data, offset):
        """Extract the data from the feature's raw data.
        
        Args:
            timestamp (int): Data's timestamp.
            data (str): The data read from the feature.
            offset (int): Offset where to start reading data.
        
        Returns:
            :class:`blue_st_sdk.feature.ExtractedData`: Container of the number
            of bytes read and the extracted data.

        Raises:
            :exc:`blue_st_sdk.utils.blue_st_exceptions.BlueSTInvalidDataException`
                if the data array has not enough data to read.
        """
        if len(data) - offset < self.DATA_LENGTH_BYTES:
            raise BlueSTInvalidDataException(
                'There are no %d bytes available to read.' \
                % (self.DATA_LENGTH_BYTES))

        sample = Sample(
            [LittleEndian.bytes_to_int16(data, offset) / self.SCALE_FACTOR],
            self.get_fields_description(),
            timestamp)
        return ExtractedData(sample, self.DATA_LENGTH_BYTES)

    @classmethod
    def get_compass(self, sample):
        """Get the Compass value from a sample.

        Args:
            sample (:class:`blue_st_sdk.feature.Sample`): Sample data.
        
        Returns:
            float: The compass value if the data array is valid, <nan>
            otherwise.
        """
        if sample is not None:
            if sample._data:
                if sample._data[0] is not None:
                    return float(sample._data[0])
        return float('nan')

    def read_compass(self):
        """Read the compass value.

        Returns:
            float: The compass value if the read operation is successful, <nan>
            otherwise.

        Raises:
            :exc:`blue_st_sdk.utils.blue_st_exceptions.BlueSTInvalidOperationException`
                is raised if the feature is not enabled or the operation
                required is not supported.
            :exc:`blue_st_sdk.utils.blue_st_exceptions.BlueSTInvalidDataException`
                if the data array has not enough data to read.
        """
        try:
            self._read_data()
            return FeatureCompass.get_compass(self._get_sample())
        except (BlueSTInvalidOperationException, BlueSTInvalidDataException) as e:
            raise e
