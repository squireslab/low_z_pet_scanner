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

#ifndef MyNtupleEnergy_hh
#define MyNtupleEnergy_hh

#include "TsVNtupleScorer.hh"

class MyNtupleEnergy : public TsVNtupleScorer
{
public:
	MyNtupleEnergy(TsParameterManager* pM, TsMaterialManager* mM, TsGeometryManager* gM, TsScoringManager* scM, TsExtensionManager* eM,
				G4String scorerName, G4String quantity, G4String outFileName, G4bool isSubScorer);

	virtual ~MyNtupleEnergy();

	G4bool ProcessHits(G4Step*,G4TouchableHistory*);

private:
	// Output variables
	G4double fEnergy;
	G4double fDeposit;
	G4float fWeight;
	G4int fParticleType;
	G4bool fIsNewHistory;
	G4float fTimeOfFlight;
	G4int fEvent;

	G4int fRunID;
	G4int fEventID;
	G4int fPrevRunID;
	G4String fOriginProcessName;
	G4int fOriginProcessID;
	G4int fPrevEventID;
	G4int fTrackID;
	G4float fPosX;
	G4float fPosY;
	G4float fPosZ;
};
#endif
