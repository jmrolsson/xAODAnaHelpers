/******************************************
 *
 * This class gets HLT jets from the TDT and can be expanded to get other features
 *
 * Merlin Davies (merlin.davies@cern.ch)
 * Caterina Doglioni (caterina.doglioni@cern.ch)
 * John Alison (john.alison@cern.ch)
 *
 *
 ******************************************/

#ifndef xAODAnaHelpers_HLTJetGetter_H
#define xAODAnaHelpers_HLTJetGetter_H


// algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"


namespace TrigConf {
    class xAODConfigTool;
}

namespace Trig {
    class TrigDecisionTool;
}


class HLTJetGetter : public xAH::Algorithm
{

public:

  /* configuration variables */
  std::string m_triggerList; // List of triggers whose features will be extracted from TDT
  std::string m_inContainerName; // input container name, WITHOUT the HLT_xAOD__JetContainer_ prefix
  std::string m_outContainerName; // output container name

private:

  Trig::TrigDecisionTool*        m_trigDecTool;   //!
  TrigConf::xAODConfigTool*      m_trigConfTool;   //!
  bool                           m_ownTDTAndTCT;   //!

public:

  // this is a standard constructor
  HLTJetGetter (std::string className = "HLTJetGetter");

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  /// @cond
  // this is needed to distribute the algorithm to the workers
  ClassDef(HLTJetGetter, 1);
  /// @endcond

};

#endif
