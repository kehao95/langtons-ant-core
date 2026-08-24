import OneBlack.Certificates

namespace OneBlack.ScatteringLeaf

theorem verified : Certificates.report = true := by
  native_decide

def certificate : Certificates.Bundle :=
  Certificates.bundle_of_report verified

end OneBlack.ScatteringLeaf
