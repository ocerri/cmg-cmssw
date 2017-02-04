import CMGTools.RootTools.fwlite.Config as cfg
from CMGTools.RootTools.fwlite.Config import printComps
from CMGTools.WMass.triggerMap import triggers_mu

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
    pileUpInfo = False
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
    event_type = "Z"
    )

hardest_subprocess_analyzer = cfg.Analyzer(
    'HardestSubprocessAnalyzer',
    event_type = "Z"
    )

tree_producer = cfg.Analyzer(
    "ZRecoilTreeProducer",
    verbose = False,
    # recoil_info = False
    # upar_uperp = False
    )


sequence = cfg.Sequence([
    json_analyzer,
    trigger_bit_filter,
    vertex_analyzer,
    particle_loader1,
    selection_analyzers,
    # particle_loader2,
    hardest_subprocess_analyzer,
    recoil_analyzer,
    tree_producer,
   ])



from CMGTools.H2TauTau.proto.samples.getFiles import getFiles

data_Run2011A_12Oct2013_v1 = cfg.DataComponent(
    name = 'data_Run2011A_12Oct2013_v1',
    files = getFiles('/SingleMu/Run2011A-12Oct2013-v1/AOD/PAT_CMG_V5_18_0', 'cmgtools', '.*root'),
    intLumi =  4749.90,
    triggers = triggers_mu,
    json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Reprocessing/Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON_v2.txt'
    )

selectedComponents = [data_Run2011A_12Oct2013_v1]
data_Run2011A_12Oct2013_v1.files = data_Run2011A_12Oct2013_v1.files[:100]
data_Run2011A_12Oct2013_v1.splitFactor = 1

config = cfg.Config(components=selectedComponents,
                    sequence=sequence)

printComps(config.components, True)
