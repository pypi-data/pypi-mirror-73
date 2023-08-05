import logging

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


class RotationAnglePlotter:
    def __init__(self, feature):
        """

        """
        self.fig, self.ax = plt.subplots(2, 2, figsize=(15, 15))
        self.ax[0][0].set_ylim(-90, 90)
        self.ax[1][0].set_ylim(-90, 90)
        self.feature = feature
    def plot(self, x, y, ix, iy, symb):
        """

        Parameters
        ----------
        x : np.array
            vector of x
        y
        ix
        iy
        symb

        Returns
        -------

        """
        self.ax[iy][ix].plot(x, y, symb)

    def add_fold_limb_data(self, symb="bo",**kwargs):
        fold_frame = self.feature.fold.fold_limb_rotation.fold_frame_coordinate
        rotation = self.feature.fold.fold_limb_rotation.rotation_angle
        self.plot(fold_frame, rotation, 0, 1, symb,**kwargs)

    def add_fold_limb_curve(self, symb='r-',**kwargs):
        x = np.linspace(self.feature.fold.foldframe[0].min(),self.feature.fold.foldframe[0].max(),100)
        self.plot(x,self.feature.fold.fold_limb_rotation(x), 0, 1, symb,**kwargs)

    def add_axis_svariogram(self, symb='bo',**kwargs):
        svariogram = self.feature.fold.fold_axis_rotation.svario
        if svariogram:
            svariogram.calc_semivariogram()
            self.plot(svariogram.lags, svariogram.variogram, 1, 1, symb,**kwargs)

    def add_limb_svariogram(self, symb='bo', **kwargs):
        svariogram = self.feature.fold.fold_limb_rotation.svario
        if svariogram:
            svariogram.calc_semivariogram()
            self.plot(svariogram.lags, svariogram.variogram, 1, 1, symb,**kwargs)

    def add_fold_axis_data(self, symb='bo',**kwargs):
        fold_frame = self.feature.fold.fold_axis_rotation.fold_frame_coordinate
        rotation = self.feature.fold.fold_axis_rotation.rotation_angle
        self.plot(fold_frame, rotation, 0, 1, symb,**kwargs)

    def add_fold_axis_curve(self, symb='r-',**kwargs):
        x = np.linspace(self.feature.fold.foldframe[1].min(),self.feature.fold.foldframe[1].max(),100)
        self.plot(x,self.feature.fold.fold_axis_rotation(x), 0, 1, symb,**kwargs)


