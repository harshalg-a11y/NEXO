from typing import Optional
import hashlib
import secrets
from app.config import settings

class NexoPaisaService:
    """Service for Nexo Paisa payment integration"""
    
    def __init__(self):
        self.api_key = settings.nexo_paisa_api_key
        self.webhook_secret = settings.nexo_paisa_webhook_secret
    
    def create_payment(
        self, 
        amount: float, 
        currency: str = "NPR",
        description: Optional[str] = None,
        return_url: Optional[str] = None
    ) -> dict:
        """
        Create a payment request with Nexo Paisa.
        
        Args:
            amount: Payment amount
            currency: Currency code (default: NPR)
            description: Payment description
            return_url: URL to redirect after payment
            
        Returns:
            Dictionary with payment URL and reference
        """
        if not self.api_key:
            # Return mock response if API key not configured
            reference = f"MOCK-{secrets.token_hex(8).upper()}"
            return {
                "success": True,
                "payment_url": f"https://nexopaisa.example.com/pay/{reference}",
                "reference": reference,
                "message": "Payment initiated (mock mode)"
            }
        
        # TODO: Implement actual Nexo Paisa API integration
        # For now, return a placeholder response
        reference = f"NXP-{secrets.token_hex(8).upper()}"
        return {
            "success": True,
            "payment_url": f"https://nexopaisa.example.com/pay/{reference}",
            "reference": reference,
            "message": "Payment initiated"
        }
    
    def verify_webhook_signature(self, payload: dict, signature: str) -> bool:
        """
        Verify webhook signature from Nexo Paisa.
        
        Args:
            payload: Webhook payload
            signature: Signature from webhook headers
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.webhook_secret:
            # In development without webhook secret, accept all
            return True
        
        # TODO: Implement actual signature verification
        # This would typically involve HMAC with the webhook secret
        expected = hashlib.sha256(
            f"{self.webhook_secret}{payload}".encode()
        ).hexdigest()
        
        return signature == expected
    
    def get_payment_status(self, reference: str) -> dict:
        """
        Get the status of a payment by reference.
        
        Args:
            reference: Payment reference
            
        Returns:
            Dictionary with payment status
        """
        # TODO: Implement actual API call to check status
        return {
            "reference": reference,
            "status": "pending",
            "message": "Status check not implemented"
        }

# Global instance
nexo_paisa_service = NexoPaisaService()
