from ROOT import TLorentzVector
from CMGTools.RootTools.physicsobjects.Particle import Particle
from numpy import sign

class PFCandidate(Particle):

    def __init__(self, cmg_packed_candidate = None):
        if cmg_packed_candidate != None:

            ###---This are not good: must be rescaled----------------####
            self.pt = cmg_packed_candidate.pt()
            self.eta = cmg_packed_candidate.eta()
            self.phi = cmg_packed_candidate.phi()
            self.m = cmg_packed_candidate.mass()
            ##############################################################

            self.p4 = TLorentzVector()
            p4.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.m)

            self.pdgId = cmg_packed_candidate.pdgId()

            self.fromPV = cmg_packed_candidate.fromPV()

            if (self.pdgId in [22, 130, 310]):
                self.charge = 0
            elif (abs(self.pdgId) in [11, 13, 15]):
                self.charge = -sign(self.pdgId)
            else: self.charge = sign(self.pdgId)

    def Pt(self):
        return self.p4.Pt()

    def pt(self):
        return self.p4.Pt()

    def eta(self):
        return self.p4.Eta()

    def pdgId(self):
        return self.pdgId

    def charge(self):
        return self.charge

    def fromPV(self):
        return self.fromPV
