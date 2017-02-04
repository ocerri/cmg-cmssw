from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ntupleFunctions import *

class ZRecoilTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ZRecoilTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        if not hasattr(self.cfg_ana,"recoil_info"):
            self.cfg_ana.recoil_info = True

        if not hasattr(self.cfg_ana, "upar_uperp"):
            self.cfg_ana.upar_uperp = True

        T = self.tree

        var(T, "n_evt", int) ##Vedere come fanno in altre analisi
        var(T, "n_vtx", int)

        bookMuonZ(T, "pos_muon")
        bookMuonZ(T, "neg_muon")
        bookVB(T,"Zreco")

        if self.cfg_comp.isMC:
            bookVB(T, "Zgen")
            bookMuonZgen(T, "pos_muon_gen")
            bookMuonZgen(T, "neg_muon_gen")
            bookMuonZgen(T, "pos_muon_genFS")
            bookMuonZgen(T, "neg_muon_genFS")
            var(T, "has_FSR", int)

        if  self.cfg_ana.recoil_info == True:
            bookRecoilInfo(T, "tk")
            bookRecoilInfo(T, "tk_not_pv")
            bookRecoilInfo(T, "nt")
            if self.cfg_comp.isMC:
                bookCorrectionCoeff(T)

        if self.cfg_ana.upar_uperp == True:
            bookUparUperp(T, "pos_tk")
            bookUparUperp(T, "neg_tk")
            bookUparUperp(T, "pos_tk_not_pv")
            bookUparUperp(T, "neg_tk_not_pv")
            bookUparUperp(T, "pos_nt")
            bookUparUperp(T, "neg_nt")
            bookUparUperp(T, "pos_Z")
            bookUparUperp(T, "neg_Z")


    def process(self, iEvent, event):
        T = self.tree
        T.reset()

        fill(T, 'n_evt', event.eventId)
        fill(T, "n_vtx", len(event.goodVertices))
        # fill(T, "evt_number", int(iEvent))

        event.muons = sorted(event.muons, key=lambda x: x.charge(), reverse=True)
        fillMuonZ(T, "pos_muon", event.muons[0])
        fillMuonZ(T, "neg_muon", event.muons[1])

        fillVB(T, event, "Zreco", p4 = event.Zreco_p4)

        if self.cfg_comp.isMC:
            fillVB(T, event, "Zgen")

            event.muons_gen_HS = sorted(event.muons_gen_HS, key=lambda x: x.charge(), reverse=True)
            fillMuonZgen(T, "pos_muon_gen", event.muons_gen_HS[0])
            fillMuonZgen(T, "neg_muon_gen", event.muons_gen_HS[1])

            event.muons_gen_FS = sorted(event.muons_gen_FS, key=lambda x: x.charge(), reverse=True)
            fillMuonZgen(T, "pos_muon_genFS", event.muons_gen_FS[0])
            fillMuonZgen(T, "neg_muon_genFS", event.muons_gen_FS[1])
            fill(T, "has_FSR", event.has_FSR)

        if  self.cfg_ana.recoil_info == True:
            fillRecoilInfo(T, event, "tk")
            fillRecoilInfo(T, event, "tk_not_pv")
            fillRecoilInfo(T, event, "nt")
            if self.cfg_comp.isMC:
                fillCorrectionCoeff(T, event)

        if self.cfg_ana.upar_uperp == True:
            fillUparUperp(T, event, "pos_tk")
            fillUparUperp(T, event, "neg_tk")
            fillUparUperp(T, event, "pos_tk_not_pv")
            fillUparUperp(T, event, "neg_tk_not_pv")
            fillUparUperp(T, event, "pos_nt")
            fillUparUperp(T, event, "neg_nt")
            fillUparUperp(T, event, "pos_Z")
            fillUparUperp(T, event, "neg_Z")



        T.tree.Fill()
