import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.WMass.triggerMap import triggers_mu
from copy import deepcopy

trigger_bit_filter = cfg.Analyzer(
     'triggerBitFilter',
     # verbose = True,
    )

vertex_analyzer = cfg.Analyzer(
    'VertexAnalyzer',
    allVertices = 'slimmedPrimaryVertices',
    goodVertices = 'slimmedPrimaryVertices',
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False,
    keepFailingEvents = False,
    )

particle_loader1 = cfg.Analyzer(
    "ParticlesLoader",
    # set_type = "light"
    set_type = "all",
    pileUpInfo = True
    )

particle_tree_producer = cfg.Analyzer(
    "ParticleTreeProducer",
    )

sequence = cfg.Sequence([
    trigger_bit_filter,
    vertex_analyzer,
    particle_loader1,
    particle_tree_producer,
   ])

from CMGTools.H2TauTau.proto.samples.ewk import WJets
from CMGTools.H2TauTau.proto.samples.getFiles import getFiles

WJetsPlus = deepcopy(WJets)
WJetsPlus.files = getFiles('/WplusToMuNu_M-50To250_ew-BMNNP_7TeV-powheg-pythia8/Summer11LegDR-PU_S13_START53_LV6-v1/AODSIM/V5_B/PAT_CMG_V5_18_0', 'cmgtools', '.*root') # 1389
WJetsPlus.files = WJetsPlus.files[:150]
WJetsPlus.triggers = triggers_mu
WJetsPlus.splitFactor = 1 #900
WJetsPlus.name = 'WPlus1'


# WJetsMinus = deepcopy(WJetsPlus)
# WJetsMinus.name = 'WMinus1'
# WJetsMinus.files = getFiles('/WminusToMuNu_M-50To250_ew-BMNNP_7TeV-powheg-pythia8/Summer11LegDR-PU_S13_START53_LV6-v1/AODSIM/V5_B/PAT_CMG_V5_18_0', 'cmgtools', '.*root') # 2106
# WJetsMinus.files = WJetsMinus.files[:1]



selectedComponents = [WJetsPlus]

config = cfg.Config(components = selectedComponents, sequence = sequence)

printComps(config.components, True)
