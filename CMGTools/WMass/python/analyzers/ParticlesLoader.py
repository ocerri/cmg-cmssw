from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from CMGTools.RootTools.physicsobjects.PhysicsObjects import Muon, Jet, GenParticle

class ParticlesLoader(Analyzer):

    def declareHandles(self):
        super(ParticlesLoader, self).declareHandles()

        if self.cfg_ana.set_type == "light" or self.cfg_ana.set_type == "all":
            self.handles['muons'] = AutoHandle('cmgMuonSel','std::vector<cmg::Muon>')
            self.handles['pfmet'] = AutoHandle('cmgPFMET','std::vector<cmg::BaseMET>' )
            self.handles['tkmet'] = AutoHandle('tkMet','std::vector<reco::PFMET>' )

        if self.cfg_ana.set_type == "add_particles_list" or self.cfg_ana.set_type == "all":
            self.handles['jets_PF'] = AutoHandle('cmgPFJetSel','std::vector<cmg::PFJet>')
            self.handles['PFCandidates'] = AutoHandle('cmgCandidates','std::vector<cmg::PackedCandidate>')
            if self.cfg_comp.isMC:
                self.mchandles['genpart'] =  AutoHandle('genParticlesPruned','std::vector<reco::GenParticle>')

    def beginLoop(self):
        super(ParticlesLoader,self).beginLoop()

    def process(self, iEvent, event):
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
            event.jets_pf = map(Jet, self.handles['jets_PF'].product())

            event.pf_candidates = self.handles['PFCandidates'].product()
            '''
            Each candidate has methods:
            pt, eta, phi, mass, pdgId, fromPV, p4, charge
            '''


            if self.cfg_comp.isMC:
              event.gen_particles = map(GenParticle, self.mchandles['genpart'].product())
