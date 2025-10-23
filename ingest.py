# -*- coding: utf-8 -*-
"""Script to run the intelligent ingestion process for a user."""

from app.core.factory import AppFactory


def main():
    """
    Initializes and runs the ingestion service for the default user.
    """
    # For now, we hardcode the user_id. In a real application,
    # this would come from an authentication layer.
    user_id = "default_user"
    
    ingestion_service = AppFactory.create_ingestion_service(user_id=user_id)
    ingestion_service.run_ingestion()


if __name__ == "__main__":
    main()
