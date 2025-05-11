from fastapi import HTTPException
import traceback
import functools

def catch_exceptions():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
                raise HTTPException(status_code=500, detail={"error": "Internal Server Error"})
        return wrapper
    return decorator


class AlreadyExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
