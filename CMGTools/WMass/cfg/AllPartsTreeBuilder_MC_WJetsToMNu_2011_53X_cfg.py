import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.WMass.triggerMap import triggers_mu
from copy import deepcopy

json_analyzer = cfg.Analyzer(
    'JSONAnalyzer',
    )

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
    pileUpInfo = False,
    # MaxNumberOfEvents = 10,
    # StartNumberOfEvents = 0
    )

selection_analyzers = cfg.Analyzer(
    'WMassEventSelection',
    event_type = "W",
    pt_muon_thr = 20,
    mass_region = [70, 110],
    met_type = "pfmet",
    met_thr = 20,  #GeV
    muon_max_dz = 0.1, #cm
    )

# particle_loader2 = cfg.Analyzer(
#     "ParticlesLoader",
#     set_type = "add_particles_list"
#     )

recoil_analyzer = cfg.Analyzer(
    'RecoilAnalyzer',
    event_type = "W",
    tracks_max_dz = 0.1 #cm
    )

hardest_subprocess_analyzer = cfg.Analyzer(
    'HardestSubprocessAnalyzer',
    event_type = "W",
    verbose = "True"
    )

recoil_correction_coefficients_analyzer = cfg.Analyzer(
    "RecoilCorrectionCoefficients",
    event_type = "W"
    )

tree_producer = cfg.Analyzer(
    "AllParticleTree",
    # verbose = False,
    # recoil_info = False
    # upar_uperp = False
    # jet_info = False
    )


sequence = cfg.Sequence([
    json_analyzer,
    trigger_bit_filter,
    vertex_analyzer,
    particle_loader1,
    selection_analyzers,
    # particle_loader2,
    hardest_subprocess_analyzer,
    # recoil_analyzer,
    # recoil_correction_coefficients_analyzer,
    tree_producer,
   ])

from CMGTools.H2TauTau.proto.samples.ewk import WJets
from CMGTools.H2TauTau.proto.samples.getFiles import getFiles

WJetsPlus = deepcopy(WJets)
WJetsPlus.files = getFiles('/WplusToMuNu_M-50To250_ew-BMNNP_7TeV-powheg-pythia8/Summer11LegDR-PU_S13_START53_LV6-v1/AODSIM/V5_B/PAT_CMG_V5_18_0', 'cmgtools', '.*root')
# 792 files
# 23k eventi per file
WJetsPlus.files = WJetsPlus.files[:50]
WJetsPlus.triggers = triggers_mu
WJetsPlus.splitFactor = 50 #900
WJetsPlus.name = 'WPlus1'


# WJetsMinus = deepcopy(WJetsPlus)
# WJetsMinus.name = 'WMinus1'
# WJetsMinus.files = getFiles('/WminusToMuNu_M-50To250_ew-BMNNP_7TeV-powheg-pythia8/Summer11LegDR-PU_S13_START53_LV6-v1/AODSIM/V5_B/PAT_CMG_V5_18_0', 'cmgtools', '.*root') # 2106
# WJetsMinus.files = WJetsMinus.files[:1]



selectedComponents = [WJetsPlus]


config = cfg.Config(components = selectedComponents, sequence = sequence)

printComps(config.components, True)
