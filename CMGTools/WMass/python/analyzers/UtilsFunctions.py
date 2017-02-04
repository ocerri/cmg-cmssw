from ROOT import TLorentzVector, TMath
from copy import deepcopy
from math import sqrt

def particle2TLorenzVector(particle):
    p4 = TLorentzVector(0, 0, 0, 0)
    p4.SetPtEtaPhiM(particle.pt(), particle.eta(), particle.phi(), particle.mass())
    return p4

def reduce_angle(angle):
    while(angle < (-1)*TMath.Pi()):
        angle += TMath.Pi()
    while(angle > TMath.Pi()):
        angle -= TMath.Pi()
    return angle

def p4_transverse(p4):
    Et = numpy.sqrt(p4.Px()**2 + p4.Py()**2)
    return TLorentzVector(p4.Px(), p4.Py(), 0., Et)

def transverse_mass(p4_list):
    p_transverse_tot = TLorentzVector(0., 0., 0., 0.)
    for p4 in p4_list:
        p_transverse_tot += p4_transverse(p4)
    return p_transverse_tot.M()

def reduce_angle(angle):
    while(angle < (-1)*TMath.Pi()):
        angle += TMath.Pi()
    while(angle > TMath.Pi()):
        angle -= TMath.Pi()
    return angle

def compute_u_projections(partRef = None, part2 = None, p4Ref = None, p42 = None):
    if p4Ref == None:
        p4Ref = particle2TLorenzVector(partRef)
    if p42 == None:
        p42 = particle2TLorenzVector(part2)

    u_par = (p4Ref.Px()*p42.Px() + p4Ref.Py()*p42.Py()) / p4Ref.Pt()
    u_perp = (p4Ref.Px()*p42.Py() - p4Ref.Py()*p42.Px()) / p4Ref.Pt()
    return (u_par, u_perp)


def compute_u_par(partRef = None, part2 = None, p4Ref = None, p42 = None):
    aux = compute_u_projections(partRef, part2, p4Ref, p42)
    return aux[0]

def compute_u_perp(partRef = None, part2 = None, p4Ref = None, p42 = None):
    aux = compute_u_projections(partRef, part2, p4Ref, p42)
    return aux[1]

def delta_phi(p41, p42):
    aux_delta_phi = p41.Phi() - p42.Phi()
    aux_delta_phi = reduce_angle(aux_delta_phi)
    return aux_delta_phi

def deltaR2(part1=None, part2=None, p41=None, p42=None):
    if p41 == None:
        p41 = particle2TLorenzVector(part1)
    if p42 == None:
        p42 = particle2TLorenzVector(part2)

    aux_delta_phi = delta_phi(p41, p42)
    aux_delta_eta = p41.Eta() - p42.Eta()

    aux_deltaR2 = aux_delta_phi**2 + aux_delta_eta**2
    return aux_deltaR2

def deltaR(**kwargs):
    return sqrt(deltaR2(**kwargs))

def kt_distance(p41, p42, p=-1, R=0.5):
    d = min([p41.Pt()**(2*p), p42.Pt()**(2*p)]) * deltaR2(p41=p41, p42=p42) / (R**2)
    return d
