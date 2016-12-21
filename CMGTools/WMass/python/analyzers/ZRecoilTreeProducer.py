from CMGTools.RootTools.analyzers.TreeAnalyzerNumpy import TreeAnalyzerNumpy
from ntupleFunctions import *

class ZRecoilTreeProducer(TreeAnalyzerNumpy):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ZRecoilTreeProducer, self).__init__(cfg_ana, cfg_comp, looperName)

    def declareVariables(self):
        T = self.tree

        var(T, "evt_number", int)

        bookMuonZ(T, "pos_muon")
        bookMuonZ(T, "neg_muon")

        bookRecoilInfo(T, "tk")
        bookRecoilInfo(T, "tk_not_pv")
        bookRecoilInfo(T, "nt")

        bookUparUperp(T, "pos_tk")
        bookUparUperp(T, "neg_tk")
        bookUparUperp(T, "pos_tk_not_pv")
        bookUparUperp(T, "neg_tk_not_pv")
        bookUparUperp(T, "pos_nt")
        bookUparUperp(T, "neg_nt")



    def process(self, iEvent, event):
        T = self.tree
        T.reset()

        fill(T, "evt_number", int(iEvent))

        fillMuonZ(T, "pos_muon", event.muons[0])
        fillMuonZ(T, "neg_muon", event.muons[1])

        fillRecoilInfo(T, event, "tk")
        fillRecoilInfo(T, event, "tk_not_pv")
        fillRecoilInfo(T, event, "nt")

        fillUparUperp(T, event, "pos_tk")
        fillUparUperp(T, event, "neg_tk")
        fillUparUperp(T, event, "pos_tk_not_pv")
        fillUparUperp(T, event, "neg_tk_not_pv")
        fillUparUperp(T, event, "pos_nt")
        fillUparUperp(T, event, "neg_nt")


        T.tree.Fill()
