import OneBlack.PrefixLeaf
import OneBlack.ScatteringLeaf
import OneBlack.Universal

namespace OneBlack.Verified

def prefixCertificate : Prefix.Certificate := PrefixLeaf.certificate
def scattering : Certificates.Bundle := ScatteringLeaf.certificate

end OneBlack.Verified
