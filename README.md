# biometric-typing

Implements a system to identify users based on biometric data about their typing

Dependencies:  numpy, pynput

Designed for execution on Linux/macOS systems.  If macOS, requires macOS SIP to be disabled, your terminal of choice to be whitelisted in Security & Privacy/Privacy/Accessibility settings.  On some systems, the process will need to be run as root.

# Models
- Manhattan Model:
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model)
    - Inference: Score by computing Manhattan distance between mean vector and new password-timing vector
- Euclidean Model: 
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model)
    - Inference: Score by computing squared Euclidean distance between mean vector and new password-timing vector
- Mahalanobis Model: 
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model) and timing distribution standard deviation
    - Inference: Score by computing squared Mahalanobis distance between mean vector and new password-timing vector
- Support-Vector Machine: 
    - Learning classification with kernel functions -- polynomial kernel and radial basis
   
