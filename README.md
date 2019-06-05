# biometric-typing

Implements a ML-based system to identify users based on biometric data about their typing

Dependencies: numpy, pynput

Designed for execution on Linux/macOS systems.  If macOS, requires macOS SIP to be disabled, your terminal of choice to be whitelisted in Security & Privacy/Privacy/Accessibility settings.  On some systems, the process will need to be run as root.  These restrictions will be eventually lifted, but are required without a certificate.

# Models
- Manhattan NN
- Euclidean NN
- Mahalanobis Distribution NN
- Support-Vector Machine (with polynomial kernel and radial basis)
- Logistic Regression (with adam-optimized SGD)
