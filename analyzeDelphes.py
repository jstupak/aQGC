maxEvents=9E9
DEBUG=False

jetType='KTjet'

particle={
    11:"e",
    13:"mu",
    21:"gamma", #using this for all jets
    22:"j",
    23:"z",
    24:"w"
}

#OBJECT SELECTION
pTMin={
    11:1,
    13:1,
    21:5,       #using this for all jets
    22:1
}

etaMax={11:2.5,
        13:2.5,
        21:10,
        22:1
        }

#---------------------------------------------------------
#EVENT SELECTION

#---------------------------------------------------------
import pdb
from sys import argv
#---------------------------------------------------------
from ROOT import *

gSystem.Load("libDelphes")
gStyle.SetOptStat(0)

#---------------------------------------------------------
def printHist(h):
    for i in range(h.GetNbinsX()+2):
        print h.GetBinContent(i),
        
#---------------------------------------------------------
#return TLorentzVector corresponding to sum of inputs

def parentConstructor(a,b):
    return a.P4()+b.P4()

#---------------------------------------------------------
#returns subset of input collection passing cut string ('x' is placeholder for item in input)
#usage: selector(tree.Electron,'x.PT>50')

def selector(input,cutString='x.PT>20'):
    return [x for x in input if eval(cutString)]

#---------------------------------------------------------

def getParents(p):
    result=[p]

    motherIndices=[]
    if p.M1!=-1 and tree.Particle[p.M1].PID==p.PID:
        motherIndices.append(p.M1)
    if p.M2!=-1 and tree.Particle[p.M2].PID==p.PID:
        motherIndices.append(p.M2)
    result+=[getParents(tree.Particle[i]) for i in motherIndices]

    return result

def isBeamRemnant(p):
    parents=getParents(p)
    while type(parents)==type([]): parents=parents[-1]
    return parents.Status==4

#---------------------------------------------------------

