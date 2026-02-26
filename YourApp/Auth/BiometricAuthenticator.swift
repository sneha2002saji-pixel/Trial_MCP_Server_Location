import Foundation
import LocalAuthentication

class BiometricAuthenticator {

    enum BiometricError: Error {
        case authenticationFailed
        case userCancel
        case userFallback
        case systemCancel
        case passcodeNotSet
        case biometryNotAvailable
        case biometryNotEnrolled
        case unknown
    }

    func canAuthenticate() -> Bool {
        let context = LAContext()
        var error: NSError?
        // Check if the device supports biometry and if a biometric identity is enrolled
        return context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error)
    }

    func authenticate(reason: String, completion: @escaping (Result<Bool, BiometricError>) -> Void) {
        let context = LAContext()
        var error: NSError?

        // First check if we can even evaluate the policy
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            // Handle cases where biometry is not available or not enrolled
            if let laError = error as? LAError {
                switch laError.code {
                case .appCancel, .authenticationFailed, .invalidContext, .notInteractive:
                    completion(.failure(.authenticationFailed))
                case .userCancel:
                    completion(.failure(.userCancel))
                case .userFallback:
                    completion(.failure(.userFallback))
                case .systemCancel:
                    completion(.failure(.systemCancel))
                case .passcodeNotSet:
                    completion(.failure(.passcodeNotSet))
                case .biometryNotAvailable:
                    completion(.failure(.biometryNotAvailable))
                case .biometryNotEnrolled:
                    completion(.failure(.biometryNotEnrolled))
                @unknown default:
                    completion(.failure(.unknown))
                }
            } else {
                completion(.failure(.unknown))
            }
            return
        }

        // Proceed with authentication
        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, authenticationError in
            DispatchQueue.main.async {
                if success {
                    completion(.success(true))
                } else {
                    if let laError = authenticationError as? LAError {
                        switch laError.code {
                        case .appCancel, .authenticationFailed, .invalidContext, .notInteractive:
                            completion(.failure(.authenticationFailed))
                        case .userCancel:
                            completion(.failure(.userCancel))
                        case .userFallback:
                            completion(.failure(.userFallback))
                        case .systemCancel:
                            completion(.failure(.systemCancel))
                        case .passcodeNotSet:
                            completion(.failure(.passcodeNotSet))
                        case .biometryNotAvailable:
                            completion(.failure(.biometryNotAvailable))
                        case .biometryNotEnrolled:
                            completion(.failure(.biometryNotEnrolled))
                        @unknown default:
                            completion(.failure(.unknown))
                        }
                    } else {
                        completion(.failure(.unknown))
                    }
                }
            }
        }
    }
}