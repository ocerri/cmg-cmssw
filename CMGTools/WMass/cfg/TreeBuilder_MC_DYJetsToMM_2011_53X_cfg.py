import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.WMass.triggerMap import triggers_mu

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
    set_type = "all"
    )

selection_analyzers = cfg.Analyzer(
    'WMassEventSelection',
    event_type = "Z",
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
    )

hardest_subprocess_analyzer = cfg.Analyzer(
    'HardestSubprocesAnalyzer'
    )

tree_producer = cfg.Analyzer(
    "ZRecoilTreeProducer",
    verbose = False
    )


sequence = cfg.Sequence([
    trigger_bit_filter,
    vertex_analyzer,
    particle_loader1,
    selection_analyzers,
    # particle_loader2,
    recoil_analyzer,
    # hardest_subprocess_analyzer,
    tree_producer,
   ])

from CMGTools.H2TauTau.proto.samples.ewk import DYJets
from CMGTools.H2TauTau.proto.samples.getFiles import getFiles

DYJets.files = getFiles('/DYToMuMu_M-50To250_ew-BMNNP_7TeV-powheg/Summer11LegDR-PU_S13_START53_LV6-v1/AODSIM/V5_B/PAT_CMG_V5_18_0_newLHEweights', 'wmass_group', '.*root') # 790

DYJets.files = DYJets.files[:1]

DYJets.triggers = triggers_mu
# DYJets.splitFactor = 900
DYJets.splitFactor = 1

selectedComponents = [DYJets]

config = cfg.Config(components = selectedComponents, sequence = sequence)

printComps(config.components, True)