if __name__=='__main__':
    
    inputName=str(argv[1])
    if len(argv)>2:
        tag=str(argv[2])
    else:
        tag=''
    outputName=(bool(tag)*(tag+'_'))+inputName.replace('.root','.hist.root')

    print "inputName:",inputName
    print "tag:",tag
    
    f=TFile(inputName)
    tree=f.Get("Delphes")
    output=TFile(outputName,"RECREATE")

    #sets upper limit for bin range
    bin_range = 15000

    #declares truth-level pT, p, eta, and multiplicity histograms for e,mu,W,Z,gamma
    h_truth={}
    for p in [11,13,21,22,23,24]:
        h_truth[p]={}
        h_truth[p]['pT'] =TH1F('T_%s_pT'%particle[p],';Truth %s pT [GeV];Events'%particle[p], 200, 0, bin_range)
        h_truth[p]['p']  =TH1F('T_%s_p'%particle[p],';Truth %s p [GeV];Events'%particle[p], 200, 0, bin_range)
        h_truth[p]['eta']=TH1F('T_%s_eta'%particle[p],';Truth %s #eta;Events'%particle[p], 20, -4, 4)
        h_truth[p]['mult']=TH1F('T_%s_mult'%particle[p],';Truth %s multiplicity;Events'%particle[p], 7, -0.5, 6.5)


    #missing energy histograms
    T_missingEt = TH1F('T_missingEt', ';Missing Transverse Energy [GeV];Events', 200, 0, bin_range)
    T_missingE = TH1F('T_missingE', ';Missing Energy [GeV];Events', 200, 0, bin_range)

    h_reco={}
    for p in [11,13,21,22]:
        h_reco[p]={}
        h_reco[p]['pT']={}
        h_reco[p]['p']={}
        h_reco[p]['eta']={}

        h_reco[p]['mult']=TH1F('R_%s_mult'%particle[p],';%s multiplicity;Events'%particle[p], 7, -0.5, 6.5)
        for i in ['I']+range(4):
            h_reco[p]['pT'][i]=TH1F('R_%s_Pt_%s'%(particle[p],i),';%s pT [GeV];Events'%particle[p], 200, 0, bin_range)
            h_reco[p]['p'][i]=TH1F('R_%s_P_%s'%(particle[p],i),';%s pT [GeV];Events'%particle[p], 200, 0, bin_range)
            h_reco[p]['eta'][i]=TH1F('R_%s_eta_%s'%(particle[p],i),';%s pT [GeV];Events'%particle[p], 20, -4, 4)

    #histograms for OS pairs
    R_ee_pT = TH1F('ee_pT', ';pT [GeV];Events', 200, 0, bin_range)
    R_ee_eta = TH1F('ee_Eta', ';Eta;Events', 20, -4, 4)
    R_ee_mass = TH1F('ee_mass', ';Mass [GeV];Events', 200, 0, 200)
    R_ee_deltaEta = TH1F('ee_Delta Eta', ';Delta Eta;Events', 20, -4, 4)
    R_ee_multiplicity = TH1F('multiplicity', ';Multiplicity;Events', 5, -.5, 4.5)

    R_mumu_pT = TH1F('mumu_pT', ';pT [GeV];Events', 200, 0, bin_range)
    R_mumu_eta = TH1F('mumu_Eta', ';Eta;Events', 20, -4, 4)
    R_mumu_mass = TH1F('mumu_mass', ';Mass [GeV];Events', 200, 0, 200)
    R_mumu_deltaEta = TH1F('mumu_Delta Eta', ';Delta Eta;Events', 20, -4, 4)
    R_mumu_multiplicity = TH1F('mumu_multiplicity', ';Multiplicity;Events', 5, -.5, 4.5)

    R_emu_pT = TH1F('emu_pT', ';pT [GeV];Events', 200, 0, bin_range)
    R_emu_eta = TH1F('emu_Eta', ';Eta;Events', 20, -4, 4)
    R_emu_mass = TH1F('emu_mass', ';Mass [GeV];Events', 200, 0, 200)
    R_emu_deltaEta = TH1F('emu_Delta Eta', ';Delta Eta;Events', 20, -4, 4)
    R_emu_multiplicity = TH1F('emu_multplicity', ';Multiplicity;Events', 5, -.5, 4.5)

    #histograms for missing energy
    R_missingET = TH1F('R_MissingET', ';Missing Transverse Energy [GeV];Events', 200, 0, bin_range)
    R_missingE = TH1F('R_MissingE', ';Missing Energy [GeV];Events', 200, 0, bin_range)
    R_missingMass = TH1F('R_MissingMass', ';Missing Mass [GeV];Events' , 200, 0, bin_range)

    #histograms for beam remnants
    T_beamRemnants_pT = TH1F('T_beamRemnants_Pt', ';pT [GeV];Events', 200, 0, bin_range)
    T_beamRemnants_p = TH1F('T_beamRemnants_p', ';p [GeV];Events', 200, 0, bin_range)
    T_beamRemnants_eta = TH1F('T_beamRemnants_eta', ';Eta;Events', 20, -10, 10)
    T_beamRemnants_multiplicity = TH1F('T_beamRemnants_multiplicity', ';Multiplicity;Events', 7, -.5, 6.5)
    Test_beamRemnants_pT = TH1F('Test_beamRemnants_Pt', ';pT [GeV];Events', 30, 0, 3)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    
    for event in range(min(tree.GetEntries(),maxEvents)):
        tree.GetEntry(event)

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #truth level
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        truthElectrons=selector(tree.Particle,'x.Status==1 and abs(x.PID)==11')
        truthMuons    =selector(tree.Particle,'x.Status==1 and abs(x.PID)==13')
        truthWs       =selector(tree.Particle,'x.Status==22 and abs(x.PID)==24')
        truthZs       =selector(tree.Particle,'x.Status==22 and abs(x.PID)==23')
        truthPhotons  =selector(tree.Particle,'x.Status==1 and abs(x.PID)==22')
        truthNeutrinos=selector(tree.Particle,'x.Status==1 and (abs(x.PID)==12 or abs(x.PID)==14 or abs(x.PID)==16)')

        beamRemnantMuons   =selector(truthMuons,'isBeamRemnant(x)')
        nonBeamRemnantMuons=selector(truthMuons,'not isBeamRemnant(x)')
                         
        T_e_multiplicity.Fill(len(truthElectrons))
        T_mu_multiplicity.Fill(len(truthMuons))
        T_W_multiplicity.Fill(len(truthWs))
        T_z_multiplicity.Fill(len(truthZs))
        T_gamma_multiplicity.Fill(len(truthPhotons))
        T_beamRemnants_multiplicity.Fill(len(beamRemnantMuons))

        truthMissingP=TLorentzVector()
        for nu in truthNeutrinos:
            truthMissingP+=nu.P4()
                                        
        T_missingEt.Fill(truthMissingP.Et())
        T_missingE.Fill(truthMissingP.E())

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #reco level
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        R_missingET.Fill(tree.MissingET[0].MET)
        R_missingE.Fill(tree.MissingET[0].P4().P())

        #final and initial-state 4-vectors
        P4_i=TLorentzVector()
        P4_i+=Particle[0].P4()
        P4_i+=Particle[1].P4()
        
        P4_f = TLorentzVector()

        electrons=selector(tree.Electron,                 'x.PT>%f and abs(x.Eta)<%f'%(pTMin[11],etaMax[11]))
        muons    =selector(tree.Muon,                     'x.PT>%f and abs(x.Eta)<%f'%(pTMin[13],etaMax[13]))
        photons  =selector(tree.Photon,                   'x.PT>%f and abs(x.Eta)<%f'%(pTMin[22],etaMax[22]))
        jets     =selector(tree.__getattribute__(jetType),'x.PT>%f and abs(x.Eta)<%f'%(pTMin[21],etaMax[21]))
        
        #electrons=selector(tree.Electron,'x.PT>5 and abs(x.Eta)<2')
        #muons=selector(tree.Muon,'x.PT>5 and abs(x.Eta)<2')

        #fMuons=selector(tree.Muon,'abs(x.Eta)>2')
        #fMuons+=selector(tree.Electron,'abs(x.Eta)>2 and x.Particle.GetObject().PID==11 and x.Particle.GetObject().Status==1 and x.Particle.GetObject().M1<5')  #this is a hack - not a typo
       
        #sort object lists
        for collection in [electrons, muons, photons, jets]: collection.sort(key=operator.attrgetter('PT'),reverse=True)

        h_reco[11]['mult'].Fill(len(electrons))
        for i in range(len(electrons)):
            P4_f+=electrons[i].P4()
            h_reco[11]['pT']['I'].Fill(electrons[i].PT)
            h_reco[11]['p']['I'].Fill(electrons[i].P)
            h_reco[11]['eta']['I'].Fill(electrons[i].Eta)

            if i<4:
                h_reco[11]['pT'][i].Fill(electrons[i].PT)
                h_reco[11]['p'][i].Fill(electrons[i].P)
                h_reco[11]['eta'][i].Fill(electrons[i].Eta)

        h_reco[13]['mult'].Fill(len(muons))
        for i in range(len(muons)):
            P4_f+=muons[i].P4()
            h_reco[13]['pT']['I'].Fill(muons[i].PT)
            h_reco[13]['p']['I'].Fill(muons[i].PT)
            h_reco[13]['eta']['I'].Fill(muons[i].PT)            
            if i<4:
                h_reco[13]['pT'][i].Fill(muons[i].PT)
                h_reco[13]['p'][i].Fill(muons[i].P)
                h_reco[13]['eta'][i].Fill(muons[i].Eta)

        h_reco[22]['mult'].Fill(len(photons))
        for i in range(len(photons)):
            P4_f+=photons[i].P4()
            h_reco[22]['pT']['I'].Fill(photons[i].PT)
            h_reco[22]['p']['I'].Fill(photons[i].PT)
            h_reco[22]['eta']['I'].Fill(photons[i].PT)
            if i<4:
                h_reco[22]['pT'][i].Fill(photons[i].PT)
                h_reco[22]['p'][i].Fill(photons[i].P)
                h_reco[22]['eta'][i].Fill(photons[i].Eta)

        h_reco[11]['mult'].Fill(len(jets))
        for i in range(len(jets)):
            P4_f+=jets[i].P4()
            h_reco[21]['pT']['I'].Fill(jets[i].PT)
            h_reco[21]['p']['I'].Fill(jets[i].PT)
            h_reco[21]['eta']['I'].Fill(jets[i].PT)
            if i<4:
                h_reco[21]['pT'][i].Fill(jets[i].PT)
                h_reco[21]['p'][i].Fill(jets[i].P)
                h_reco[21]['eta'][i].Fill(jets[i].Eta)
        
        R_missingMass.Fill((P4_f-P4_i).M())

        #-------------------------------------------------------------------------------------------------
        leptons=electrons+muons

        Zs={}
        for i1 in range(len(leptons)-1):
            l1=leptons[i1]
            Zs[i1]={}
            for i2 in range(i1+1,len(leptons)):
                l2=leptons[i2]

                if (l1.Charge==l2.Charge) or (type(l1) != (type(l2))): Zs[i1][i2]=None
                else:                                                 Zs[i1][i2]=parentConstructor(l1,l2)

        minimum=9E9
        theZ=None
        for i1 in range(len(Zs.keys())):
            for i2 in range(len(Zs[i1].keys())):
                Zcand=Zs[i1][i2]
                if Zcand:
                    if abs(Zcand.Mass()-91.1876)<minimum:
                        theZ=Zcand
                        l1=leptons[i1]
                        l2=leptons[i2]
                        minimum=abs(theZ.Mass()-91.1876)
        if theZ:
            if type(l1)==type(Electron()):
                R_ee_mass.Fill(theZ.Mass())
                R_ee_pT.Fill(theZ.Pt())
                R_ee_eta.Fill(theZ.Eta())
                R_ee_deltaEta.Fill(abs(l1.Eta - l2.Eta))
            else:
                R_mumu_mass.Fill(theZ.Mass())
                R_mumu_pT.Fill(theZ.Pt())
                R_mumu_eta.Fill(theZ.Eta())
                R_mumu_deltaEta.Fill(abs(l1.Eta - l2.Eta))

        """
        ee = 0
        mumu = 0
        emu = 0
        if (len(leptons) > 1):
            #creates every possible unique OS lepton pair from event
            i = 0
            pairs1 = []
            pairs2 = []
            for i in range(len(leptons)):
                j = i + 1
                for j in range(i+1, len(leptons)):
                    p1 = leptons[i]
                    p2 = leptons[j]
                    #only selects OS pairs
                    if (p1.Charge != p2.Charge):
                        pairs1.append(leptons[i])
                        pairs2.append(leptons[j])
                    j = j + 1
                i = i + 1
            #creates two lists to hold the invariant mass of the pair, the difference between mass of the pair and the Z mass, and each particle of the pair
            a = []
            b = []
            for i in range(len(pairs1)):
                p1 = pairs1[i]
                p2 = pairs2 [i]
                a.append(p1.P4().M() + p2.P4().M() - 91)
                b.append(p1.P4().M() + p2.P4().M())

            #zips the 4 lists together in a tuple and sorts the list of pairs from closest to Z mass to furthest.   
            pairs = zip(a,b,pairs1,pairs2)
            pairs = sorted(pairs, key=lambda x:x[0])
            #loops through the list of sorted pairs and picks the pair closest to the Z mass that any 1 lepton participates in
            #prevents any 1 lepton from being in more than one pair. 
            consumed = []
            master_pairs = []
            for i in range(len(pairs)):
                if ((pairs[i][2] not in consumed) and (pairs[i][3] not in consumed)):
                    master_pairs.append(pairs[i])
                    consumed.append(pairs[i][2])
                    consumed.append(pairs[i][3])
            #sorts the pairs by type: ee, mumu, or emu and fills appropriate histograms
            for i in range(len(master_pairs)):
                l1 = master_pairs[i][2]
                l2 = master_pairs[i][3]
                if ((type(l1)==type(Electron())) and type(l2)==type(Electron())):
                    R_ee_pT.Fill(l1.PT + l2.PT)
                    R_ee_eta.Fill((l1.Eta + l2.Eta)/2.0)
                    R_ee_mass.Fill(l1.P4().M() + l2.P4().M())
                    if (l1.Charge < l2.Charge):
                        R_ee_deltaEta.Fill(l1.Eta - l2.Eta)
                    else:
                        R_ee_deltaEta.Fill(l2.Eta - l1.Eta)
                    ee = ee +1
                elif ((type(l1)==type(Muon())) and type(l2)==type(Muon())):
                    R_mumu_pT.Fill(l1.PT + l2.PT)
                    R_mumu_eta.Fill((l1.Eta + l2.Eta)/2.0)
                    R_mumu_mass.Fill(l1.P4().M() + l2.P4().M())
                    if (l1.Charge < l2.Charge):
                        R_mumu_deltaEta.Fill(l1.Eta - l2.Eta)
                    else:
                        R_mumu_deltaEta.Fill(l2.Eta - l1.Eta)
                    mumu = mumu +1
                elif ((type(l1)==type(Electron())) and type(l2)==type(Muon())):
                    R_emu_pT.Fill(l1.PT + l2.PT)
                    R_emu_eta.Fill((l1.Eta + l2.Eta)/2.0)
                    R_emu_mass.Fill(l1.P4().M() + l2.P4().M())
                    if (l1.Charge < l2.Charge):
                        R_emu_deltaEta.Fill(l1.Eta - l2.Eta)
                    else:
                        R_emu_deltaEta.Fill(l2.Eta - l1.Eta)
                    emu = emu +1
                elif ((type(l1)==type(Muon())) and type(l2)==type(Electron())):
                    R_emu_pT.Fill(l1.PT + l2.PT)
                    R_emu_eta.Fill((l1.Eta + l2.Eta)/2.0)
                    R_emu_mass.Fill(l1.P4().M() + l2.P4().M())
                    if (l1.Charge < l2.Charge):
                        R_emu_deltaEta.Fill(l1.Eta - l2.Eta)
                    else:
                        R_emu_deltaEta.Fill(l2.Eta - l1.Eta)
                    emu = emu +1
                                           
        R_ee_multiplicity.Fill(ee)
        R_mumu_multiplicity.Fill(mumu)
        R_emu_multiplicity.Fill(emu)
        """
    output.Write()
