from typing import List
from PIL import Image
from scipy.optimize import curve_fit
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tkinter.filedialog import asksaveasfilename
from unittest.mock import patch
import io
import logging

log = logging.getLogger(__name__)


class SpectrumUncurver:

    def __init__(self):
        self.spectrumImagePath = None
        self.curvaturePeakZoneX = None
        self.pixelList = None
        self.curvaturePeakZoneY = None
        self.imPIL = None
        self.imMAT = None
        self.imArray = None
        self.imPlot = None
        self.method = 'maximum'
        self.figure = plt.Figure()
        self.ax = self.figure.gca()
        self.canvas = FigureCanvas(self.figure)

        self.gaussianPeakPos = []
        self.maximumPeakPos = []
        self.gaussianPixelDeviationX = []
        self.fittedGaussianPixelDeviationX = []
        self.maximumPixelDeviationX = []

        self.shiftedImage = None
        self.shiftedPILImage = None
        self.fittedPILImage = None
        log.info("Class created successfully.")

    def save_image(self, imageFile:Image):
        generalErrorMessage = "File was not saved. "
        try:
            path = asksaveasfilename()
            imageFile.save(path)
        except ValueError as e:
            if str(e) == "unknown file extension:":
                log.error("unknown file extension." + generalErrorMessage)
            else:
                log.error(generalErrorMessage + str(e))

    def save_uncurved_image(self):
        generalErrorMessage = "File was not saved. "
        try:
            self.shiftedPILImage = Image.fromarray(self.shiftedImage)
            self.save_image(self.shiftedPILImage)
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute '__array_interface__'":
                log.error(
                    generalErrorMessage + "No Image to save. Please proceed with loading and uncurving of the spectral data.")
            else:
                log.error(generalErrorMessage + str(e))

    def save_image_with_fit(self):
        # TODO: make the superposition of the fit work
        pass
        # with patch('matplotlib.pyplot.show') as p:
        #     self.show_image_with_fit()
        #     self.canvas.draw()
        #     image = np.fromstring(self.canvas.tostring_rgb(), dtype='uint32').reshape((400, 1340, 3))
        #     self.fittedPILImage = Image.fromarray(image)
        #     self.save_image(self.fittedPILImage)

    def show_uncurved_image(self):
        self.shiftedPILImage = Image.fromarray(self.shiftedImage)
        self.shiftedPILImage.show()

    def show_image_with_fit(self):
        self.ax.imshow(self.imArray, cmap='gray')
        self.ax.scatter([self.gaussianPeakPos], [np.linspace(self.curvaturePeakZoneY[0], self.curvaturePeakZoneY[1], self.curvaturePeakZoneY[1]-self.curvaturePeakZoneY[0])], c='r', s=0.2, label="Gaussian fit")
        self.ax.scatter([self.maximumPeakPos], [np.linspace(self.curvaturePeakZoneY[0], self.curvaturePeakZoneY[1],
                                                         self.curvaturePeakZoneY[1] - self.curvaturePeakZoneY[0])],
                    c='b', s=0.2, label="Maximum fit")
        self.ax.legend()
        plt.show()

    def show_curved_image(self):
        self.imPIL.show()

    def show_curvature(self):
        fig, ax = plt.subplot()
        ax.plot(self.gaussianPeakPos)

    def load_image(self, imagePath: str):
        self.spectrumImagePath = imagePath
        self.imPIL = Image.open(self.spectrumImagePath)
        self.imArray = np.array(self.imPIL)
        self.imMAT = plt.imread(self.spectrumImagePath)
        self.imPlot = plt.imshow(self.imMAT)

    def uncurve_spectrum_image(self, xlim: List, ylim: List, method='maximum'):
        self.curvaturePeakZoneX = xlim
        self.curvaturePeakZoneY = ylim
        self.pixelList = np.linspace(self.curvaturePeakZoneX[0], self.curvaturePeakZoneX[1], len(self.curvaturePeakZoneX)+1)
        self.method = method

        self.find_peak_position_on_each_row()
        self.find_peak_deviations_on_each_row()
        if self.method == 'maximum':
            result = self.correct_maximum_deviation_on_each_row()
            return result
        elif self.method == 'gaussian':
            result = self.correct_gaussian_deviation_on_each_row()
            return result

    def find_peak_position_on_each_row(self):
        for ypos in range(self.curvaturePeakZoneY[0], self.curvaturePeakZoneY[1]):

            sectionyData = self.imArray[ypos][self.curvaturePeakZoneX[0]:self.curvaturePeakZoneX[1]+1]   # +1 because it doesn't include the given index
            sectionxData = np.linspace(self.curvaturePeakZoneX[0], self.curvaturePeakZoneX[1], len(sectionyData))
            log.debug("sectionxData:", sectionxData)
            pars, cov = curve_fit(f=self.gaussian, xdata=sectionxData, ydata=sectionyData,
                                  p0=[1, sectionxData[round(len(sectionxData)/2)], 1], bounds=(-np.inf, np.inf))
            stdevs = np.sqrt(np.diag(cov))
            maxIndex = sectionxData[np.argmax(sectionyData)]

            self.gaussianPeakPos.append(int(pars[1]))
            self.maximumPeakPos.append(int(maxIndex))

        log.info("GaussianPeakPos:{}".format(self.gaussianPeakPos))

    def find_peak_deviations_on_each_row(self):
        gaussianMidPosition = self.gaussianPeakPos[round(len(self.gaussianPeakPos) / 2)]
        maxMidPos = self.maximumPeakPos[round(len(self.maximumPeakPos) / 2)]
        log.info("gaussian peak avg position:{}".format(gaussianMidPosition))
        
        for ypos in range(self.curvaturePeakZoneY[1] - self.curvaturePeakZoneY[0]):
            xDevGaussian = self.gaussianPeakPos[ypos] - gaussianMidPosition
            self.gaussianPixelDeviationX.append(xDevGaussian)
            
            xDevMax = self.maximumPeakPos[ypos] - maxMidPos
            self.maximumPixelDeviationX.append(xDevMax)
        log.info("maximum peak average position:{}".format(self.maximumPixelDeviationX))

    def correct_maximum_deviation_on_each_row(self):
        self.shiftedImage = np.zeros(shape=(self.imPIL.height, self.imPIL.width))
        for ypos, i in enumerate(range(self.curvaturePeakZoneY[0], self.curvaturePeakZoneY[1])):
            corr = -self.maximumPixelDeviationX[i]
            log.debug(self.imArray[ypos][0:-corr])
            if corr >= 1:
                self.shiftedImage[ypos][corr:] = self.imArray[ypos][0:-corr]
            elif corr < 0:
                self.shiftedImage[ypos][0:corr-1] = self.imArray[ypos][-corr:-1]
            else:
                self.shiftedImage[ypos][::] = self.imArray[ypos][::]
        self.shiftedImage = self.shiftedImage/np.max(self.shiftedImage)
        self.shiftedPILImage = Image.fromarray(np.uint32(self.shiftedImage*63555))
        return self.shiftedImage

    def correct_gaussian_deviation_on_each_row(self):
        self.shiftedImage = np.zeros(shape=(self.imPIL.height, self.imPIL.width))
        for ypos, i in enumerate(range(self.curvaturePeakZoneY[0], self.curvaturePeakZoneY[1])):
            corr = -self.gaussianPixelDeviationX[i]
            log.debug(self.imArray[ypos][0:-corr])

            log.debug("YPOS:", ypos)
            log.debug("ARRAY", self.imArray[ypos])
            log.debug("DEV", corr)
            if corr >= 1:
                self.shiftedImage[ypos][corr:] = self.imArray[ypos][0:-corr]
            elif corr < 0:
                self.shiftedImage[ypos][0:corr-1] = self.imArray[ypos][-corr:-1]
            else:
                self.shiftedImage[ypos][::] = self.imArray[ypos][::]

        return self.shiftedImage

    def polyfit_peak_deviations(self):
        plt.plot(np.linspace(0,len(self.maximumPixelDeviationX), len(self.maximumPixelDeviationX)), self.maximumPixelDeviationX)

        x = np.linspace(0, len(self.maximumPixelDeviationX), len(self.maximumPixelDeviationX))
        y = self.maximumPixelDeviationX
        pars, cov = curve_fit(f=self.parabolic, xdata=x, ydata=y,
                              p0=[-1, 1, 1],
                              bounds=(-max(x), max(x)))
        stdevs = np.sqrt(np.diag(cov))

        devFity = self.parabolic(x, *pars)
        plt.plot(x, devFity, c='r')
        plt.show()

    @staticmethod
    def gaussian(x, a, b, c):
        return a * np.exp(-np.power(x - b, 2) / (2 * np.power(c, 2)))

    @staticmethod
    def parabolic(x, a, b, c):
        return a*x**2 + b*x + c


if __name__ == "__main__":
    corrector = SpectrumUncurver()
    corrector.load_image('./data/glycerol_06_06_2020_2.tif')
    corrector.uncurve_spectrum_image([640, 700], [0, 400], 'gaussian')
    corrector.save_image_with_fit()