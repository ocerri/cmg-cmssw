from CMGTools.RootTools.fwlite.Analyzer import Analyzer
from ROOT import TLorentzVector, TVector3, TVector2, TMath
from copy import deepcopy
from UtilsFunctions import particle2TLorenzVector

class HardestSubprocessAnalyzer(Analyzer):
    '''
    TODO: retrieve muons, Z and h from gen particles and store them.
        capirci qualcosa
    '''

    def process(self, iEvent, event):


        if self.cfg_ana.event_type == "Z":

            event.Zreco_p4 = particle2TLorenzVector(event.muons[0]) + particle2TLorenzVector(event.muons[1])

            if self.cfg_comp.isMC:

                genZ_dummy = [ genp for genp in event.gen_particles if ( genp.pdgId() ==23 and abs(genp.status())==62 )]
                if len(genZ_dummy) > 1:
                    print "Error: Gen VB ambiguity"
                    return False
                elif len(genZ_dummy) == 0:
                    print "Error: Gen VB not found"
                    return False

                event.Zgen = genZ_dummy[0]

                if hasattr(self.cfg_ana, "verbose"):
                    if self.cfg_ana.verbose == True:
                        print "HSB: len genZ_dummy", len(genZ_dummy)
                        print 'Zgen.numberOfDaughters()=', event.Zgen.numberOfDaughters()
                        print 'Zgen.daughter(0)', event.Zgen.daughter(0).pdgId(), 'status', event.Zgen.daughter(0).status()
                        print 'Zgen.daughter(1)', event.Zgen.daughter(1).pdgId(), 'status', event.Zgen.daughter(1).status()

                #Muons from the hardest subrocess has produced by the Z boson
                event.muons_gen_HS = [event.Zgen.daughter(0), event.Zgen.daughter(1)]
                if event.muons_gen_HS[0].status() != 1 or event.muons_gen_HS[1].status() != 1:
                    event.has_FSR = 1
                else:
                    event.has_FSR = 0


                #Finale state muons, after FSR and all the rest....
                event.muons_gen_FS =[part for part in event.gen_particles if ( abs(part.pdgId()) ==13 and part.status()==1 )]


                ##########------------------Debuging lines------------####################
                if hasattr(self.cfg_ana, "verbose"):
                    if self.cfg_ana.verbose == True:
                        if len(event.muons_gen_FS)!= 2:
                            print "HS muons:"
                            for p in event.muons_gen_HS:
                                print p.pt(), p.phi(), p.eta()

                            print "FS muons"
                            for p in event.muons_gen_FS:
                                print p.pt(), p.phi(), p.eta()

                        if hasattr(self.cfg_ana, "hyper_verbose"):
                            print "Status   mother(0)   mother(1)   daughter(0) daughter(0)"
                            for part in [ genp for genp in event.gen_particles if abs(genp.pdgId())==13 ]:
                                print part.status(), '\t', part.mother(0).pdgId()," ", part.mother(0).status()
                                if hasattr(part, "mother(1)"):
                                    print part.mother(1).pdgId()," ", part.mother(1).status()

                                if hasattr(part, "daughter(0)"):
                                    print type(part.daughter(0))
                                    print part.daughter(0).pdgId()," ",part.daughter(0).status()
                                    if hasattr(part, "daughter(1)"):
                                        print part.daughter(1).pdgId()," ",part.daughter(1).status()
                                    else:
                                        print "No daughters"
                                else:
                                    print "No attribute"

                                print '.\n', '.\n'
                #################---------------------------------###########################


        elif self.cfg_ana.event_type == "W" and self.cfg_comp.isMC:

            if self.cfg_comp.isMC:

                genW_dummy = [ genp for genp in event.gen_particles if ( abs(genp.pdgId()) ==24 and abs(genp.status())==62 )]
                if len(genW_dummy) > 1:
                    print "Error: Gen VB ambiguity"
                    return False
                elif len(genW_dummy) == 0:
                    print "Error: Gen VB not found"
                    return False

                event.Wgen = genW_dummy[0]

                if hasattr(self.cfg_ana, "verbose"):
                    if self.cfg_ana.verbose == True:
                        print "--------------- VERBOSITY ----------------------"
                        print "HSB: len genW_dummy", len(genW_dummy)
                        print 'Wgen.numberOfDaughters()=', event.Wgen.numberOfDaughters()
                        print 'Wgen.daughter(0)', event.Wgen.daughter(0).pdgId(), 'status', event.Wgen.daughter(0).status()
                        # Usually there are no neutrinos in the event record....


                #Leptons from the hardest subrocess has produced by the W boson
                if event.Wgen.numberOfDaughters() ==2:
                    if abs(event.Wgen.daughter(0).pdgId()) == 13:
                        event.muon_gen_HS = event.Wgen.daughter(0)
                        event.nu_gen_HS = event.Wgen.daughter(1)
                    else:
                        event.muon_gen_HS = event.Wgen.daughter(1)
                        event.nu_gen_HS = event.Wgen.daughter(0)
                elif event.Wgen.numberOfDaughters() ==1:
                        event.muon_gen_HS = event.Wgen.daughter(0)


                if event.muon_gen_HS.status() != 1:
                    event.has_FSR = 1
                else:
                    event.has_FSR = 0


                #Final state muons, after FSR and all the rest....
                event.muons_gen_FS =[part for part in event.gen_particles if ( abs(part.pdgId()) ==13 and part.status()==1 )]

        return True
