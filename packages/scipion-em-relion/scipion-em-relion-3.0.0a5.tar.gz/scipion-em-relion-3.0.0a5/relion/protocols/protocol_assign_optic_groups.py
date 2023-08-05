# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *
# * [1] SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
import os

import pwem
import pyworkflow.protocol.params as params

from relion.convert.convert31 import OpticsGroups
from .protocol_base import ProtRelionBase


class ProtRelionAssignOpticsGroup(ProtRelionBase):
    """ Assign Optics Group name and related parameters to an input set.
     Input set can be: movies, micrographs or particles.
    """
    _label = 'assign optics group'
    
    # --------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')
        form.addParam('inputSet', params.PointerParam,
                      pointerClass='SetOfMovies,SetOfMicrographs,SetOfParticles',
                      label="Input set", important=True,
                      help='Select the input set (Movies, Micrographs or '
                           'Particles) to assign Optics Group parameters.')

        form.addParam('opticsGroupName', params.StringParam,
                      default='opticsGroup1',
                      label='Optics group name',
                      help='Relion-specific option. Name of this optics group. '
                           'Each group of movies with different '
                           'optics characteristics for CTF refinement '
                           'should have a unique name.')

        form.addParam('mtfFile', params.FileParam, allowsNull=True,
                      label='MTF-curve file',
                      help='User-provided STAR-file with the MTF-curve '
                           'of the detector. Use the wizard to load one '
                           'of the predefined ones provided at:\n'
                           '- [[https://www3.mrc-lmb.cam.ac.uk/relion/index.php/'
                           'FAQs#Where_can_I_find_MTF_curves_for_typical_detectors.3F]'
                           '[Relion\'s Wiki FAQs]]\n'
                           ' - [[https://www.gatan.com/techniques/cryo-em#MTF][Gatan\'s website]]\n\n'
                           'Relion param: *--mtf*')

        line = form.addLine('Beam tilt (mrad)',
                            help='Known beam tilt in the X/Y-direction (in mrad). '
                                 'Set to zero if unknown.')
        line.addParam('beamTiltX', params.FloatParam, default=0.,
                      label='X')
        line.addParam('beamTiltY', params.FloatParam, default=0.,
                      label='Y')

        form.addParam('defectFile', params.FileParam, allowsNull=True,
                      label='Defects file',
                      help='Location of a UCSF MotionCor2-style '
                      'defect text file or a defect map that '
                      'describe the defect pixels on the detector. '
                      'Each line of a defect text file should contain '
                      'four numbers specifying x, y, width and height '
                      'of a defect region. A defect map is an image '
                      '(MRC or TIFF), where 0 means good and 1 means '
                      'bad pixels. The coordinate system is the same '
                      'as the input movie before application of '
                      'binning, rotation and/or flipping.\n\n'
                      '_Note that the format of the defect text is '
                      'DIFFERENT from the defect text produced '
                      'by SerialEM!_\n One can convert a SerialEM-style '
                      'defect file into a defect map using IMOD '
                      'utilities e.g.:\n'
                      '*clip defect -D defect.txt -f tif movie.tif defect_map.tif*\n'
                      'See explanations in the SerialEM manual.\n'
                      'Leave empty if you do not have any defects, '
                      'or do not want to correct for defects on your detector.')

    # --------------------------- INSERT steps functions ----------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('createOutputStep',
                                 self.inputSet.get().getObjId())

    # --------------------------- STEPS functions -----------------------------
    def createOutputStep(self, inputId):
        inputSet = self.inputSet.get()
        
        if isinstance(inputSet, pwem.objects.SetOfMovies):
            outputSet = self._createSetOfMovies()
            outputName = 'outputMovies'
        elif isinstance(inputSet, pwem.objects.SetOfMicrographs):
            outputSet = self._createSetOfMicrographs()
            outputName = 'outputMicrographs'
        elif isinstance(inputSet, pwem.objects.SetOfParticles):
            outputSet = self._createSetOfParticles()
            outputName = 'outputParticles'
        else:
            raise Exception("Invalid input of type %s, expecting:\n"
                            "SetOfMovies, SetOfMicrographs or SetOfParticles"
                            % inputSet.getClassName())

        # Copy general info from input set
        outputSet.copyInfo(inputSet)
        # Update the acquisition object with new parameters from input
        acq = inputSet.getAcquisition()
        outputSet.copyItems(inputSet)

        og = OpticsGroups.create(
            rlnVoltage=acq.getVoltage(),
            rlnSphericalAberration=acq.getSphericalAberration(),
            rlnAmplitudeContrast=acq.getAmplitudeContrast(),
            rlnImagePixelSize=inputSet.getSamplingRate(),
            rlnImageSize=inputSet.getXDim(),
            rlnOpticsGroupName=self.opticsGroupName.get(),
            rlnMtfFileName=self.mtfFile.get(),
            rlnBeamTiltX=self.beamTiltX.get(),
            rlnBeamTiltY=self.beamTiltY.get(),
            rlnMicrographDefectFile=self.defectFile.get()  # looks not used by relion 3.1
        )
        og.toImages(outputSet)

        self._defineOutputs(**{outputName: outputSet})
        self._defineTransformRelation(inputSet, outputSet)
    
    # --------------------------- INFO functions ------------------------------
    def _validate(self):
        validateMsgs = []

        defectFile = self.defectFile.get()
        if defectFile is not None and not os.path.exists(defectFile):
            validateMsgs.append("Defect file not found:\n%s" % self.defectFile.get())
        if self.mtfFile.hasValue() and not os.path.exists(self.mtfFile.get()):
            validateMsgs.append("MTF file not found:\n%s" % self.mtfFile.get())

        return validateMsgs
    
    def _summary(self):
        summary = []
        return summary
    
    def _methods(self):
        return []
