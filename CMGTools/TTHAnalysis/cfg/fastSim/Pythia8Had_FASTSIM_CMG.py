#### FASTSIM + CMG in one go
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_2012_Summer_inTimeOnly_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('HLTrigger.Configuration.HLT_7E33v2_Famos_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/g/gpetrucc/public/DYLL_trivial.lhe')
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(),
        parameterSets = cms.vstring('pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
        )
    )
)

# Output definition
#process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
#    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
#    outputCommands = process.AODSIMEventContent.outputCommands,
#    fileName = cms.untracked.string('aodsim.root'),
#    dataset = cms.untracked.PSet(
#        filterName = cms.untracked.string(''),
#        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
#    ),
#)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.generator+process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')

# Path and EndPath definitions
process.generation_step = cms.Path(process.generator+process.pgen_genonly)
process.reconstruction = cms.Path(process.generator+process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
#process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
#process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])
process.schedule.extend([process.reconstruction])

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

###=================================================================================================================
###========  PREPARE FOR SUBPROCESS  ===============================================================================
###=================================================================================================================

MAIN_PROCESS = process

#print "NOW PROCESS NAME IS ",process.name_()," AND PROCESS ID IS ",id(process)

import os, subprocess, tempfile

tmpf = tempfile.NamedTemporaryFile(delete=False)
tmpf.close()

dumpcode = """dumpf = open(r'%s', 'w');
dumpf.write(process.dumpPython());
dumpf.close();
exit(); """ % tmpf.name

print "WILL FULLY EXPAND PATCMG_fastSim_cfg.py INTO %s" % tmpf.name

subp = subprocess.Popen(["python", "-i", "PATCMG_fastSim_cfg.py"], stdin=subprocess.PIPE, bufsize=-1)
subp.communicate(dumpcode)

subp.wait()

#print "WILL NOW READ %s" % tmpf.name
execfile(tmpf.name)
#print "NOW PROCESS NAME IS ",process.name_()," AND PROCESS ID IS ",id(process)

os.unlink(tmpf.name)
del process.source

###=================================================================================================================
###========  FINALIZE FOR SUBPROCESS  ==============================================================================
###=================================================================================================================

#### =========== SET THIS AS SUBPROCESS ================
MAIN_PROCESS.subProcess = cms.SubProcess(process,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

#### =========== AND PUT BACK THE MAIN AS PROCESS ======
process = MAIN_PROCESS

#print "NOW PROCESS NAME IS ",process.name_()," AND PROCESS ID IS ",id(process)
