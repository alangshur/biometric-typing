# biometric-typing

Implements a system to identify users based on biometric data about their typing

# Models
- Manhattan Model:
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model)
    - Inference: Score by computing Manhattan distance between mean vector and new password-timing vector
- Euclidean Model: 
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model)
    - Inference: Score by computing squared Euclidean distance between mean vector and new password-timing vector
- Euclidean Model: 
    - Training: Take password-timing vectors and calculate mean timing vector (becomes detection model)
    - Inference: Score by computing squared Mahalanobis distance between mean vector and new password-timing vector
