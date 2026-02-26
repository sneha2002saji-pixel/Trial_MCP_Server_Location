package com.example.yourapp.auth

import android.content.Context
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity

/**
 * Module: BiometricAuthenticator
 * Purpose: Handles biometric authentication for Android applications.
 * Author: Gemini (Autonomous Senior Developer)
 * Created: 2024-01-01 (Placeholder)
 * Notes: This class abstracts the Android BiometricPrompt API for easier integration.
 */
class BiometricAuthenticator(private val context: Context) {

    /**
     * Interface: BiometricCallback
     * Purpose: Defines callbacks for biometric authentication results.
     */
    interface BiometricCallback {
        /**
         * Short description of what the function does.
         *
         * Args:
         *     None
         *
         * Returns:
         *     None
         */
        fun on_authentication_success()

        /**
         * Short description of what the function does.
         *
         * Args:
         *     None
         *
         * Returns:
         *     None
         */
        fun on_authentication_failure()

        /**
         * Called when an unrecoverable error has been encountered and authentication has been stopped.
         *
         * Args:
         *     error_code (int): An integer identifying the error message.
         *     err_string (CharSequence): A human-readable error message.
         *
         * Returns:
         *     None
         */
        fun on_authentication_error(error_code: Int, err_string: CharSequence)
    }

    private lateinit var biometric_prompt: BiometricPrompt
    private lateinit var prompt_info: BiometricPrompt.PromptInfo

    /**
     * Checks if biometric authentication is available and enrolled on the device.
     *
     * Args:
     *     None
     *
     * Returns:
     *     int: An integer indicating the authentication capability.
     *          Possible values from BiometricManager: BIOMETRIC_SUCCESS, BIOMETRIC_ERROR_NO_HARDWARE,
     *          BIOMETRIC_ERROR_HW_UNAVAILABLE, BIOMETRIC_ERROR_NONE_ENROLLED.
     */
    fun can_authenticate(): Int {
        val biometric_manager = BiometricManager.from(context)
        return biometric_manager.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_WEAK or BiometricManager.Authenticators.DEVICE_CREDENTIAL)
    }

    /**
     * Initiates biometric authentication.
     *
     * Args:
     *     activity (FragmentActivity): The activity that will host the biometric prompt.
     *     title (String): The title to be displayed on the biometric prompt.
     *     subtitle (String): The subtitle to be displayed on the biometric prompt.
     *     description (String): The description to be displayed on the biometric prompt.
     *     negative_button_text (String): The text for the negative button (fallback mechanism).
     *     callback (BiometricCallback): The callback interface to handle authentication results.
     *
     * Returns:
     *     None
     */
    fun authenticate(
        activity: FragmentActivity,
        title: String,
        subtitle: String,
        description: String,
        negative_button_text: String,
        callback: BiometricCallback
    ) {
        val executor = ContextCompat.getMainExecutor(context)

        biometric_prompt = BiometricPrompt(activity, executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationError(error_code: Int, err_string: CharSequence) {
                    super.onAuthenticationError(error_code, err_string)
                    callback.on_authentication_error(error_code, err_string)
                }

                override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                    super.onAuthenticationSucceeded(result)
                    callback.on_authentication_success()
                }

                override fun onAuthenticationFailed() {
                    super.onAuthenticationFailed()
                    callback.on_authentication_failure()
                }
            })

        prompt_info = BiometricPrompt.PromptInfo.Builder()
            .setTitle(title)
            .setSubtitle(subtitle)
            .setDescription(description)
            .setNegativeButtonText(negative_button_text) // Fallback mechanism
            .setAllowedAuthenticators(BiometricManager.Authenticators.BIOMETRIC_WEAK or BiometricManager.Authenticators.DEVICE_CREDENTIAL)
            .build()

        biometric_prompt.authenticate(prompt_info)
    }
}
