import Foundation
import LocalAuthentication

/**
 * Module: BiometricAuthenticator
 * Purpose: Handles biometric authentication for iOS applications.
 * Author: Gemini (Autonomous Senior Developer)
 * Created: 2024-01-01 (Placeholder)
 * Notes: This class abstracts the iOS Local Authentication Framework for easier integration.
 */
class BiometricAuthenticator {

    /**
     * Enum: BiometricError
     * Purpose: Defines specific error cases for biometric authentication failures.
     */
    enum BiometricError: Error {
        case authentication_failed
        case user_cancel
        case user_fallback
        case system_cancel
        case passcode_not_set
        case biometry_not_available
        case biometry_not_enrolled
        case unknown
    }

    /**
     * Checks if biometric authentication is available and enrolled on the device.
     *
     * Args:
     *     None
     *
     * Returns:
     *     Bool: True if biometry can be used for authentication, false otherwise.
     */
    func can_authenticate() -> Bool {
        let context = LAContext()
        var error: NSError?
        // Check if the device supports biometry and if a biometric identity is enrolled
        return context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error)
    }

    /**
     * Initiates biometric authentication.
     *
     * Args:
     *     reason (String): The reason string displayed to the user in the authentication prompt.
     *     completion (Result<Bool, BiometricError>): A closure to be called upon authentication completion.
     *                                                  It returns .success(true) on success or .failure(BiometricError) on failure.
     *
     * Returns:
     *     None
     */
    func authenticate(reason: String, completion: @escaping (Result<Bool, BiometricError>) -> Void) {
        let context = LAContext()
        var error: NSError?

        // First check if we can even evaluate the policy
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            // Handle cases where biometry is not available or not enrolled
            if let la_error = error as? LAError {
                switch la_error.code {
                case .appCancel, .authenticationFailed, .invalidContext, .notInteractive:
                    completion(.failure(.authentication_failed))
                case .userCancel:
                    completion(.failure(.user_cancel))
                case .userFallback:
                    completion(.failure(.user_fallback))
                case .systemCancel:
                    completion(.failure(.system_cancel))
                case .passcodeNotSet:
                    completion(.failure(.passcode_not_set))
                case .biometryNotAvailable:
                    completion(.failure(.biometry_not_available))
                case .biometryNotEnrolled:
                    completion(.failure(.biometry_not_enrolled))
                @unknown default:
                    completion(.failure(.unknown))
                }
            } else {
                completion(.failure(.unknown))
            }
            return
        }

        // Proceed with authentication
        context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, authentication_error in
            DispatchQueue.main.async {
                if success {
                    completion(.success(true))
                } else {
                    if let la_error = authentication_error as? LAError {
                        switch la_error.code {
                        case .appCancel, .authenticationFailed, .invalidContext, .notInteractive:
                            completion(.failure(.authentication_failed))
                        case .userCancel:
                            completion(.failure(.user_cancel))
                        case .userFallback:
                            completion(.failure(.user_fallback))
                        case .systemCancel:
                            completion(.failure(.system_cancel))
                        case .passcodeNotSet:
                            completion(.failure(.passcode_not_set))
                        case .biometryNotAvailable:
                            completion(.failure(.biometry_not_available))
                        case .biometryNotEnrolled:
                            completion(.failure(.biometry_not_enrolled))
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
