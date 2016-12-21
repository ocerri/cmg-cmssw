from ROOT import TLorentzVector

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
    if p4Ref == None and p42 == None:
        p4Ref = partRef.p4()
        p42 = part2.p4()

    u_par = (p4Ref.Px()*p42.Px() + p4Ref.Py()*p42.Py()) / p4Ref.Pt()
    u_perp = (p4Ref.Px()*p42.Py() - p4Ref.Py()*p42.Px()) / p4Ref.Pt()
    return (u_par, u_perp)


def compute_u_par(partRef = None, part2 = None, p4Ref = None, p42 = None):
    aux = get_u_projection(partRef, part2, p4Ref, p42)
    return aux[0]

def compute_u_perp(partRef = None, part2 = None, p4Ref = None, p42 = None):
    aux = get_u_projection(partRef, part2, p4Ref, p42)
    return aux[1]
