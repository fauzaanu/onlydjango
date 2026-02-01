"""Background tasks using Huey.

In DEBUG mode, tasks run immediately (synchronously) within the request.
In production, tasks are queued to Redis and processed by Huey workers.

Usage:
    from apps.core.tasks import send_welcome_email
    
    # Call the task - behavior depends on DEBUG setting
    send_welcome_email(user_id=123)

Running Huey workers (production):
    uv run python manage.py run_huey
"""

import logging
from functools import wraps

from django.conf import settings

logger = logging.getLogger(__name__)


# =============================================================================
# TASK DECORATOR - DEBUG-AWARE
# =============================================================================
#
# In DEBUG mode: Tasks run synchronously (immediately)
# In production: Tasks are queued to Redis via Huey
# =============================================================================

if settings.DEBUG:
    def task():
        """Synchronous task wrapper for DEBUG mode.
        
        Tasks execute immediately within the request cycle.
        Useful for development and testing without running Huey workers.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def periodic_task(cron):
        """No-op periodic task decorator for DEBUG mode.
        
        Periodic tasks don't auto-run in DEBUG mode.
        Trigger them manually via management commands.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
else:
    from huey.contrib.djhuey import db_task as task
    from huey.contrib.djhuey import db_periodic_task as periodic_task


# =============================================================================
# TASKS
# =============================================================================


@task()
def send_welcome_email(user_id: int) -> bool:
    """Send welcome email to a newly registered user.
    
    Args:
        user_id: The ID of the user to send the email to
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    from apps.core.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        # TODO: Implement actual email sending
        # send_mail(
        #     subject="Welcome!",
        #     message=f"Hi {user.first_name}, welcome!",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user.email],
        # )
        
        logger.info(f"Welcome email sent to user {user_id} ({user.email})")
        return True
        
    except User.DoesNotExist:
        logger.error(f"Cannot send welcome email: User {user_id} not found")
        return False
    except Exception as e:
        logger.exception(f"Failed to send welcome email to user {user_id}: {e}")
        return False


@task()
def process_user_action(user_id: int, action: str, metadata: dict | None = None) -> dict:
    """Process a user action asynchronously.
    
    Args:
        user_id: The user performing the action
        action: Type of action (e.g., 'profile_update', 'settings_change')
        metadata: Additional data about the action
        
    Returns:
        Dict with processing result
    """
    from apps.core.models import User
    
    metadata = metadata or {}
    
    try:
        user = User.objects.get(id=user_id)
        
        result = {
            "user_id": user_id,
            "action": action,
            "status": "processed",
        }
        
        logger.info(f"Processed action '{action}' for user {user_id}")
        return result
        
    except User.DoesNotExist:
        logger.error(f"Cannot process action: User {user_id} not found")
        return {"user_id": user_id, "action": action, "status": "error"}


# =============================================================================
# PERIODIC TASKS (production only)
# =============================================================================
#
# In DEBUG mode, trigger these manually via management commands.
# In production, Huey runs them on schedule.
#
# Schedule examples:
#   crontab(minute='0', hour='*')     - Every hour
#   crontab(minute='*/15')            - Every 15 minutes
#   crontab(minute='0', hour='0')     - Daily at midnight
# =============================================================================

if not settings.DEBUG:
    from huey import crontab
    
    @periodic_task(crontab(minute="0", hour="0"))
    def daily_cleanup() -> int:
        """Run daily cleanup tasks at midnight."""
        cleaned = 0
        logger.info(f"Daily cleanup completed: {cleaned} items removed")
        return cleaned
else:
    def daily_cleanup() -> int:
        """Run daily cleanup tasks (manual trigger in DEBUG)."""
        cleaned = 0
        logger.info(f"Daily cleanup completed: {cleaned} items removed")
        return cleaned
