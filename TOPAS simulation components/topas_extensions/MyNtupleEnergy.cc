// Scorer for MyNtupleEnergy
//
// ********************************************************************
// *                                                                  *
// *                                                                  *
// * This file was obtained from Topas MC Inc under the license       *
// * agreement set forth at http://www.topasmc.org/registration       *
// * Any use of this file constitutes full acceptance of              *
// * this TOPAS MC license agreement.                                 *
// *                                                                  *
// ********************************************************************
//

#include "MyNtupleEnergy.hh"

#include "G4PSDirectionFlag.hh"
#include "TsTrackInformation.hh"
#include "G4VProcess.hh"
#include "G4Event.hh"

MyNtupleEnergy::MyNtupleEnergy(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
						  G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer)
						 : TsVNtupleScorer(pM, mM, gM, scM, eM, scorerName, quantity, outFileName, isSubScorer)
{
	// SetSurfaceScorer();

	fNtuple->RegisterColumnI(&fEvent, "Event Number");
	fNtuple->RegisterColumnD(&fEnergy, "Energy", "keV");
	fNtuple->RegisterColumnD(&fDeposit, "Energy Deposited", "keV");
	fNtuple->RegisterColumnF(&fPosX, "Position X", "cm");
	fNtuple->RegisterColumnF(&fPosY, "Position Y", "cm");
	fNtuple->RegisterColumnF(&fPosZ, "Position Z", "cm");
	// fNtuple->RegisterColumnF(&fWeight, "Weight", "");
	fNtuple->RegisterColumnF(&fTimeOfFlight, "Time of Flight", "ns");
	fNtuple->RegisterColumnI(&fParticleType, "Particle Type (in PDG Format)");
	// fNtuple->RegisterColumnS(&fOriginProcessName, "Origin Process");
	// fNtuple->RegisterColumnI(&fOriginProcessID, "Origin Process (int)");
	fNtuple->RegisterColumnI(&fTrackID, "Particle ID");
}


MyNtupleEnergy::~MyNtupleEnergy() {;}


G4bool MyNtupleEnergy::ProcessHits(G4Step* aStep,G4TouchableHistory*)
{
	if (!fIsActive) {
		fSkippedWhileInactive++;
		return false;
	}

	ResolveSolid(aStep);

	G4StepPoint* theStepPoint=0;
	// G4int direction = GetDirection();
	fDeposit			= aStep->GetTotalEnergyDeposit();
	// if (fDeposit == 0) {
	// 	return true;
	// }

	fEnergy				= aStep->GetPreStepPoint()->GetKineticEnergy();
	fWeight 			= aStep->GetPreStepPoint()->GetWeight();
	fTimeOfFlight 		= aStep->GetTrack()->GetGlobalTime();


	G4ThreeVector pos 	= aStep->GetPreStepPoint()->GetPosition();

	fPosX				= pos.x();
	fPosY				= pos.y();
	fPosZ				= pos.z();

	fParticleType 		= aStep->GetTrack()->GetDefinition()->GetPDGEncoding();

	fEvent			= GetEventID();
	
	fTrackID			= aStep->GetTrack()->GetTrackID();


	const G4VProcess* originProcess = aStep->GetTrack()->GetCreatorProcess();
	if (originProcess) {
		fOriginProcessName = originProcess->GetProcessName();
		// fOriginProcessID = (int)fOriginProcessName[0] << 24;
		// fOriginProcessID += (int)fOriginProcessName[0] << 16;
		// fOriginProcessID += (int)fOriginProcessName[0] << 8;
		// fOriginProcessID += (int)fOriginProcessName[0];
	}
	else
		fOriginProcessName = "Primary";
		// fOriginProcessID = 0;
	

	// Check if this is a new history
	// fRunID   = GetRunID();
	// fEventID = GetEventID();
	// if (fEventID != fPrevEventID || fRunID != fPrevRunID) {
	// 	fIsNewHistory = true;
	// 	fPrevEventID = fEventID;
	// 	fPrevRunID = fRunID;
	// } else {
	// 	fIsNewHistory = false;
	// }

	fNtuple->Fill();
	return true;
}
