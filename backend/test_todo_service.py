"""Tests for ToDo service implementation"""

import asyncio
import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.todo_task import ToDoTask, TaskStatus, TaskPriority
from app.core.service_clients import ToDoService


@pytest.fixture
async def test_db():
    """Create test database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user(test_db: AsyncSession):
    """Create a test user"""
    user = User(
        auth0_id="auth0|test_user_123",
        email="test@example.com",
        name="Test User"
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.mark.asyncio
async def test_create_task(test_db: AsyncSession, test_user: User):
    """Test creating a new task"""
    todo_service = ToDoService(test_db)
    
    task = await todo_service.create_task(
        user_id=test_user.id,
        title="Test Task",
        description="Test Description",
        priority="high",
        due_date=datetime.now(timezone.utc) + timedelta(days=1)
    )
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_get_tasks(test_db: AsyncSession, test_user: User):
    """Test getting all tasks for a user"""
    todo_service = ToDoService(test_db)
    
    # Create multiple tasks
    await todo_service.create_task(
        user_id=test_user.id,
        title="Task 1",
        priority="low"
    )
    await todo_service.create_task(
        user_id=test_user.id,
        title="Task 2",
        priority="high"
    )
    await todo_service.create_task(
        user_id=test_user.id,
        title="Task 3",
        priority="medium"
    )
    
    tasks = await todo_service.get_tasks(user_id=test_user.id)
    
    assert len(tasks) == 3
    # Should be ordered by priority (high first)
    assert tasks[0].priority == TaskPriority.HIGH
    assert tasks[1].priority == TaskPriority.MEDIUM
    assert tasks[2].priority == TaskPriority.LOW


@pytest.mark.asyncio
async def test_update_task_status(test_db: AsyncSession, test_user: User):
    """Test updating task status"""
    todo_service = ToDoService(test_db)
    
    task = await todo_service.create_task(
        user_id=test_user.id,
        title="Test Task"
    )
    
    assert task.status == TaskStatus.PENDING
    
    updated_task = await todo_service.update_task_status(
        user_id=test_user.id,
        task_id=task.id,
        status="completed"
    )
    
    assert updated_task.status == TaskStatus.COMPLETED
    assert updated_task.completed_at is not None


@pytest.mark.asyncio
async def test_delete_task(test_db: AsyncSession, test_user: User):
    """Test deleting a task"""
    todo_service = ToDoService(test_db)
    
    task = await todo_service.create_task(
        user_id=test_user.id,
        title="Test Task"
    )
    
    success = await todo_service.delete_task(
        user_id=test_user.id,
        task_id=task.id
    )
    
    assert success is True
    
    # Verify task is deleted
    tasks = await todo_service.get_tasks(user_id=test_user.id)
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_get_pending_tasks_count(test_db: AsyncSession, test_user: User):
    """Test getting count of pending tasks"""
    todo_service = ToDoService(test_db)
    
    # Create tasks with different statuses
    await todo_service.create_task(user_id=test_user.id, title="Pending Task 1")
    await todo_service.create_task(user_id=test_user.id, title="Pending Task 2")
    task3 = await todo_service.create_task(user_id=test_user.id, title="Completed Task")
    
    await todo_service.update_task_status(
        user_id=test_user.id,
        task_id=task3.id,
        status="completed"
    )
    
    count = await todo_service.get_pending_tasks_count(user_id=test_user.id)
    
    assert count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
