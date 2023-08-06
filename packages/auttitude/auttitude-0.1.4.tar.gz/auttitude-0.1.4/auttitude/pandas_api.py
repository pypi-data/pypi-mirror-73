import pandas as pd

import auttitude as au


@pd.api.extensions.register_dataframe_accessor("autti")
class AuttitudeAccessor:
    def __init__(self, pandas_obj, direction_column=None, dip_column=None, strike=None):
        self._obj = pandas_obj
        self.direction_column = direction_column
        self.dip_column = dip_column
        self.strike = strike

    def translate(self, direction, dip, strike=False):
        return self._obj.apply(
            lambda row: au.translate_attitude(
                row[direction], row[dip], strike
            ),
            axis=1,
            result_type="expand",
        ).rename(columns={0: "direction", 1: "dip"})

