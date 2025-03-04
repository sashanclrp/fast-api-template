from fastapi import HTTPException, Request, Query
from typing import Dict, Any

from services.webhook_service import process_webhook
from config.env import WEBHOOK_VERIFY_TOKEN
from utils.logger import logger

class WebhookController:
    """
    Controller for handling webhook requests.
    """
    
    @staticmethod
    async def verify_webhook(token: str) -> Dict[str, Any]:
        """
        Verify a webhook request with the provided token.
        
        Args:
            token: The verification token
            
        Returns:
            A dictionary with the verification status
            
        Raises:
            HTTPException: If the token is invalid
        """
        expected_token = WEBHOOK_VERIFY_TOKEN
        
        if not expected_token:
            logger.warning("WEBHOOK_VERIFICATION_TOKEN is not set")
            return {"message": "Webhook verification token is not configured"}
        
        if token != expected_token:
            logger.warning(f"Invalid webhook verification token: {token}")
            raise HTTPException(status_code=401, detail="Invalid verification token")
        
        logger.info("Webhook verification successful")
        return {"message": "Webhook verification successful"}
    
    @staticmethod
    async def receive_webhook(request: Request) -> Dict[str, Any]:
        """
        Receive and process a webhook request.
        
        Args:
            request: The FastAPI request object
            
        Returns:
            A dictionary with the processing result
            
        Raises:
            HTTPException: If there's an error processing the webhook
        """
        try:
            body = await request.json()
            logger.info(f"Received webhook: {body}")
            
            # Process the webhook
            result = await process_webhook(body)
            
            return {"message": "Webhook received successfully", "result": result}
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")
    
    @staticmethod
    async def handle_webhook_callback(callback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a webhook callback.
        
        Args:
            callback_data: The callback data
            
        Returns:
            A dictionary with the callback processing result
        """
        try:
            logger.info(f"Received webhook callback: {callback_data}")
            
            # Process the callback
            # This is a placeholder for your actual callback processing logic
            
            return {"message": "Webhook callback processed successfully"}
        except Exception as e:
            logger.error(f"Error processing webhook callback: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error processing webhook callback: {str(e)}") 