import OneBlack.Prefix

namespace OneBlack.PrefixLeaf

theorem verified : Prefix.report = true := by
  native_decide

def certificate : Prefix.Certificate :=
  Prefix.certificate_of_report verified

end OneBlack.PrefixLeaf
