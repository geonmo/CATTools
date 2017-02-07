import FWCore.ParameterSet.Config as cms
process = cms.Process("CATeX")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.options.allowUnscheduled = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 50000

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
from CATTools.Validation.commonTestInput_cff import commonTestCATTuples
process.source.fileNames = commonTestCATTuples["bkg"]
process.load("CATTools.CatAnalyzer.filters_cff")
process.load("CATTools.Validation.ttljEventSelector_cff")
process.load("CATTools.Validation.validation_cff")

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("hist.root"),
)

process.eventsTTLJ.filters.ignoreTrig = True
process.eventsTTLJ.skipHistograms = True
process.eventsTTLJ.applyFilterAt = 7 ## save events from step 5c, nJet>=3

process.load("CATTools.CatAnalyzer.analyzers.ttLJAnalyzer_cff")
process.load("CATTools.CatAnalyzer.csvWeights_cfi")
process.filterRECO = process.filterRECOMC.clone()
delattr(process, 'filterRECOMC')

process.pTTLJ = cms.Path(
    process.gen# + process.rec
  * process.eventsTTLJ
  * process.ttLJ
)

## Customise with cmd arguments
import sys
if len(sys.argv) > 2:
    for l in sys.argv[2:]: exec('process.'+l)

