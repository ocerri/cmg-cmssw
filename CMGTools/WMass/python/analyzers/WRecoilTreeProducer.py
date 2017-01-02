from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ntupleFunctions import *

class WRecoilTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(WRecoilTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        if not hasattr(self.cfg_ana,"recoil_info"):
            self.cfg_ana.recoil_info = True

        if not hasattr(self.cfg_ana, "upar_uperp"):
            self.cfg_ana.upar_uperp = True

        T = self.tree

        var(T, "n_evt", int) ##Vedere come fanno in altre analisi
        var(T, "n_vtx", int)

        bookMuonZ(T, "muon")

        if self.cfg_comp.isMC:
            bookVB(T, "Wgen")
            bookMuonZgen(T, "muon_gen")
            # bookMuonZgen(T, "nu_gen")

            bookMuonZgen(T, "muon_genFS")
            var(T, "has_FSR", int)

        if  self.cfg_ana.recoil_info == True:
            bookRecoilInfo(T, "tk")
            bookRecoilInfo(T, "tk_not_pv")
            bookRecoilInfo(T, "nt")
            if self.cfg_comp.isMC:
                bookCorrectionCoeff(T)

        if self.cfg_ana.upar_uperp == True:
            bookUparUperp(T, "tk")
            bookUparUperp(T, "tk_not_pv")
            bookUparUperp(T, "nt")
            if self.cfg_comp.isMC:
                bookUparUperp(T, "MC")


    def process(self, iEvent, event):
        T = self.tree
        T.reset()

        # fill(T, "evt_number", int(iEvent))
        fill(T, 'n_evt', event.eventId)
        fill(T, "n_vtx", len(event.goodVertices))

        fillMuonZ(T, "muon", event.muon_W)

        if self.cfg_comp.isMC:
            fillVB(T, event, "Wgen")

            fillMuonZgen(T, "muon_gen", event.muon_gen_HS)
            # fillMuonZgen(T, "nu_gen", event.nu_gen_HS)

            fillMuonZgen(T, "muon_genFS", event.muons_gen_FS[0])
            fill(T, "has_FSR", event.has_FSR)

        if  self.cfg_ana.recoil_info == True:
            fillRecoilInfo(T, event, "tk")
            fillRecoilInfo(T, event, "tk_not_pv")
            fillRecoilInfo(T, event, "nt")
            if self.cfg_comp.isMC:
                fillCorrectionCoeff(T, event)

        if self.cfg_ana.upar_uperp == True:
            fillUparUperp(T, event, "tk")
            fillUparUperp(T, event, "tk_not_pv")
            fillUparUperp(T, event, "nt")
            if self.cfg_comp.isMC:
                fillUparUperp(T, event, "MC")



        T.tree.Fill()
