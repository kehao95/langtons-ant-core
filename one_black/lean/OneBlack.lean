import OneBlack.Verified

namespace OneBlack

theorem universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s := by
  let certificate := Verified.scattering
  let spectrum := Scattering.single_defect_scattering certificate.pristine
    certificate.actual certificate.phase
  intro s one
  exact Universal.universal_one_black Verified.prefixCertificate
    certificate.entry spectrum s one

end OneBlack
