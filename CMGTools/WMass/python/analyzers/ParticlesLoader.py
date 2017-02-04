from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Muon, Jet, GenParticle
from CMGTools.RootTools.physicsobjects.PileUpSummaryInfo import PileUpSummaryInfo

class ParticlesLoader(Analyzer):

    def declareHandles(self):
        super(ParticlesLoader, self).declareHandles()

        if self.cfg_ana.set_type == "light" or self.cfg_ana.set_type == "all":
            self.handles['muons'] = AutoHandle('cmgMuonSel', 'std::vector<cmg::Muon>')
            self.handles['pfmet'] = AutoHandle('cmgPFMET', 'std::vector<cmg::BaseMET>')
            self.handles['tkmet'] = AutoHandle('tkMet', 'std::vector<reco::PFMET>')

        if self.cfg_ana.set_type == "add_particles_list" or self.cfg_ana.set_type == "all":
            self.handles['jets_PF_CHS'] = AutoHandle('cmgPFJetSelCHS', 'std::vector<cmg::PFJet>')
            self.handles['PFCandidates'] = AutoHandle('cmgCandidates', 'std::vector<cmg::PackedCandidate>')
            if self.cfg_comp.isMC:
                self.mchandles['genpart'] =  AutoHandle('genParticlesPruned', 'std::vector<reco::GenParticle>')

        if self.cfg_ana.pileUpInfo:
            self.mchandles['pileUpInfo'] =  AutoHandle('addPileupInfo', 'std::vector<PileupSummaryInfo>')

    def beginLoop(self):
        super(ParticlesLoader,self).beginLoop()

    def process(self, iEvent, event):
        # if hasattr(self.cfg_ana,"MaxNumberOfEvents"):
        #     self.cfg_ana.StartNumberOfEvents += 1
        #     if self.cfg_ana.StartNumberOfEvents == 1+self.cfg_ana.MaxNumberOfEvents:
        #         print "--------------- Max event reached: ", self.cfg_ana.StartNumberOfEvents
        #         return False

        self.readCollections( iEvent )

        if self.cfg_ana.set_type == "light" or self.cfg_ana.set_type == "all":
            event.muons = map(Muon, self.handles['muons'].product())
            ##Perform vertex association: not automatic!!!
            for muon in event.muons:
                muon.associatedVertex = event.goodVertices[0]

                # dl = map(muon.dz, event.goodVertices)
                # muon.associatedVertex = event.goodVertices[dl.index(min(dl))]


            event.met_pf = self.handles['pfmet'].product()[0]
            event.met_tk = self.handles['tkmet'].product()[0]

        if self.cfg_ana.set_type == "add_particles_list" or self.cfg_ana.set_type == "all":
            event.jets_pf_chs = map(Jet, self.handles['jets_PF_CHS'].product())
            event.jets_pf_chs.sort(key=lambda x: x.pt(), reverse=True)
            event.pf_candidates = self.handles['PFCandidates'].product()
            '''
            Each candidate has methods:
            pt, eta, phi, mass, pdgId, fromPV, p4, charge, vx, vy, vz
            '''
            # vx,vy,vz
            # print "Trial vx of pf candidates-------------------------------"
            # print event.pf_candidates[0].vz() in cm
            # print event.goodVertices[0].z()
            # taglia a 500 mu


            if self.cfg_comp.isMC:
              event.gen_particles = map(GenParticle, self.mchandles['genpart'].product())


        if self.cfg_ana.pileUpInfo:
            event.pileUpInfo = map(PileUpSummaryInfo, self.mchandles['pileUpInfo'].product())
